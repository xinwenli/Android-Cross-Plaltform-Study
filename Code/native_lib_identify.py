#!/usr/bin/python3
import os
import csv
import sys
import tarfile
from android_cross_platform_identify import *
from subprocess import *

# get current apk file name under current dir
def apk_scan(workdir):
    dir_apk_names = []
    with os.scandir(workdir) as it:
        for entry in it:
            if (
                not entry.name.startswith(".")
                and entry.name.endswith(".apk")
                and entry.is_file()
            ):
                dir_apk_names.append(workdir + os.sep + entry.name)
    it.close()
    return dir_apk_names


# check if apk is decoded before and archived in a tar file.
def apk_tar_decoded(tarname):
    with os.scandir(".") as it:
        for entry in it:
            if (
                not entry.name.startswith(".")
                and entry.name == tarname
                and entry.is_file()
            ):
                return True
    return False


# check decoded tar file type exist
def apk_tar_filetype_exist(tarname, file_extension):
    tar = tarfile.open(tarname)
    file_exist = False
    for tarinfo in tar.getmembers():
        if tarinfo.isfile() and tarinfo.name.endswith(file_extension):
            tar.close()
            return True
    tar.close()
    return False


# check decoded folder exist
def apk_tar_dir_exist(tarname, dirname):
    tar = tarfile.open(tarname)
    file_exist = False
    for tarinfo in tar.getmembers():
        if tarinfo.isdir() and tarinfo.name == dirname:
            tar.close()
            return True
    tar.close()
    return False


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
def apk_decode(dir_apk_name):
    p = Popen(
        "apktool d -r " + dir_apk_name, shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE
    )
    out, errors = p.communicate()
    if errors != b"":
        print(errors)
        p.kill()
        return -1
    p.kill()
    return 0


# add all decoded files into tarfile.
def apk_archive(dirname):
    tarname = dirname + ".tar"
    p = Popen(
        "tar -cvf " + tarname + " " + dirname,
        shell=True,
        stdout=PIPE,
        stdin=PIPE,
        stderr=PIPE,
    )
    out, errors = p.communicate()
    if errors != b'':
        print(errors)
        p.kill()
        return -1
    p.kill()
    return 0


# used to find if System.loadlibrary method called in smali source code.
def smali_check_sysload(smali_path):
    sysloadstr = "Ljava/lang/System;->loadLibrary"
    with open(smali_path, "r") as fp:
        line = fp.readline()
        while line:
            if sysloadstr in line:
                fp.close()
                return True
            line = fp.readline()
        fp.close()
    return False


# walk the apk folder scanning all the smali files. if find System.loadlibrary method called, returned name path immedietly
def apk_lib_load(dirname):
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            if not name.startswith(".") and name.endswith(".smali"):
                smali_path = os.path.join(root, name)
                if smali_check_sysload(smali_path):
                    return True, smali_path
    return False, None


# check the smali file if System.loadlibrary method is called.
def apk_tar_lib_load(tarname):
    tar = tarfile.open(tarname)
    file_exist = False
    for tarinfo in tar.getmembers():
        if tarinfo.isfile() and tarinfo.name.endswith(".smali"):
            tar.extract(tarinfo.name)
            if smali_check_sysload(tarinfo.name):
                tar.close()
                return True, tarinfo.name
    tar.close()
    return False, None


# check the platform with platform lib and class name rule.
def apk_tar_platform_check(tarname):
    tar = tarfile.open(tarname)
    platform_exist = False
    platform_ret = ""
    plat_mono_checked = False
    plat_react_checked = False
    plat_flutter_checked = False
    plat_cordova_checked = False
    plat_capacitor_checked = False
    for tarinfo in tar.getmembers():
        # check if mono app
        app = mono_app_identify.MonoApp(tarinfo.name)
        if app.is_mono_app(tarinfo.name) and not plat_mono_checked:
            platform_exist = True
            plat_mono_checked = True
            platform_ret = platform_ret + app.platform_name
        app = react_app_identify.ReactApp(tarinfo.name)
        if app.is_react_app(tarinfo.name) and not plat_react_checked:
            if platform_exist:
                platform_ret = platform_ret + ", " + app.platform_name
            else:
                platform_ret = platform_ret + app.platform_name
            platform_exist = True
            plat_react_checked = True
        app = flutter_app_identify.FlutterApp(tarinfo.name)
        if app.is_flutter_app(tarinfo.name) and not plat_flutter_checked:
            if platform_exist:
                platform_ret = platform_ret + ", " + app.platform_name
            else:
                platform_ret = platform_ret + app.platform_name
            platform_exist = True
            plat_flutter_checked = True
        app = cordova_app_identify.CordovaApp(tarinfo.name)
        if app.is_cordova_app(tarinfo.name) and not plat_cordova_checked:
            if platform_exist:
                platform_ret = platform_ret + ", " + app.platform_name
            else:
                platform_ret = platform_ret + app.platform_name
            platform_exist = True
            plat_cordova_checked = True
        app = capacitor_app_identify.CapacitorApp(tarinfo.name)
        if app.is_capacitor_app(tarinfo.name) and not plat_capacitor_checked:
            if platform_exist:
                platform_ret = platform_ret + ", " + app.platform_name
            else:
                platform_ret = platform_ret + app.platform_name
            platform_exist = True
            plat_capacitor_checked = True

    tar.close()
    return platform_exist, platform_ret

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
apk_check_res = {}

# check if APK scan dir provided otherwise by default is the current working directory
scan_dir = '.'
out_dir = '.'
script_dir = os.getcwd()
if len(sys.argv) == 2:
    scan_dir = scan_dir_preprocess(sys.argv[1])
    if scan_dir == '':
        exit(1)
    #set output directory name follow scandir name
    scan_dir_splited = scan_dir.split(os.sep)
    out_dir = scan_dir_splited[len(scan_dir_splited)-1]
    if os.path.isdir(out_dir):
        os.chdir(out_dir)
    else:
        os.makedirs(out_dir)
        os.chdir(out_dir)    
elif len(sys.argv) == 3:
    scan_dir = scan_dir_preprocess(sys.argv[1])
    if scan_dir == '':
        exit(1)
    #set output directory name as usr input
    out_dir = sys.argv[2]
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
        os.chdir(out_dir)
    else:
        os.chdir(out_dir)
else:
    print("Please give an input directory name contains APK file")
    print("Usage: python3 native_lib_identify [your APK directory name] (optional)[output directory name]")
    exit(0)

dir_apk_names = apk_scan(scan_dir)

# scanning all apk and save result in apk_check_res
for dir_apk_name in dir_apk_names:
    print("File: " + dir_apk_name)
    dir_apk_splited = dir_apk_name.split(os.sep)
    dirname = os.sep.join(dir_apk_splited[:len(dir_apk_splited)-1])
    apkname = dir_apk_splited[len(dir_apk_splited)-1]
    decode_dirname = apkname[:len(apkname) - 4]
    tarname = apkname[:len(apkname) - 4] + ".tar"
    apk_check_res[apkname] = []

    # check if the file is decoded before
    if apk_tar_decoded(tarname) == False:
        # decode apk file as it's not decoded and skip decode error apk
        if apk_decode(dir_apk_name) != 0:
            apk_check_res[apkname] = ["Error", "Error", "Error"]
            #apk_clean_up(decode_dirname)
            continue
        if apk_archive(decode_dirname) != 0:
            print("Err adding to tar file")
            exit(1)


    # decoded tar file is garanteed available here
    # check so file exsistence in tar file
    so_exsist = apk_tar_filetype_exist(tarname, ".so")
    if so_exsist:
        print("Find so file in " + apkname)
        apk_check_res[apkname].append("True")
    else:
        apk_check_res[apkname].append("False")

    # check library
    lib_load, smali_file = apk_tar_lib_load(tarname)
    if lib_load:
        print(
            "Find System.loadLibrary code in " + apkname + ", locate in " + smali_file
        )
        apk_check_res[apkname].append(smali_file)
    else:
        apk_check_res[apkname].append("N/A")

    # check platform
    platform_detected, platformname = apk_tar_platform_check(tarname)
    if platform_detected:
        print("Platform " + platformname + " detected")
        apk_check_res[apkname].append(platformname)
    else:
        apk_check_res[apkname].append("N/A")

    # do cleanup afterwards
    apk_clean_up(decode_dirname)
    print("")

# export result in apk_check_res to a csv file
if len(apk_check_res) != 0:
    with open("apk_check_res.csv", "w", newline="") as csvfile:
        fieldnames = [
            "Apk name",
            "Native library so file exist",
            "Source file name load library",
            "Platform name",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for apkname in apk_check_res:
            writer.writerow(
                {
                    "Apk name": apkname,
                    "Native library so file exist": apk_check_res[apkname][0],
                    "Source file name load library": apk_check_res[apkname][1],
                    "Platform name": apk_check_res[apkname][2],
                }
            )

exit(0)
