#!/usr/bin/python3
import os
mono_lib_names = [
    "libmono-btls-shared.so",
    "libmono-native.so",
    "libmono-profiler-log.so",
    "libmonodroid.so",
    "libxamarin-app.so",
    "libxamarin-debug-app-helper.so"
]

mono_class_smali_names = [
    "mono.MonoPackageManager_Resources",
    "mono.MonoPackageManager",
    "mono.MonoRuntimeProvider",
    "mono.android",
    "mono.java",
    "mono.javax"
]


class MonoApp:
    platform_name = "Mono"
    def __init__(self, app_name):
        self.mono_app_name = app_name
        self.lib_exist = False
        self.class_exist = False

    def path2classname(self, smali_path):
        return smali_path.replace(os.sep, '.')

    def is_mono_class(self, smali_path):
        if not smali_path.endswith(".smali"):
            return
        package_name = self.path2classname(smali_path)
        if any([classname in package_name for classname in mono_class_smali_names]):
            self.class_exist = True

    def is_mono_lib(self, lib_path):
        if not lib_path.endswith(".so"):
            return
        if any([libname in lib_path for libname in mono_lib_names]):
            self.lib_exist = True
    
    def is_mono_app(self, path):
        self.is_mono_class(path)
        self.is_mono_lib(path)
        return self.class_exist or self.lib_exist
