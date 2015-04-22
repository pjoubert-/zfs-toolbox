
import re
from datetime import datetime

class Buckets(dict):
    def __init__(self, retention):
        match = re.match('^(?P<days>[0-9]+)d(!P<weeks>[0-9]+)w(?P<months>[0-9]+)m(?P<years>[0-9]+)y$', retention)
        matchdata = match.groupdict()

        for key in matchdata.keys():
            self[key] = int(matchdata[key])

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
        self.format = timeformat
        
    def which_bucket(snasphot):
        age = snapshot.age
        if age < 7:
            return "days"
        if age < 28:
            return "weeks"
        if age < 336:
            return "months"
        return "years"
        

class Snapshot():
    def __init__(self, dataset, name, timeformat):
        self.parent = dataset
        now = datetime.now()
        self.age = now - datetime.strptime(name, timeformat).days

def track_removable(snapshots, retention):
# Manage retention get a set of snapshot and retention, returns list of snapshots to remove
    buckets = Buckets(retention)
    
    for snapshot in snapshots:
        snap = Snapshot(snapshot[name], snapshot[name])
        bucket
        if is_in_bucket(snapshot):
            to_keep.add(snapshot)
        else:
            to_delete.add(snapshot)
