#!/usr/bin/python3
import os
react_lib_names = [
    "libreactnativeblob.so",
    "libreactnativejni.so"
]

react_class_smali_names = [
    "com.facebook.react.ReactActivity*",
    "com.facebook.react.ReactApplication",
    "com.facebook.react.ReactDelegate",
    "com.facebook.react.ReactFragment",
    "com.facebook.react.ReactInstanceManager",
    "com.facebook.react.ReactPackage",
    "com.facebook.react"
]

class ReactApp:
    platform_name = "React"
    def __init__(self, app_name):
        self.react_app_name = app_name
        self.lib_exist = False
        self.class_exist = False

    def path2classname(self, smali_path):
        return smali_path.replace(os.sep, '.')

    def is_react_class(self, smali_path):
        if not smali_path.endswith(".smali"):
            return
        package_name = self.path2classname(smali_path)
        if any([classname in package_name for classname in react_class_smali_names]):
            self.class_exist = True

    def is_react_lib(self, lib_path):
        if not lib_path.endswith(".so"):
            return
        if any([libname in lib_path for libname in react_lib_names]):
            self.lib_exist = True
    
    def is_react_app(self, path):
        self.is_react_class(path)
        self.is_react_lib(path)
        return self.class_exist or self.lib_exist