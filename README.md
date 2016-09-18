# Saltoreto
Automatic snapshotting tool for btrfs – your safety net

## Idea

*Saltoreto* is the Esperanto word for “safety net”.

### Snapshots of btrfs
btrfs can create *snapshots*. That means, that it can save the current state of
the subvolume without actually copying it. So a snapshot is almost for free in
the moment, when it's created. By the time as files are modified and added it
diverges from its parent volume and takes more space on the disk.


### Using snapshots as a safety net

You can create snapshots – say – every five minutes and have them around on the disk.
If you make a mistake like `rm -rf oldstuff/ *` a second later realize that you
have not only deleted your `oldstuff`, the snapshot from five minutes ago comes
to save you. It's your safety net.


### Safety net as a cron job

This python script is meant to be called by a cron job. It creates a new read only
snapshot of the specified btrfs volumes and deletes old ones. That means it deletes
the ones that are older than one hour except the plain hour ones and deletes the ones
older than one day except the one of a specified hour. So you always have fresh ones
as well as older ones.


### Really deleting files

... well difficult. There are two reasons to really delete a file:

* You need disk space. Well, buy a new harddisk then.
* You really want to destroy the data eternally. Then you probably should destroy your
  harddisk and all the backups. A first step is to have everything encrypted.


## System requirements

A modern Linux system with

* btrfs-tools
* a minimal python3


## Installation

Just put `saltoreto.py` into `$PATH`. It needs root privileges, so maybe
`/usr/local/sbin` is a good place.


## Usage

### Invocation and command line options

Basically you call `saltoreto volume [volume ...]` with `volume` the btrfs
subvolumes you want to have the safety net for. Then it creates a read only
snapshot and deletes the ones older than an hour except the ones of the plain
hour. Furthermore it deletes the ones older than a day except the ones from
`02:00 am`

There are a few command line options:

* `-r RETAIN_HOUR`, `--retain-hour RETAIN_HOUR`: Usually the daily snapshots
  from 02:00 am are retained. By this option you can adjust this hour.
* `-f DATEFORMAT`, `--date-format DATEFORMAT`: The date format, that is used to
  encode the creation date of the snapshot. The default is `%Y-%m-%dT%H:%M`
  which results in `2016-09-16T02:00` for example. Note that you **must not**
  change it, when there are already snapshots on the safety net as these would
  no longer be cleared.
* `-p SLUG_PREFIX, --prefix SLUG_PREFIX`: This is the prefix that determines
  how the snapshots are named. Its default is `.snapshot-` so that with the
  default date format a snapshot would be named like
  `.snapshot-2016-09-16T02:00`. Again don't change it if there are already
  snapshots on your safety net.
* `-e EXCLUDE`, `--exclude EXCLUDE`: By this option you can set a filename that
  is to be excluded from the safety net. Technically that means that any files
  named like this parameter are deleted from the created snapshots. At this
  time you can specify *exactly one* filename. Any files with the *exactly
  same* file name are excluded. Default is `tmp`. Maybe I will sometimes add
  the option to specify several filenames or even a regex.
* `-v`, `--verbose`: Only one verbose level to `stdout`. Errors are reported to
  `stderr` anyway.


### As a cron job

Usually you would setup a cron job to invoke `saltoreto.py`. Therefor put
something like

```
*/5 *   * * * root /usr/local/sbin/saltoreto.py /home /data 2>> /var/log/saltoreto-err.log
```

This creates a new snapshots of `/home` and `/data` every five minutes and
reports errors to `/var/log/saltoreto-err.log`. Adjust the `*/5` to for example
`*/15` to have a new snapshot every fifteen minutes.


### If you've fallen into the safety net ...

If you need to recover from some accidental removal in the main subvolume you
can roll it back manually using the `btrfs` command.

Let's say you want to rollback `.snapshot-2016-09-16T22:20` from `/data`.

First find out which ID your snapshot has.
```
# btrfs subvolume list /data | grep .snapshot-2016-09-16T22:20
ID 5391 gen 97391 top level 5 path .snapshot-2016-09-16T22:20
```

So the ID of your snapshot is 5391. Now you can make this subvolume the
default:

```
# btrfs subvolume set-default 5391 /data
```

Then umount and mount the file system. Now you have your state back read
only. You can make it writable by

```
# btrfs property set /data ro false
```

That's it.


## Limits

Not that the safety net **does not replace a backup**. It does not protect you
whatsoever from a disk crash and further catastrophes like fire, burglary and
so on.
