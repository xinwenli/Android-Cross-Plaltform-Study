#!/usr/bin/python3
import os
import sys
from subprocess import *

# get current apk file name under current dir
def dir_has_apk(dirname):
    with os.scandir(dirname) as it:
        for entry in it:
            if (
                not entry.name.startswith(".")
                and entry.name.endswith(".apk")
                and entry.is_file()
            ):
                it.close()
                return True
    it.close()
    return False

# scanning for directory have apk files inside and return the directory name
def dir_has_apk_scan(apkdb_dir):
    dir_has_apk_names = []
    for root, dirs, files in os.walk(apkdb_dir, topdown=False):
        for name in dirs:
            if dir_has_apk(os.path.join(root, name)):              
                dir_has_apk_names.append(os.path.join(root, name))
    return dir_has_apk_names

# decode apk using apk tool and check if any exception ocurred, if exception or error occured, return -1 else return 0
def native_dir_identify(dirname, script_dir):
    if not os.path.isfile(script_dir + os.sep + "native_lib_identify.py"):
        print("cannot find native_lib_identify.py please check from https://bitbucket.org/purseclab/android-native-lib-identifier/src/master/Code/")
        return -1
    p = Popen(
        "python3 " + script_dir + os.sep + "native_lib_identify.py " + dirname,
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

def scan_dir_preprocess(usr_input_scandir):
    # check if given dir exsist
    if not os.path.isdir(usr_input_scandir):
        print("cannot find given directory")
        return ''
    # remove extra sep at the end
    scan_dir_splited = usr_input_scandir.split(os.sep)
    if scan_dir_splited[len(scan_dir_splited)-1] == '':
        return os.sep.join(scan_dir_splited[:len(scan_dir_splited)-1])
    else:
        return usr_input_scandir


# main code
apkdb_dir = ''
out_dir = ''
script_dir = os.getcwd()

# check if provided directory exist and save it to the working directory
if len(sys.argv) == 2:
    apkdb_dir = scan_dir_preprocess(sys.argv[1])
    if apkdb_dir == '':
        exit(1)
    apkdb_dir_splited = apkdb_dir.split(os.sep)
    out_dir = apkdb_dir_splited[len(apkdb_dir_splited)-1]
#check if output directory is speficied, otherwise create a new output folder follow by the scanning name
elif len(sys.argv) == 3:
    apkdb_dir = scan_dir_preprocess(sys.argv[1])
    if apkdb_dir == '':
        exit(1)
    out_dir = sys.argv[2]
else:
    print("please provide a database of APK directory")
    print("Usage: python3 apkdb_identify.py [your APK DB directory] (optional)[output directory name]")
    exit(0)

dirnames = dir_has_apk_scan(apkdb_dir)
for dirname in dirnames:
    print("Original APK directory: " + dirname)
    new_dir = script_dir + os.sep + out_dir
    print("Current directory: " + new_dir)
    if not os.path.isdir(new_dir):
        os.makedirs(new_dir)
        os.chdir(new_dir)
    else:
        os.chdir(new_dir)
    if native_dir_identify(dirname, script_dir) != 0:
        exit(1)
    print("")

exit(0)
