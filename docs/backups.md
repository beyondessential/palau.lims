# Database backups and packing policies

## Introduction

This document explains the backup policies set by default in both the 
[Virtual appliance][virtual_appliance] elaborated by Naralabs and the Ansible
recipe included in this extension profile. Please check 
[Virtual Appliance overview](appliance_overview.md) and 
[Deployment of the application stack with Ansible](ansible.md) for further 
information.

SENAITE uses [collective.recipe.backup][collective.recipe.backup] for the 
creation and restore of database backups. This "recipe" is mostly a wrapper 
around the `bin/repozo` script in Zope buildout, and is especially oriented 
to Plone applications and the like.

SENAITE relies on system's [cron][cron] to schedule backups regularly, as well 
as other maintenance tasks such as database packing.

## Database location and files

SENAITE uses ZODB, an object-oriented database. This database has two
components:

- filestorage: stores the objects (electronic records)
- blobstorage: stores files, attachments (binaries in general)

Each component is stored in its own folder:

- filestorage at `/home/senaite/data/filestorage`
- blobstorage at `/home/senaite/data/blobstorage`

## ZODB Database packing (zeopack) policies

SENAITE does not automatically prune deleted content and keeps all the 
transactions performed. The advantage is that it supplies a knowledgeable 
administrator with the ability to undo transactions on an emergency basis. 
However, this means the disk space consumed by ZODB will grow with every 
transaction.

Hence, the database needs to be packed periodically, or it will eventually
consume all available disk space.

The tool used for packing the database is `zeopack`, that is installed 
automatically by the [plone.recipe.zeoserver][plone.recipe.zeoserver]
recipe, that generates the zeoserver (database server component). `zeopack` can
be executed manually via `bin/zeopack`, that is located in the buildout 
directory of the Virtual Machine (`/home/senaite/senaite`). Nevertheless, the
system is automatically configured to do zeopacks periodically via 
[cron][cron], so manual zeopack should only be done in very rare occasions 
(e.g. after migrations).

Zeopack only affects to `filestorage` component.

### Cron configuration for zeopack

Virtual Appliance is configured to do zeopacks every day at 3 AM:

```
0 3 * * * cd /home/senaite/senaite && bin/zeopack && echo "zeopack""_success for senaite"
```

Note that this cron job belongs to user `senaite_daemon`, that is the user that
runs SENAITE services and owns the database. Thus, for the modification of the
periodicity of zeopack, the user `senaite_daemon` must be used. Hence, to 
change the periodicity (e.g. every day at 4:00 AM), login as `senaite_daemon` 
user: 

```shell
senaite@senaite:~$ sudo su senaite_daemon
senaite_daemon@senaite:/home/senaite$ crontab -e
```

and edit the cron tab as follows:

```
0 4 * * * cd /home/senaite/senaite && bin/zeopack && echo "zeopack""_success for senaite"
```

By default the system is configured so that zeopack retains one day of 
transactions history. If necessary, the setting `pack-days` can be modified in
the buildout file (`live.cfg`). Once modified, and for the changes to take 
effect, you need to run `bin/buildout -c live.cfg` with user `senaite`.

The version of the database before packing (`Data.fs.old`) is always kept in 
filestorage directory (`/home/senaite/data/senaite/filestorage`).

## Database backups policies

Virtual Appliance is configured to do backups via `cron` every day at 7:00 PM:

```
#Ansible: senaite Plone backup
0 19 * * * cd /home/senaite/senaite && bin/backup && echo "backup""_success for senaite"
```

Backups are stored in `/home/senaite/data/backups`, but system is configured to 
keep the last 5 backups for filestorage, and the last 5 days for blobstorage. 
Hence, is strongly recommend to setup a [rsync][rsync] script in another 
machine to grab the backups from the VM in a regular basis (see section below).

Same procedure as the one explained for zeopack can be used to change the 
periodicity of backups. As an example, to change the periodicity (e.g. twice a
day, at 01:30 pm and at 01:30 am), login as `senaite_daemon` user:

```shell
senaite@senaite:~$ sudo su senaite_daemon
senaite_daemon@senaite:/home/senaite$ crontab -e
```

and edit the cron tab as follows:

```
30 */12 * * * cd /home/senaite/senaite && bin/backup && echo "backup""_success for senaite"
```

To change either the number of days to keep blobs or the number of filestorage
backups to keep, you need to modify `live.cfg` from the buildout directory:

```
[backup]
recipe = collective.recipe.backup
location = ${buildout:backups-dir}/backups
blobbackuplocation = ${buildout:backups-dir}/blobstoragebackups
snapshotlocation = ${buildout:backups-dir}/snapshotbackups
blobsnapshotlocation = ${buildout:backups-dir}/blobstoragesnapshots
datafs = ${buildout:var-dir}/filestorage/Data.fs
blob-storage = ${buildout:var-dir}/blobstorage
keep = 5
keep_blob_days = 5
rsync_options = 
```

and run `bin/buildout -c live.cfg` thereafter.

### Restoring backups

To restore the last available backup, go to buildout's directory (`/home/senaite/senaite/`)
and type `bin/restore`:

```shell
$ cd ~/senaite
$ sudo -u senaite_daemon bin/restore
```

To restore a backup other than the latest available, look first for the 
available backups in the backups directory:

```
senaite@senaite:~$ ls -lh /home/senaite/data/senaite/backups/
total 9.1G
-rw-r--r-- 1 senaite_daemon senaite  106 May 10 02:59 2019-05-10-00-30-03.dat
-rw-r--r-- 1 senaite_daemon senaite 2.9G May 10 02:59 2019-05-10-00-30-03.fsz
-rw-r--r-- 1 senaite_daemon senaite 224M May 10 02:30 2019-05-10-00-30-03.index
-rw-r--r-- 1 senaite_daemon senaite  469 May 19 02:31 2019-05-11-00-30-04.dat
-rw-r--r-- 1 senaite_daemon senaite 1.8G May 11 02:44 2019-05-11-00-30-04.fsz
-rw-r--r-- 1 senaite_daemon senaite 215M May 11 02:30 2019-05-11-00-30-04.index
-rw-r--r-- 1 senaite_daemon senaite 1.1K May 16 02:30 2019-05-16-00-30-45.deltafsz
-rw-r--r-- 1 senaite_daemon senaite 215M May 16 02:30 2019-05-16-00-30-45.index
-rw-r--r-- 1 senaite_daemon senaite 316M May 18 02:33 2019-05-18-00-30-02.deltafsz
-rw-r--r-- 1 senaite_daemon senaite 218M May 18 02:32 2019-05-18-00-30-02.index
-rw-r--r-- 1 senaite_daemon senaite 324M May 19 02:31 2019-05-19-00-30-09.deltafsz
-rw-r--r-- 1 senaite_daemon senaite 218M May 19 02:30 2019-05-19-00-30-09.index
-rw-r--r-- 1 senaite_daemon senaite  106 May 20 02:39 2019-05-20-00-30-03.dat
-rw-r--r-- 1 senaite_daemon senaite 2.5G May 20 02:39 2019-05-20-00-30-03.fsz
-rw-r--r-- 1 senaite_daemon senaite 215M May 20 02:30 2019-05-20-00-30-03.index
```

and append the date of the copy you wish to restore to `bin/restore` command:

```shell
$ cd ~/senaite
$ sudo -u senaite_daemon bin/restore 2019-05-19
```

## Long-term backups

As mentioned above, the Virtual Appliance only stores the last 5 backups and 
5 days of blobs. This allows a rapid recovery of data in case of database 
corruption (e.g., caused by an electricity cut-off): system administrator will 
only need to access to the machine and recover the last backup with a single 
command, as we've seen in the section above.

Nevertheless, is also important to keep backups for long-term. These backups
might be handy, specially in case of severe damage or for when data recovery
is required for forensic analyses and audit.

### Backups in a different disk

Storing backups in a different disk (ideally a RAID1) other than the one where
ZODB is located is strongly recommended, not only for long-term backups, but 
also for daily backups. This approach guarantees the following:

- Only reads are done in the disk where ZODB is installed. Compared to read and
writes, end users of SENAITE won't experience a significant performance decay
while using the system.

- The disk where the backups will be stored is not heavily used compared to the
 disk where ZODB is located. Thus, the probability of disk-failure and data
 loose is much lower.

Nevertheless, keeping disks inside same physical machine does not protect the
data from a disaster involving the whole machine (this can be fire, but can
also be a simple mistake of system administrator while performing maintenance
tasks).

### Backups in a different machine

Keeping backups in a disk from another machine (ideally a dedicated NAS server
with a RAID1 configuration) is the best choice, cause it has the benefits from 
having the backups in a different disk explained above plus less chance of 
data loss because of a disaster involving the machine where SENAITE is
running.

This said, doing a backup will take longer because data transfer between the
source and destination will take place through the network. 

### Use of rsync to automatically grab backups of filestorage

Both strategies explained above can be achieved by using [rsync][rsync], a 
widely used tool for transferring and synchronizing files between servers, 
between a server and an external device, etc.

For instance, the following command will sync filestorage from SENAITE to the 
current folder of the destination machine (from where `rsync` is called):

```bash
$ rsync -av --partial senaite@<senaite_ip>:/home/senaite/data/senaite/backups/* .
```
where `<senaite_ip>` is the **IP of the source** machine

Similar instruction can be used to sync filestorage from SENAITE to a given
folder of the destination machine, but `rsync` called from the source machine
(where SENAITE is installed):

```bash
$ rsync -av --partial /home/senaite/data/senaite/backups/* <user>@<nas_ip>:/home/backups/filestorage/
```
where `<user>` is the username and `<nas_ip>` the **IP of the destination machine**.

Note that access through SSH needs to be granted in both cases.

If the destination machine cannot be accessed through SSH, but is a NAS server
with a shared folder, you can mount that folder in the machine that will run
`rsync` (the one where SENAITE is installed probably). Note that NAS server does
not need to be a Linux machine, can be a Windows system:

```bash
# mount -v -t cifs "//<nas_ip>/<nas_shared_folder>" /mnt/nas -o username=<user>,password=<password>,exec,uid=1000,iocharset=utf8,noperm
```
where:

- `<nas_ip>` is the IP of the NAS server, 
- `<nas_shared_folder>` is the full path of the shared folder
- `<user>` the NAS user
- `<password>` the NAS user's password

You might need to install `cifs-utils` first:

```bash
$ sudo apt-get install cifs-utils
```

Once the unit is mounted, you can use the mounting point instead of SSH url:

```bash
$ rsync -av --partial /home/senaite/data/senaite/backups/* /mnt/nas/fs/
```

Note you might need to create the folder `fs` first in the NAS folder:

```bash
$ mkdir -p /mnt/nas/fs
```

### Use of rsync to automatically grab backups of blobstorage

In the instructions above, we were grabbing the filestorage files from the
folder where the daily backups done by SENAITE take place. We could do the
same for blobstorage, but in this case is recommended to grab directly the
files from the folder where ZODB's blobstorage is located. 

SENAITE's backup machinery follows a logrotate strategy for blob backups. Thus,
each time a backup of blobstorage is done, a new `blobstoragebackups` folder
is created and previous folders are renamed so a suffix with a number is added
(`blobstoragebackups.1`, `blobstoragebackups.2`, etc.) accordingly.

SENAITE does not allow the removal of results reports or any other blob data,
so the pattern in blobstorage will always be additive. Thus, re-copying all
backups is a waste of time and resources. Much better to keep the ZODB's
blobstorage folder in sync:

```bash
$ rsync -av --partial /home/senaite/data/senaite/blobstorage /mnt/nas/blobs/
```


[virtual_appliance]: https://en.wikipedia.org/wiki/Virtual_appliance
[collective.recipe.backup]: https://pypi.org/project/collective.recipe.backup
[plone.recipe.zeoserver]: https://pypi.org/project/plone.recipe.zeoserver/
[cron]: https://en.wikipedia.org/wiki/Cron
[rsync]: https://en.wikipedia.org/wiki/Rsync