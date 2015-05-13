
import re
from datetime import datetime

class Buckets(dict):
    # default timeformat:
    # match = re.match('^(?P<days>[0-9]+)d(?P<weeks>[0-9]+)w(?P<months>[0-9]+)m(?P<years>[0-9]+)y$', retention)
    def __init__(self, retention):
        match = re.match('^(?P<days>[0-9]+)d(?P<weeks>[0-9]+)w(?P<months>[0-9]+)m(?P<years>[0-9]+)y$', retention)
        matchdata = match.groupdict()

        #for key in matchdata.keys():
        #    print key
        #    self[key] = int(matchdata[key])

        counter = -1
        for i in range(int(matchdata["days"])):
            counter += 1
            self[counter] = []
        for i in range(int(matchdata["weeks"])):
            counter += 7
            self[counter] = []
        for i in range(int(matchdata["months"])):
            counter += 28
            self[counter] = []
        for i in range(int(matchdata["years"])):
            counter += 336
            self[counter] = []
        
    def which_bucket(snasphot):
        age = snapshot.age
        if age < 7:
            return "days"
        if age < 28:
            return "weeks"
        if age < 336:
            return "months"
        return "years"
        

class Dataset(object):
    """
    This is the main object for a single dataset.
    It comes with it's set of buckets which then are filled with snapshots, and
    cleaned up pfollowing Khendrick algorithm:
    https://github.com/khenderick/zfs-snap-manager
    """
    def __init__(self, dataset, retention, timeformat='GMT-%Y.%m.%d-%H.%M.%S'):
        self.dataset = dataset
        self.buckets = Buckets(retention)
        self.now = datetime.now()
        self.timeformat = timeformat


    def fill_buckets(self, dataset):
        """
        walk snapshots and push them into their respective buckets, eliminating
        """
        for snapshot in sorted(dataset):
            days = (self.now - datetime.strptime(snapshot, self.timeformat)).days
            possible_keys = []
            for age in self.buckets:
                if days <= age:
                    possible_keys.append(age)
            if possible_keys:
                self.buckets[min(possible_keys)].append(snapshot)

        to_keep = {}
        to_delete = {}

        for key in self.buckets:
            oldest = None
            oldest_age = None
            if len(self.buckets[key]) == 1:
                oldest = self.buckets[key][0]
            else:
                for snapshot in self.buckets[key]:
                    age = (self.now - datetime.strptime(snapshot, self.timeformat)).days
                    if oldest is None:
                        oldest = snapshot
                        oldest_age = age
                    elif age > oldest_age:
                        oldest = snapshot
                        oldest_age = age
                    else:
                        to_delete[key] = to_delete.get(key, []) + [snapshot]
            to_keep[key] = oldest
            to_delete[key] = to_delete.get(key, [])
        for key in sorted(to_keep):
            print to_keep[key]
        for key in sorted(to_delete):
            print key
            print to_delete[key]

    def triage_buckets(self):
        """
        apply retention and possible specific one to the buckets / snapshots
        """
        pass

    def clean_snapshots(self):
        """
        Remove cleanable snapshots from buckets
        """
        pass

def track_removable(snapshots, retention):
# Manage retention get a set of snapshot and retention, returns list of snapshots to remove
    buckets = Buckets(retention)
    
    # fill snapshots in buckets
    for snapshot in snapshots:
        snap = Snapshot(snapshot[name], snapshot[name])
        bucket
        if is_in_bucket(snapshot):
            to_keep.add(snapshot)
        else:
            to_delete.add(snapshot)

    # remove out of retention snapshots

    for bucket in buckets:
        pass

