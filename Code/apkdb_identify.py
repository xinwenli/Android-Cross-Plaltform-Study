#!/usr/bin/python3
import os
from subprocess import *

# get current dir name
def dir_scan():
    dir_names = []
    with os.scandir(".") as it:
        for entry in it:
            if not entry.name.startswith(".") and entry.is_dir():
                dir_names.append(entry.name)
    it.close()
    return dir_names


# decode apk using apk tool and check if any exception ocurred, if exception or error occured, return -1 else return 0
def native_dir_identify(dirname):
    if not os.path.isfile("native_lib_identify.py"):
        print("cannot find native_lib_identify.py please check from https://bitbucket.org/purseclab/android-native-lib-identifier/src/master/Code/")
        return -1
    p = Popen(
        "python3 native_lib_identify.py " + dirname,
        shell=True,
        stdout=PIPE,
        stdin=PIPE,
        stderr=PIPE,
    )
    out, errors = p.communicate()
    if errors != b"":
        print(errors)
        p.kill()
        return -1
    if out != b"":
        print(out.decode("latin"))
    p.kill()
    return 0


# main code
dirnames = dir_scan()
for dirname in dirnames:
    print("Current working directory: " + dirname)
    if native_dir_identify(dirname) != 0:
        exit(1)
    print("")

exit(0)
