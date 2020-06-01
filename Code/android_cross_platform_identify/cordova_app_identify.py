#!/usr/bin/python3
import os
cordova_lib_names = [
    "assets" + os.sep + "www" + os.sep + "cordova-js-src",
    "assets" + os.sep + "www" + os.sep + "css",
    "assets" + os.sep + "www" + os.sep + "js",
    "assets" + os.sep + "www" + os.sep + "ckrdova_plugin.js",
    "assets" + os.sep + "www" + os.sep + "cordova.js",
    "assets" + os.sep + "www" + os.sep + "index.html",
]

cordova_class_smali_names = [
    "org.apache.cordova.engine",
    "org.apache.cordova.whitelist",
    "org.apache.cordova"
]

class CordovaApp:
    platform_name = "Cordova"
    def __init__(self, app_name):
        self.cordova_app_name = app_name
        self.lib_exist = False
        self.class_exist = False

    def path2classname(self, smali_path):
        return smali_path.replace(os.sep, '.')

    def is_cordova_class(self, smali_path):
        if not smali_path.endswith(".smali"):
            return
        package_name = self.path2classname(smali_path)
        if any([classname in package_name for classname in cordova_class_smali_names]):
            self.class_exist = True

    def is_cordova_lib(self, lib_path):
        if any([libname in lib_path for libname in cordova_lib_names]):
            self.lib_exist = True
    
    def is_cordova_app(self, path):
        self.is_cordova_class(path)
        self.is_cordova_lib(path)
        return self.class_exist or self.lib_exist