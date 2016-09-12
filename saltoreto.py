#!/usr/bin/env python3

import os
import sys
import datetime
import argparse
import subprocess
from io import StringIO

class Snapshotter:

    def __init__(self, args):
        self.volumes = args.volumes
        self.retain_hour = args.retain_hour
        self.dateformat = args.dateformat
        self.slug_prefix = args.slug_prefix
        self.should_verbose = args.verbose

    def go(self):
        for v in self.volumes:
            if v != '/':
                v = v.rstrip('/')
            self.create_snapshot(v)
            self.erase_old_snapshots(v)

    def create_snapshot(self, volume):
        nowstring = datetime.datetime.now().strftime(self.dateformat)
        snapshot = volume+'/'+self.slug_prefix+nowstring

        if (os.path.exists(snapshot)):
            self._error("Cannot create %s. Something is in the way." % (snapshot))
            return

        self._call_process(["btrfs", "subvolume", "snapshot", "-r", volume, snapshot])


    def erase_old_snapshots(self, volume):

        def erase_snapshot(sn):
            self._call_process(["btrfs", "subvolume", "delete", volume+'/'+sn])

        now = datetime.datetime.now()
        minute = now.time().minute
        hour= now.time().hour
        date = now.date()

        lst = os.listdir(volume)

        for snapshot in lst:
            if not snapshot.startswith(self.slug_prefix):
                continue
            sn_timestring = snapshot[snapshot.find('-')+1:]
            try:
                sn_datetime = datetime.datetime.strptime(sn_timestring, "%Y-%m-%dT%H:%M")
            except ValueError as e:
                self._error("Snapshot "+snapshot+" not treated. " + str(e))
                continue

            age = now-sn_datetime

            if (age > datetime.timedelta(hours=1) and sn_datetime.time().minute != 0):
                erase_snapshot(snapshot)

            if (age > datetime.timedelta(hours=24) and sn_datetime.time().hour != self.retain_hour):
                erase_snapshot(snapshot)


    def _call_process(self, cli):
        with subprocess.Popen(cli, stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                              universal_newlines=True) as p:
            err = p.stderr.read().strip()
            out = p.stdout.read().strip()
            if (err != ''):
                self._error(err)
            if (out != ''):
                self._verbose(out)


    def _error(self, s):
        print("EROOR:", s)

    def _verbose(self, s):
        if self.should_verbose:
            print("VERBOSE:", s, ".")


def main():
    parser = argparse.ArgumentParser(
        description="Create automitically readonly snapshot from btrfs volumes."
    )
    parser.add_argument('volumes', help="volumes to snapshot", nargs='+')
    parser.add_argument(
        '-r', '--retain-hour',
        help="Which hourly snapshot should daily remain (default 2)",
        type=int, default=2, dest='retain_hour')
    parser.add_argument(
        '-f', '--date-format',
        help='Date format used for the volume slug (default "%Y-%m-%dT%H:%M")',
        default="%Y-%m-%dT%H:%M", dest='dateformat')
    parser.add_argument(
        '-p', '--prefix',
        help='Prefix por the volume slug (default ".snapshot-")',
        default=".snapshot-", dest='slug_prefix')
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose')

    args = parser.parse_args()

    worker = Snapshotter(args)
    worker.go()

if __name__ == "__main__":
    main()
