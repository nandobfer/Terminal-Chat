# script to be run the first time before the chat program
# it will install required modules and add local dir to git safe directory list

import os, pathlib

os.system('pip install reqcheq')

import reqcheq

path = pathlib.Path().resolve()
git_config = f'git config --global --add safe.directory {path}'
os.system(git_config)