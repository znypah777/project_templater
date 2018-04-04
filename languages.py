import abc
import os
import shutil
import re
import git
from typing import List, Dict
class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class LanguageTemplate(metaclass=abc.ABCMeta):

    NEEDED_FILES = {
        ".gitignore": ["*.out", "*.sw*"]
    }

    NEEDED_FOLDERS = {}

    def __init__(self, project_path:str=None):
        self._project_path = project_path

    def create_template(self):
        self._create_folders()
        self._create_files()

    def _create_folders(self):
        for needed_dir, dir_contents in self.NEEDED_FOLDERS.items():
            current_dir_path = os.path.join(self._project_path, needed_dir)
            if not os.path.exists(current_dir_path):
                os.mkdir(current_dir_path)
                for conts in dir_contents:
                    with open(os.path.join(current_dir_path, conts), "w") as cont_file:
                        pass
            else:
                print(f"{BColors.WARNING}{current_dir_path} already exists so skipping it {BColors.ENDC}")

    def _create_files(self):
        for file, contents in self.NEEDED_FILES.items():
            file_path = os.path.join(self._project_path, file)
            if not os.path.exists(file_path):
                with open(file_path, "w") as new_file:
                    for content in contents:
                        new_file.write(content)
                        new_file.write("\n")
            else:
                print(f"{BColors.WARNING}{file_path} already exists so skipping it {BColors.ENDC}")



class _C(LanguageTemplate):
    NEEDED_FILES = {
        ".gitignore": ["*.out", "*.sw*"],
        "Makefile": []
    }
    NEEDED_FOLDERS = {
        "src": ["main.c"],
        "libs": [],
        "includes": []
    }

    def __init__(self,
                 project_path:str=None,
                 local_libs: List[str]=None,
                 remote_libs: List[str]=None):
        super().__init__(project_path)
        self._local_libs = local_libs
        self._remote_libs = remote_libs

    def create_template(self):
        super().create_template()
        if self._local_libs is not None:
            self._add_local_libs()
        if self._remote_libs is not None:
            self._add_remote_libs()

    def _add_remote_libs(self):
        lib_path = lambda new_lib: os.path.join(self._project_path, "libs",new_lib)
        for remote_lib in self._remote_libs:
            lib_name = re.search("/(\w+)(?:\.git)?$",remote_lib)
            if lib_name is not None:
                print(f"{BColors.OKGREEN} cloning  remote {lib_name.group(1)}{BColors.ENDC}")
                lib_name = lib_name.group(1)
                try:
                    git.Repo.clone_from(remote_lib, lib_path(lib_name))
                except:
                    print(f"{BColors.FAIL} {lib_name} already exists and is not an empty directory{BColors.ENDC}")
            else:
                print(f"{BColors.FAIL}{remote_lib}{BColors.ENDC}not a valid git repo")

    def _add_local_libs(self):
        lib_path = lambda new_lib : os.path.join(self._project_path, "libs", new_lib)
        for lib in self._local_libs:
            if not os.path.isdir(lib):
                print(f"{BColors.WARNING}{lib} is not a directory. so we are skipping it{BColors.ENDC}".format(lib=lib))
            else:
                try:
                    shutil.copytree(lib, lib_path(lib.rsplit("/", )[-1]))
                    print(f"{BColors.OKGREEN} cloning local {lib}".format(
                        lib=lib))
                except Exception as e:
                    print(f"{BColors.FAIL}unable to copy {lib}{BColors.FAIL}".format(lib=lib))

class _CPP(_C):
    pass

class _Ruby(LanguageTemplate):
    pass


class _Python(LanguageTemplate):
    pass


def language_factory(lang:str,  options:Dict[str, str]) -> LanguageTemplate:
    if lang == "c":
        lang_template = _C
    elif lang == "c++":
        lang_template = _CPP
    elif lang == "ruby":
        lang_template = _Ruby
    elif lang == "python":
        lang_template = _Python
    else:
        return
    return lang_template(**options)






