#!/usr/bin/python3
import os
import csv
from subprocess import *

# get current apk file name under current dir


def apk_scan():
    apk_names = []
    with os.scandir('.') as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.name.endswith(".apk") and entry.is_file():
                apk_names.append(entry.name)
    it.close()
    return apk_names

# do the cleanup remove everything from decoded folder and the folder itself


def apk_clean_up(dirname):
    for root, dirs, files in os.walk(dirname, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    try:
        os.rmdir(dirname)
    finally:
        return

# decode apk using apk tool and check if any exception ocurred, if exception or error occured, return -1 else return 0


def apk_decode(apkname):
    p = Popen("apktool d -r " + apkname, shell=True,
              stdout=PIPE, stdin=PIPE, stderr=PIPE)
    out, errors = p.communicate()
    if errors != b'':
        p.kill()
        return -1
    p.kill()
    return 0

# add all decoded files into tarfile.


def apk_archive(dirname):
    tarname = dirname + ".tar"
    p = Popen("tar -cvf " + tarname + ' ' + dirname, shell=True,
              stdout=PIPE, stdin=PIPE, stderr=PIPE)
    out, errors = p.communicate()
    if errors != b'':
        p.kill()
        return -1
    p.kill()
    return 0

# check if current apk file has so lib


def apk_so_check(dirname):
    has_lib = False
    path = os.getcwd()
    os.chdir(path + os.sep + dirname)
    with os.scandir('.') as it:
        for entry in it:
            if entry.name == "lib" and entry.is_dir():
                has_lib = True
    it.close()
    if has_lib == True:
        for root, dirs, files in os.walk("lib", topdown=False):
            for name in files:
                if not name.startswith('.') and name.endswith(".so"):
                    os.chdir("..")
                    return True
    os.chdir("..")
    return False

# used to find if System.loadlibrary method called in smali source code.


def smali_check_sysload(smali_path):
    sysloadstr = "Ljava/lang/System;->loadLibrary"
    with open(smali_path, 'r') as fp:
        line = fp.readline()
        while line:
            if sysloadstr in line:
                fp.close()
                return True
            line = fp.readline()
        fp.close()
    return False

# walk the smali folder scanning all the smali files. if find System.loadlibrary method called, returned name path immedietly


def apk_lib_load(dirname):
    path = os.getcwd()
    os.chdir(path + os.sep + dirname)
    for root, dirs, files in os.walk("smali", topdown=False):
        for name in files:
            if not name.startswith('.') and name.endswith(".smali"):
                smali_path = os.path.join(root, name)
                if smali_check_sysload(smali_path):
                    os.chdir("..")
                    return True, smali_path
    os.chdir("..")
    return False, None


# main code
apk_check_res = {}
apk_names = apk_scan()

# scanning all apk and save result in apk_check_res
for apkname in apk_names:
    print("Current: "+apkname)
    dirname = apkname[:len(apkname)-4]

    # check if the file is decoded before
    #decoded = apk_tar_decode(dirname)

    # decode apk file if it's not decoded and skip decode error apk
    if apk_decode(apkname) != 0:
        apk_check_res[apkname] = ["Error", "Error"]
        apk_clean_up(dirname)
        continue

    # check so file exsistence
    so_exsist = apk_so_check(dirname)
    if so_exsist:
        print("Find so file in " + apkname)
        apk_check_res[apkname] = []
        apk_check_res[apkname].append('True')
    else:
        apk_check_res[apkname] = []
        apk_check_res[apkname].append('False')
        # if so file not find, it's definatly a none-thrid party lib app
        apk_check_res[apkname].append("No match")
        apk_clean_up(dirname)
        continue

    # check library
    lib_load, smali_file = apk_lib_load(dirname)
    if lib_load:
        print("Find System.loadLibrary code in " +
              apkname + ", locate in " + smali_file)
        apk_check_res[apkname].append(smali_file)
    else:
        apk_check_res[apkname].append("No match")

    # do cleanup and archive afterwards
    apk_clean_up(dirname)
    print('')

# export result in apk_check_res to a csv file
if len(apk_check_res) != 0:
    with open('apk_check_res.csv', 'w', newline='') as csvfile:
        fieldnames = ['apk name', 'so file exsist', 'lib load src file']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for apkname in apk_check_res:
            writer.writerow(
                {'apk name': apkname, 'so file exsist': apk_check_res[apkname][0], 'lib load src file': apk_check_res[apkname][1]})

exit(0)
