# Copyright (c) 2018-2019 The University of Manchester
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from .file_converter import FileConverter
import datetime
import os
import sys

if 'SPINN_DIRS' in os.environ:
    RANGE_DIR = os.path.join(os.environ['SPINN_DIRS'], "lib")
else:
    RANGE_DIR = "lib"

DICTIONARY_HEADER = "Id,Preface,Original\n" \
                    ",DO NOT EDIT,THIS FILE WAS AUTOGENERATED BY MAKE\n"
SKIPABLE_FILES = ["common.mk", "Makefile.common",
                  "paths.mk", "Makefile.paths",
                  "neural_build.mk", "Makefile.neural_build"]


class Converter(object):
    __slots__ = [
        # Full destination directory
        "_dest",
        # Part of destination directory to replace in when converting paths
        "_dest_basename",
        # File to hold dictionary mappings
        "_dict",
        # Full source directory
        "_src",
        # Part of source directory to take out when converting paths
        "_src_basename"]

    def __init__(self, src, dest, dict_file):
        """ Converts a whole directory including sub directories

        :param src: Full source directory
        :type src: str
        :param dest: Full destination directory
        :type dest: str
        :param dict_file: Full path to dictionary file
        :type dict_file: str
        """
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
        self._src_basename = src_basename
        self._dest_basename = dest_basename
        self._dict = os.path.abspath(dict_file)

    def run(self):
        """ Runs the file converter on a whole directory including sub \
            directories

        WARNING. This code is absolutely not thread safe.
        Interwoven calls even on different FileConverter objects is dangerous!
        It is highly likely that dict files become corrupted and the same
        message_id is used multiple times.

        :return:
        """
        self._mkdir(self._dest)
        message_id = self._get_id()
        for dir_name, _subdir_list, file_list in os.walk(self._src):
            self._mkdir(dir_name)
            for file_name in file_list:
                _, extension = os.path.splitext(file_name)
                source = os.path.join(dir_name, file_name)
                if extension in [".c", ".cpp", ".h"]:
                    destination = self._any_destination(source)
                    message_id = FileConverter.convert(
                        source, destination, self._dict, message_id)
                elif file_name in SKIPABLE_FILES:
                    pass
                else:
                    print("Unexpected file {}".format(source))

    def _get_id(self):
        # Check the dict file exixts.
        if not os.path.exists(self._dict):
            with open(self._dict, 'w') as dict_f:
                dict_f.write(DICTIONARY_HEADER)
        # Added a line saying what you converted
        with open(self._dict, 'a') as dict_f:
            dict_f.write("{},{},{}\n".format(
                self._src.replace(",", ";"), self._dest.replace(",", ";"),
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

        max_id = 0
        with open(self._dict, 'r') as dict_f:
            for line in dict_f:
                parts = line.strip().split(",", 2)
                if len(parts) == 3 and parts[0].isdigit():
                    id = int(parts[0])
                    if id > max_id:
                        max_id = id

        return max_id + 1


    def _any_destination(self, path):
        # Here we need the local separator
        src_bit = os.path.sep + self._src_basename + os.path.sep
        dest_bit = os.path.sep + self._dest_basename + os.path.sep
        li = path.rsplit(src_bit, 1)
        return dest_bit.join(li)

    def _mkdir(self, destination):
        if not os.path.exists(destination):
            os.mkdir(destination)
        if not os.path.exists(destination):
            raise Exception("mkdir failed {}".format(destination))

    def _find_common_based_on_environ(self):
        if 'SPINN_DIRS' not in os.environ:
            return ""
        if 'NEURAL_MODELLING_DIRS' not in os.environ:
            return ""
        return os.path.dirname(os.path.commonprefix(
            [os.environ['SPINN_DIRS'], os.environ['NEURAL_MODELLING_DIRS']]))

    @staticmethod
    def convert(src, dest, dict_file):
        converter = Converter(src, dest, dict_file)
        converter.run()


if __name__ == '__main__':
    src = sys.argv[1]
    dest = sys.argv[2]
    dict_file = sys.argv[3]
    Converter.convert(src, dest, dict_file)
