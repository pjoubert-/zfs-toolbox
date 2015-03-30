# Some useful functions for snapshot management
#
# sync_snapshots: sync recursively datasets and snapshots from host1/dataset1 to host2/dataset2
#


import ZfsFunc
import time
import argparse


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
            # we need the last available snapshot
            last_key = sorted(host_list_1['values'][dataset].keys())[-1]
            dataset_not_in_host_list_2.append((dataset, last_key))
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
                last_snapshot = snap

    print "snapshots to sync %d" % len(snapshot_not_in_host_list_2)
    print "datasets to sync %d" % len(dataset_not_in_host_list_2)

    return dataset_not_in_host_list_2, snapshot_not_in_host_list_2

def iter_snapshots(dataset):
    return sorted(dataset)

def transfer_datasets(host_1, host_2, host_1_path, host_2_path, datasets):
    for dataset in datasets:
        print "sending %s @ %s" % (dataset[0], dataset[1])
        ZfsFunc.send_dataset(host_1, host_2, dataset[0], host_2_path + dataset[0].split(host_1_path)[1], dataset[1])

def transfer_snasphots(host_1, host_2, host_1_path, host_2_path, snapshots):
    # snapshot is a dict of datasets, each element key is a dataset containing a list of snapshot
    for dataset in snapshots:
        print "sending %s" % dataset
        ZfsFunc.send_snapshot(host_1, host_2, host_1_path, host_2_path + dataset.split(host_1_path)[1], dataset, snapshots[dataset])


"""
higher level functions
"""
def sync_snapshots(host1, source_path, host2, target_path):
    tps = time.time()
    host_1_list = get_snapshots(host1, source_path)
    print "%s : %d datasets" % (host1, len(host_1_list['values']))
    host_2_list = get_snapshots(host2, target_path)
    print "%s : %d datasets" % (host2, len(host_2_list['values']))
    totaltime = time.time() - tps
    print totaltime

    tps = time.time()
    new_datasets, new_snapshots = find_last_common_snapshot(host_1_list, host_2_list, source_path, target_path)
    totaltime = time.time() - tps
    tps = time.time()
    print totaltime

    print "datasets to send: %d" % len(new_datasets)
    transfer_datasets(host1, host2, source_path, target_path, new_datasets)
    transfer_snasphots(host1, host2, source_path, target_path, new_snapshots)
    totaltime = time.time() - tps
    print totaltime

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", help="action. Available actions: sync")
    parser.add_argument("host1",help="host to replictate from")
    parser.add_argument("source_dataset", help="origin dataset. Replication is recursive")
    parser.add_argument("host2", help="host to replicate to")
    parser.add_argument("target_dataset", help="destination dataset. Replication is recursive")
    try:
        args = parser.parse_args()
        if args.action == "sync":
            sync_snapshots(args.host1, args.source_dataset, args.host2, args.target_dataset)

    except argparse.ArgumentError:
        print str(e)
        parser.print_help()

