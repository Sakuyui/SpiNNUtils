from .file_convertor import FileConvertor
import os
import math
import shutil
import sys

RANGE_DIR = os.path.join(os.environ['SPINN_DIRS'], "lib")
COMMON_DIR = os.path.dirname(os.path.commonprefix(
    [os.environ['SPINN_DIRS'], os.environ['NEURAL_MODELLING_DIRS']]))


class Convertor(object):
    # __slots__ = [
    #    "_dest", "_dest_basename", "_src", "_src_basename"]

    def __init__(self, src, dest, dict):
        self._src = os.path.abspath(src)
        if not os.path.exists(self._src):
            raise Exception(
                "Unable to locate source directory {}".format(self._src))
        self._dest = os.path.abspath(dest)
        src_root, src_basename = os.path.split(
            os.path.normpath(self._src))
        dest_root, dest_basename = os.path.split(
            os.path.normpath(self._dest))
        if src_root != dest_root:
            # They must be siblings due to text manipulation in makefiles
            raise Exception("src and destination must be siblings")
        else:
            self._root = src_root
        self._src_basename = src_basename
        self._dest_basename = dest_basename
        self._dict = os.path.abspath(dict)

    def run(self):
        self._mkdir(self._dest)
        with open(self._dict, 'w') as dict_f:
            dict_f.write("Id,Preface,Original\n"
                         ",DO NOT EDIT,THIS FILE WAS AUTOGENERATED BY MAKE\n")
        message_id = self._get_id()
        for dirName, subdirList, fileList in os.walk(self._src):
            self._mkdir(dirName)
            for file_name in fileList:
                _, extension = os.path.splitext(file_name)
                source = os.path.join(dirName, file_name)
                if extension in [".c", ".cpp", ".h"]:
                    destination = self._any_destination(source)
                    message_id = FileConvertor.convert(
                        source, destination, self._dict, message_id)
                elif file_name in ["common.mk", "Makefile.common",
                                   "paths.mk", "Makefile.paths",
                                   "neural_build.mk", "Makefile.neural_build"]:
                    pass
                else:
                    print ("Unexpected file {}".format(source))

    def _get_id(self):
        RANGE_PER_DIR = 1000

        rangefile = os.path.join(RANGE_DIR, "log.ranges")
        range_start = 0
        filename = self._dest
        if filename.startswith(COMMON_DIR):
            filename = filename[len(COMMON_DIR)+1:]

        # If the range_file does not exist create it and use range_start
        if not os.path.exists(rangefile):
            with open(rangefile, 'w') as log_ranges_file:
                log_ranges_file.write("AUTOGENERATED DO NOT EDIT\n")
                log_ranges_file.write("{} {}\n".format(
                    range_start, filename))
            return range_start

        # Check if the file is ranged or find highest range so far
        highest_found = range_start
        with open(rangefile, 'r') as log_ranges_file:
            data_lines = iter(log_ranges_file)
            next(data_lines)  # Ignore do not edit
            for line in data_lines:
                parts = line.split(" ", 1)
                if filename.strip() == parts[1].strip():
                    return int(parts[0])
                else:
                    highest_found = max(highest_found, int(parts[0]))

        # Go one step above best found
        new_start = highest_found + RANGE_PER_DIR

        # Append to range file in case rebuilt without clean
        with open(rangefile, 'a') as log_ranges_file:
            log_ranges_file.write("{} {}\n".format(new_start, filename))
        return new_start

    def copy_if_newer(self, src_path):
        destination = self._newer_destination(src_path)
        if destination is None:
            return  # newer so no need to copy
        shutil.copy2(src_path, destination)

    def _any_destination(self, path):
        # Here we need the local seperator
        destination = path.replace(
            os.path.sep + self._src_basename + os.path.sep,
            os.path.sep + self._dest_basename + os.path.sep)
        return destination

    def _newer_destination(self, path):
        destination = self._any_destination(path)
        if not os.path.exists(destination):
            return destination
        # need to floor the time as some copies ignore the partial second
        src_time = math.floor(os.path.getmtime(path))
        dest_time = math.floor(os.path.getmtime(destination))
        if src_time > dest_time:
            return destination
        else:
            # print ("ignoring {}".format(destination))
            return None

    def _mkdir(self, path):
        destination = self._any_destination(path)
        if not os.path.exists(destination):
            os.mkdir(destination, 0755)
        if not os.path.exists(destination):
            raise Exception("mkdir failed {}".format(destination))

    @staticmethod
    def convert(src, dest, dict):
        convertor = Convertor(src, dest, dict)
        convertor.run()


if __name__ == '__main__':
    src = sys.argv[1]
    dest = sys.argv[2]
    dict = sys.argv[3]
    Convertor.convert(src, dest, dict)
