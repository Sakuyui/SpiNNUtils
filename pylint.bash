#!/bin/bash

# Copyright (c) 2024 The University of Manchester
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This bash assumes that SupportScripts has been installed in parallel

# requires the latest pylint and pyenchant
# pip install --upgrade pylint pyenchant

# requires the spelling dicts
# sudo apt-get -o Dpkg::Use-Pty=0 install --fix-missing enchant-2 hunspell hunspell-en-gb

dict=/tmp/dict.txt

cat "../SupportScripts/actions/pylint/default_dict.txt" >$dict
cat ".pylint_dict.txt" >>$dict

pylint --output-format=colorized --disable=R --persistent=no --jobs=1 --rcfile=../SupportScripts/actions/pylint/strict_rcfile --spelling-dict=en_GB --spelling-private-dict-file=$dict	spinn_utilities
