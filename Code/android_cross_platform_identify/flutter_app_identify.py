#!/usr/bin/python3
import os
flutter_lib_names = [
    "libflutter.so"
]

flutter_class_smali_names = [
    "io.flutter.app",
    "io.flutter.embedding",
    "io.flutter.plugin",
    "io.flutter.view",
    "io.flutter.util",
    "io.flutter"
]

class FlutterApp:
    platform_name = "Flutter"
    def __init__(self, app_name):
        self.flutter_app_name = app_name
        self.lib_exist = False
        self.class_exist = False

    def path2classname(self, smali_path):
        return smali_path.replace(os.sep, '.')

    def is_flutter_class(self, smali_path):
        if not smali_path.endswith(".smali"):
            return
        package_name = self.path2classname(smali_path)
        if any([classname in package_name for classname in flutter_class_smali_names]):
            self.class_exist = True

    def is_flutter_lib(self, lib_path):
        if not lib_path.endswith(".so"):
            return
        if any([libname in lib_path for libname in flutter_lib_names]):
            self.lib_exist = True
    
    def is_flutter_app(self, path):
        self.is_flutter_class(path)
        self.is_flutter_lib(path)
        return self.class_exist or self.lib_exist