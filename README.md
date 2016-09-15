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



## Usage

*to be written*
