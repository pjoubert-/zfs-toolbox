A ZFS Toolbox
=============

Current functions
-----------------
* sync -> synchronize datasets (and subdatasets) from host 1 to host2

Fetches snapshots from host1 and host2, compare them, and send difference to host2: new datasets, and incremental stream
for existing datasets

* stats: lists the number of snapshots

* clean_snaps: handles snapshot retention with buckets
  can use a retention.conf file in yaml format for complex snapshot retention policy
  XXX: implemention not finished

