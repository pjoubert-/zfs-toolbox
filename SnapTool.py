#!/usr/bin/env python
# Some useful functions for snapshot management
#
# sync_snapshots: sync recursively datasets and snapshots from host1/dataset1 to host2/dataset2
#


import ZfsFunc
import time
import argparse
import Cleaner
import yaml
import pprint

"""
snapshots functions
"""
def get_snapshots(host, dataset):
    snapshots_list = ZfsFunc.list(host, dataset, type='snapshot', recursive=True, properties=['name', 'used', 'compressratio'])
    return snapshots_list

def find_last_common_snapshot(host_list_1, host_list_2, host_1_path, host_2_path):
    # dataset_not_in_host_list have to be fully synced
    dataset_not_in_host_list_2 = []
    # snapshots_not_in_host_list have to be synced (if newer than last common snapshot)
    snapshot_not_in_host_list_2 = {}

    # here we iter on each datasets available on host1
    for dataset in host_list_1['values']:
        # common trunk helps just for the comparison of things 
        left_trunk = dataset.lstrip(host_1_path)

        # Not that hard, but a bit tricky : remove from host1 and add host 2 part
        dataset_h2 = host_2_path + dataset.split(host_1_path)[1]

        right_trunk = dataset.lstrip(host_2_path)
        is_common = dataset.split(host_1_path)
        host1_snaps = iter_snapshots(host_list_1['values'][dataset])
        # host1_snaps contains just the raw list of snapshots (no other information

        # dataset_not_in_host_list_2 tracks new datasets
        if not host_list_2['values'].has_key(dataset_h2):

            # we need the first and the last available snapshot
            first_key = sorted(host_list_1['values'][dataset].keys())[0]
            last_key = sorted(host_list_1['values'][dataset].keys())[-1]
            dataset_not_in_host_list_2.append((dataset, first_key, last_key))
        else:
            last_snapshot = ""
            for snap in sorted(host1_snaps):
                # snapshot not synced
                if not host_list_2['values'][dataset_h2].has_key(snap):
                    # new dataset, has to be referenced
                    if not snapshot_not_in_host_list_2.has_key(dataset):
                        snapshot_not_in_host_list_2[dataset] = []
                        # add the snapshot before to be able to send incremental data !
                        snapshot_not_in_host_list_2[dataset].append(last_snapshot)
                    snapshot_not_in_host_list_2[dataset].append(snap)
                else:
                    # if snapshot exists, just erase the key
                    if snapshot_not_in_host_list_2.has_key(dataset):
                        del snapshot_not_in_host_list_2[dataset]
                last_snapshot = snap

    print "snapshots to synchronize : %d" % len(snapshot_not_in_host_list_2)
    print "new datasets to synchronize : %d" % len(dataset_not_in_host_list_2)

    return dataset_not_in_host_list_2, snapshot_not_in_host_list_2

def iter_snapshots(dataset):
    return sorted(dataset)

def transfer_datasets(host_1, host_2, host_1_path, host_2_path, datasets, properties=None):
    for dataset in datasets:
        print "sending %s @ %s" % (dataset[0], dataset[1])
        ZfsFunc.send_dataset(host_1, host_2, dataset[0], host_2_path + dataset[0].split(host_1_path)[1], dataset[1],
                dataset[2], properties)

def transfer_snasphots(host_1, host_2, host_1_path, host_2_path, snapshots, properties=None):
    # snapshot is a dict of datasets, each element key is a dataset containing a list of snapshot
    for dataset in sorted(snapshots):
        print "sending snapshots of %s" % dataset
        ZfsFunc.send_snapshot(host_1, host_2, host_1_path, host_2_path + dataset.split(host_1_path)[1], dataset,
                snapshots[dataset], properties)



"""
higher level functions
"""
def sync_snapshots(args):
    # args.host1, args.source, args.host2, args.destination
    tps = time.time()
    try:
        conf = yaml.load(open(args.file))
    except yaml.YAMLError, exc:
        print "error in conf :", exc
        return
    for volume in sorted(conf):
        source_host = conf[volume]["source"]["host"]
        source_dataset = conf[volume]["source"]["dataset"]
        target_host = conf[volume]["destination"]["host"]
        target_dataset = conf[volume]["destination"]["dataset"]
        properties = conf[volume]["destination"]["properties"]
        host_1_list = get_snapshots(source_host, source_dataset)
        host_2_list = get_snapshots(target_host, target_dataset)

        print "On %s : %d datasets" % (source_host, len(host_1_list['values']))
        print "On %s : %d datasets" % (target_host, len(host_2_list['values']))

        new_datasets, new_snapshots = find_last_common_snapshot(host_1_list, host_2_list, source_dataset, target_dataset)

        transfer_datasets(source_host, target_host, source_dataset, target_dataset, new_datasets, properties)
        transfer_snasphots(source_host, target_host, source_dataset, target_dataset, new_snapshots, properties)
        totaltime = time.time() - tps
        print "total duration: %d seconds" % int(totaltime)
        print

def get_stats(args):
    """Computes statistics against the host"""

    datasets = get_snapshots(args.host, args.dataset)
    ndatasets = len(datasets['values'])
    nsnapshot = reduce(lambda x, y: x + y, [len(snapshots) for snapshots in datasets['values']])
    print "Snapshots in %s:%s : %s" % (args.host, args.dataset,nsnapshot)

def clean_holds(args):
    ZfsFunc.clean(args.host, args.dataset, args.hold)

def clean_snaps(args):
    try:
        conf = yaml.load(open(args.file))
    except yaml.yamlerror, exc :
        print "error in conf :", exc
        return
    p = pprint.PrettyPrinter()
    deleted = 0
    count = 0
    for host in sorted(conf):
        for volume in sorted(conf[host]):
            print "For %s at %s " % (volume, host)
            if not conf[host][volume].has_key('first'):
                first = 0
            else:
                first = conf[host][volume]['first']
            datasets = get_snapshots(host, volume)
            for dataset in sorted(datasets["values"]):
                snapshots = datasets["values"][dataset]
                data = Cleaner.Dataset(dataset,
                            conf[host][volume]['retention'],
                            first)
                to_keep, to_delete = data.fill_buckets(snapshots,)
                for snap in to_keep:
                    if to_keep[snap] is not None:
                        count += 1
                deleted += ZfsFunc.remove_snapshots(host, dataset, to_delete)
            print "snapshots kept: %d" % count
            print "snapshots cleaned: %d" % deleted

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help="Help for subcommand")

    parser_sync = subparsers.add_parser('sync', help="Synchronize snapshots between two hosts")
    parser_sync.set_defaults(func=sync_snapshots)
    parser_sync.add_argument("file", help="Configuration file for synchronization")

    parser_stat = subparsers.add_parser('stats', help='statistics')
    parser_stat.set_defaults(func=get_stats)
    parser_stat.add_argument("host", help="statistics for host")
    parser_stat.add_argument("dataset", help="target dataset")

    parser_hold = subparsers.add_parser('clean_holds', help="clean holds for dataset")
    parser_hold.set_defaults(func=clean_holds)
    parser_hold.add_argument("host", help="host to clean")
    parser_hold.add_argument("dataset", help="dataset to check")
    parser_hold.add_argument("hold", help="hold to remove")

    parser_snapclean = subparsers.add_parser('clean_snaps', help="clean snapshots bucket fashion way")
    parser_snapclean.set_defaults(func=clean_snaps)
    parser_snapclean.add_argument('file', help="Configuration file for retention")

    try:
        args = parser.parse_args()
        args.func(args)

    except argparse.ArgumentError:
        print str(e)
        parser.print_help()

