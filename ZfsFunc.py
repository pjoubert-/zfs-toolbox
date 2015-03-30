# Zfs helper functions

from subprocess import check_output, CalledProcessError

ZFS_COMMAND="zfs"
REMOTE_COMMAND="ssh"
GLOBAL_PARAMETERS="-H"
DRY="echo"

# this function aims to get a list of a remote dataset
def list(host, dataset, type='dataset', recursive=False, properties=['name']):
# returns a dict with the following structure:
#   dataset:
#   ---> properties:
#        ---> list of properties
#   ---> snapshot name:
#        ---> list of property values

    ordered_list={'properties': properties[1:], 'values': {}}
    if recursive: recurse="-r "
    else:
        recurse=""
    props = '-o' + ','.join(properties)
    command = (REMOTE_COMMAND, host, ZFS_COMMAND, "list", GLOBAL_PARAMETERS, props, "-t", type, recurse, dataset)
    try:
        for line in check_output(command).split('\n'):
            if line !="":
                prop_values = line.split()
                dataset, snapshot = prop_values.pop(0).split('@')
                if not ordered_list['values'].has_key(dataset):
                    ordered_list['values'][dataset] = {}
                ordered_list['values'][dataset][snapshot] = prop_values

    except CalledProcessError:
        return "list failed"
    return ordered_list

def send_dataset(host1, host2, source_set, target_path, snapshot):
    command = (REMOTE_COMMAND, host1, "%s send -RP %s@%s | %s %s %s recv -vF %s" % ( \
                        ZFS_COMMAND, source_set, snapshot, REMOTE_COMMAND, host2, ZFS_COMMAND, target_path))
    print "send dataset!"
    try:
        print "sending source_set ?"
        for line in check_output(command).split('\n'):
           if line !="":
               print line
       # command = ("ssh","sp7", 'ls | ssh sp7c wc')
       # print command
       # for line in check_output(command).split('\n'):
       #     print line
    except CalledProcessError:
        print "error sending dataset %s" % source_set
        print "command = %s" % str(command)
        return "send dataset failed"
    return True



def send_snapshot(host1, host2, source_set, target_path, dataset, snapshots):
    command = (REMOTE_COMMAND, host1, "%s send -I %s %s@%s | %s %s %s recv -vF %s" % \
                        (ZFS_COMMAND, snapshots[0], dataset, snapshots[-1], REMOTE_COMMAND, host2, ZFS_COMMAND,
                            target_path))
    print command
    try:
        print "sending snapshot"
        for line in check_output(command).split('\n'):
            print line
    except CalledProcessError:
        print "Error ! Error !"
    return
