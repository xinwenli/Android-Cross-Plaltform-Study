#!/usr/bin/python3
import os
import sys
import csv
from subprocess import *

# for each directory, read the result csv file and get data
def csv_read_data(dirname):
    if not os.path.isfile(dirname + os.sep + "apk_check_res.csv"):
        print("cannot find apk_check_res.csv file with provided directory")
        return None
    csvfile = open(dirname + os.sep + "apk_check_res.csv")
    return csv.DictReader(csvfile)


# get current directory name
def dir_scan():
    dirname = []
    with os.scandir(".") as it:
        for entry in it:
            if not entry.name.startswith(".") and entry.is_dir():
                dirname.append(entry.name)
    it.close()
    return dirname


# init catigory
def apk_catigory_init(cat_dict, catigory_name):
    cat_dict["Category"] = catigory_name
    cat_dict["App number"] = 0
    cat_dict["Native library usage number"] = 0
    cat_dict["Native library usage rate rate"] = 0
    cat_dict["Platform usage number"] = 0
    cat_dict["Platform usage rate rate"] = 0
    cat_dict["Mono usage number"] = 0
    cat_dict["Mono usage rate in all platform"] = 0
    cat_dict["React usage number"] = 0
    cat_dict["React usage rate in all platform"] = 0
    cat_dict["Flutter usage number"] = 0
    cat_dict["Flutter usage rate in all platform"] = 0
    cat_dict["Cordova usage number"] = 0
    cat_dict["Cordova usage rate in all platform"] = 0
    cat_dict["Capacitor usage number"] = 0
    cat_dict["Capacitor usage rate in all platform"] = 0
    return cat_dict


# add up catigorized data
def apk_sum_update(sum_dict, new_cat_data):
    sum_dict["App number"] += new_cat_data["App number"]
    sum_dict["Native library usage number"] += new_cat_data[
        "Native library usage number"
    ]
    if sum_dict["App number"] != 0:
        sum_dict["Native library usage rate rate"] = sum_dict[
            "Native library usage number"
        ] / sum_dict["App number"]
        sum_dict["Platform usage number"] += new_cat_data["Platform usage number"]
        sum_dict["Platform usage rate rate"] = sum_dict[
            "Platform usage number"
        ] / sum_dict["App number"]
    if sum_dict["Platform usage number"] != 0:
        sum_dict["Mono usage number"] += new_cat_data["Mono usage number"]
        sum_dict["Mono usage rate in all platform"] = sum_dict[
            "Mono usage number"
        ] / sum_dict["Platform usage number"]
        sum_dict["React usage number"] += new_cat_data["React usage number"]
        sum_dict["React usage rate in all platform"] = sum_dict[
            "React usage number"
        ] / sum_dict["Platform usage number"]
        sum_dict["Flutter usage number"] += new_cat_data["Flutter usage number"]
        sum_dict["Flutter usage rate in all platform"] = sum_dict[
            "Flutter usage number"
        ] / sum_dict["Platform usage number"]
        sum_dict["Cordova usage number"] += new_cat_data["Cordova usage number"]
        sum_dict["Cordova usage rate in all platform"] = sum_dict[
            "Cordova usage number"
        ] / sum_dict["Platform usage number"]
        sum_dict["Capacitor usage number"] += new_cat_data["Capacitor usage number"]
        sum_dict["Capacitor usage rate in all platform"] = sum_dict[
            "Capacitor usage number"
        ] / sum_dict["Platform usage number"]
    return sum_dict


# summrize the platform find based on catigory
dirnames = dir_scan()
apk_static_res = {}
apk_sum_line = {}
apk_static_res["Total"] = apk_catigory_init(apk_sum_line, "Total")
for dirname in dirnames:
    csvreader = csv_read_data(dirname)
    apk_catigory_res = {}
    apk_catigory_res = apk_catigory_init(apk_catigory_res, dirname)
    for row in csvreader:
        if row["Native library so file exist"] == "Error":
            continue
        apk_catigory_res["App number"] += 1
        if (
            row["Native library so file exist"] == "True"
            and row["Source file name load library"] != "N/A"
        ):
            apk_catigory_res["Native library usage number"] += 1
            apk_catigory_res["Native library usage rate rate"] = (
                apk_catigory_res["Native library usage number"]
                / apk_catigory_res["App number"]
            )
        if row["Platform name"] != "N/A":
            apk_catigory_res["Platform usage number"] += 1
            apk_catigory_res["Platform usage rate rate"] = (
                apk_catigory_res["Platform usage number"]
                / apk_catigory_res["App number"]
            )
            if "Mono" in row["Platform name"]:
                apk_catigory_res["Mono usage number"] += 1
                apk_catigory_res["Mono usage rate in all platform"] = (
                    apk_catigory_res["Mono usage number"]
                    / apk_catigory_res["Platform usage number"]
                )
            if "React" in row["Platform name"]:
                apk_catigory_res["React usage number"] += 1
                apk_catigory_res["React usage rate in all platform"] = (
                    apk_catigory_res["React usage number"]
                    / apk_catigory_res["Platform usage number"]
                )
            if "Flutter" in row["Platform name"]:
                apk_catigory_res["Flutter usage number"] += 1
                apk_catigory_res["Flutter usage rate in all platform"] = (
                    apk_catigory_res["Flutter usage number"]
                    / apk_catigory_res["Platform usage number"]
                )
            if "Cordova" in row["Platform name"]:
                apk_catigory_res["Cordova usage number"] += 1
                apk_catigory_res["Cordova usage rate in all platform"] = (
                    apk_catigory_res["Cordova usage number"]
                    / apk_catigory_res["Platform usage number"]
                )
            if "Capacitor" in row["Platform name"]:
                apk_catigory_res["Capacitor usage number"] += 1
                apk_catigory_res["Capacitor usage rate in all platform"] = (
                    apk_catigory_res["Capacitor usage number"]
                    / apk_catigory_res["Platform usage number"]
                )
    apk_static_res[dirname] = apk_catigory_res
    apk_sum_update(apk_static_res["Total"], apk_catigory_res)


# export result in apk_static_res to a csv file
if len(apk_static_res) != 0:
    with open("apk_statistic_res.csv", "w", newline="") as csvfile:
        fieldnames = [
            "Category",
            "App number",
            "Native library usage number",
            "Native library usage rate rate",
            "Platform usage number",
            "Platform usage rate rate",
            "Mono usage number",
            "Mono usage rate in all platform",
            "React usage number",
            "React usage rate in all platform",
            "Flutter usage number",
            "Flutter usage rate in all platform",
            "Cordova usage number",
            "Cordova usage rate in all platform",
            "Capacitor usage number",
            "Capacitor usage rate in all platform",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for cat_dict_name in apk_static_res:
            writer.writerow(
                {
                    "Category": apk_static_res[cat_dict_name]["Category"],
                    "App number": apk_static_res[cat_dict_name]["App number"],
                    "Native library usage number": apk_static_res[cat_dict_name][
                        "Native library usage number"
                    ],
                    "Native library usage rate rate": apk_static_res[cat_dict_name][
                        "Native library usage rate rate"
                    ],
                    "Platform usage number": apk_static_res[cat_dict_name][
                        "Platform usage number"
                    ],
                    "Platform usage rate rate": apk_static_res[cat_dict_name][
                        "Platform usage rate rate"
                    ],
                    "Mono usage number": apk_static_res[cat_dict_name][
                        "Mono usage number"
                    ],
                    "Mono usage rate in all platform": apk_static_res[cat_dict_name][
                        "Mono usage rate in all platform"
                    ],
                    "React usage number": apk_static_res[cat_dict_name][
                        "React usage number"
                    ],
                    "React usage rate in all platform": apk_static_res[cat_dict_name][
                        "React usage rate in all platform"
                    ],
                    "Flutter usage number": apk_static_res[cat_dict_name][
                        "Flutter usage number"
                    ],
                    "Flutter usage rate in all platform": apk_static_res[cat_dict_name][
                        "Flutter usage rate in all platform"
                    ],
                    "Cordova usage number": apk_static_res[cat_dict_name][
                        "Cordova usage number"
                    ],
                    "Cordova usage rate in all platform": apk_static_res[
                        cat_dict_name
                    ]["Cordova usage rate in all platform"],
                    "Capacitor usage number": apk_static_res[cat_dict_name][
                        "Capacitor usage number"
                    ],
                    "Capacitor usage rate in all platform": apk_static_res[
                        cat_dict_name
                    ]["Capacitor usage rate in all platform"],
                }
            )
exit(0)
