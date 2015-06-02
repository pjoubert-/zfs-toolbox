
import re
from datetime import datetime
import dateutil.relativedelta
import pprint

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
    def __init__(self, dataset, retention, firstday=0, timeformat='GMT-%Y.%m.%d-%H.%M.%S'):
        self.dataset = dataset
        self.buckets = Buckets(retention)
        self.now = datetime.now()
        self.firstday = firstday
        self.timeformat = timeformat


    def fill_buckets(self, dataset):
        """
        walk snapshots and push them into their respective buckets, eliminating
        """
## TODO: keep first snapshot of the month (if configured) in order to be able to store the monthly backup
##       test that datetime object.day = 1 and days < 32
        end_of_life_snapshots = {}
        for snapshot in sorted(dataset):
            try:
                days = (self.now - datetime.strptime(snapshot, self.timeformat)).days
                possible_keys = []
                for age in self.buckets:
                    if days <= age:
                        possible_keys.append(age)
                if possible_keys:
                    self.buckets[min(possible_keys)].append(snapshot)
                else:
                    end_of_life_snapshots[days] = end_of_life_snapshots.get(days, []) + [snapshot]
            except Exception, exc:
                print exc
                return
 
        first_days = []

        for i in range(self.firstday):
            d = datetime.strptime("%d-%d-%d" %
                        # trick is to use the second day of the month. Don't get it for the moment
                        (self.now.year, self.now.month, 2), "%Y-%m-%d")
            date = d - dateutil.relativedelta.relativedelta(months=i)
            age = self.now - date
            first_days.append(age.days)

        to_keep = {}
        to_delete = {}

        for key in sorted(self.buckets):
            oldest = None
            oldest_age = None
            if len(self.buckets[key]) == 1:
                oldest = self.buckets[key][0]
            else:
                for snapshot in sorted(self.buckets[key]):
                    age = (self.now - datetime.strptime(snapshot, self.timeformat)).days
                    if oldest is None:
                        oldest = snapshot
                        oldest_age = age
                    elif age in first_days:
                        pass
                    elif age > oldest_age:
                        oldest = snapshot
                        oldest_age = age
                    else:
                        to_delete[key] = to_delete.get(key, []) + [snapshot]
            to_keep[key] = oldest
            to_delete[key] = to_delete.get(key, [])
        to_delete.update(end_of_life_snapshots)
        return to_keep, to_delete

    def triage_buckets(self):
        """
        apply retention and possible specific one to the buckets / snapshots
        """
        pass

    def clean_snapshots(self, dataset, snapshots):
        """
        Remove cleanable snapshots from buckets
        """
        pass

