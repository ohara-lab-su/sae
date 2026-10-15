#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import sys
import optparse
import shlex
import subprocess


def run(command, input=None):
    try:
        proc = subprocess.Popen(
            shlex.split(command),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if input:
            proc.stdin.write(input)
        proc.stdin.close()
        result = proc.stdout.read()
        ret = proc.wait()
        return (ret, result)
    except OSError as e:
        return (e.errno, e.args[1])


def check_datname(suffix1, suffix2):
    from sae.common.paths import FileDiscovery

    try:
        datname1 = FileDiscovery().find_datfile(suffix1)
        try:
            datname2 = FileDiscovery().find_datfile(suffix2)
            if datname1 == datname2:
                datname = datname1
        except:
            sys.exit("STOP: ." + suffix1 + " and ." + suffix2 + "file not found")
    except:
        sys.exit("STOP: ." + suffix1 + " file not found")
    return datname


if __name__ == "__main__":
    dosmain = "DosMain"
    suffix1 = "Dos.val"
    suffix2 = "Dos.vec"
    datname = check_datname(suffix1, suffix2)
    if datname:
        print(datname)
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    options, args = parser.parse_args()
    if options.INPUT:
        datname = options.INPUT
    if len(args) > 0:
        datname = args[0]
    if datname:
        command = (
            dosmain + " " + datname + "." + suffix1 + " " + datname + "." + suffix2
        )
        print(command)
        inline = "1 1"
        ret, result = run(command, inline)
        if ret:
            print("------")
            print(result)
        print("------")
        proc = subprocess.Popen(shlex.split(command))
        proc.communicate()
