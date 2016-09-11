# Saltoreto
Automatic snapshotting tool for btrfs – your safety net

## Idea

*Saltoreto* is the Esperanto word for “savety net”.

### Snapshots of btrfs
btrfs can create *snapshots*. That means, that it can save the current state of
the subvolume without actually copying it. So a snapshot is almost for free in
the moment, when it's created. By the time as files are modified and added it
diverges from its parent volume and takes more space on the disk.


### Using snapshots as a safety net

You can create snapshots – say – every five minutes and have them around. If
you make a mistake like `rm -rf oldstuff/ *` a second later realize that you
have not only deleted your `oldstuff`, the snapshot from five minutes ago comes
to save you. It's your safety net.


## Usage

*to be written*
