#!/usr/bin/python3
import os
capacitor_lib_names = [
    "assets" + os.sep + "capacitor.config.json"
]

capacitor_class_smali_names = [
    "com.getcapacitor.android",
    "capacitor.android.plugins"
]

class CapacitorApp:
    platform_name = "Capacitor"
    def __init__(self, app_name):
        self.capacitor_app_name = app_name
        self.lib_exist = False
        self.class_exist = False

    def path2classname(self, smali_path):
        return smali_path.replace(os.sep, '.')

    def is_capacitor_class(self, smali_path):
        if not smali_path.endswith(".smali"):
            return
        package_name = self.path2classname(smali_path)
        if any([classname in package_name for classname in capacitor_class_smali_names]):
            self.class_exist = True

    def is_capacitor_lib(self, lib_path):
        if any([libname in lib_path for libname in capacitor_lib_names]):
            self.lib_exist = True
    
    def is_capacitor_app(self, path):
        self.is_capacitor_class(path)
        self.is_capacitor_lib(path)
        return self.class_exist or self.lib_exist