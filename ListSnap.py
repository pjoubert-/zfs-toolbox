# Lists snapshots from a remote host, and return a list of them
#
#
#
#

import ZfsFunc
import time

host_1 = "sp7"
host_1_path = "data/midterm"

host_2 = "spsnpa3"
host_2_path = "backup/sp7"

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
            dataset_not_in_host_list_2.append(dataset)
        else:
            for snap in sorted(host1_snaps):

                # snapshot not synced
                if not host_list_2['values'][dataset_h2].has_key(snap):
                    # new dataset, has to be referenced
                    if not snapshot_not_in_host_list_2.has_key(dataset_h2):
                        snapshot_not_in_host_list_2[dataset] = []
                    snapshot_not_in_host_list_2[dataset].append(snap)

    print str(snapshot_not_in_host_list_2)
    print sorted(dataset_not_in_host_list_2)

    return dataset_not_in_host_list_2, snapshot_not_in_host_list_2

def iter_snapshots(dataset):
    return sorted(dataset)

def transfer_datasets(host_1, host_2, host_1_path, host_2_path, datasets):
    for dataset in datasets:
        ZfsFunc.send_dataset(host_1, host_2, dataset, host_2_path)
    pass

def transfer_snasphots(host_1, host_2, host_1_path, host_2_path, snapshots):
    pass

host_1_list = get_snapshots(host_1, host_1_path)
print "%s : %d" % (host_1, len(host_1_list['values']))
host_2_list = get_snapshots(host_2, host_2_path)
print "%s : %d" % (host_2, len(host_2_list['values']))
tps = time.time()
new_datasets, new_snapshots = find_last_common_snapshot(host_1_list, host_2_list, host_1_path, host_2_path)

transfer_datasets(host_1, host_2, host_1_path, host_2_path, new_datasets)

totaltime = time.time() - tps
print totaltime
