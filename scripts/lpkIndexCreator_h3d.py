#!/usr/bin/python
# ================================
# created by Jensenmike, 15:08, 24 March 2015
# https://modosdk.foundry.com/wiki/File:LpkIndexCreator.zip
# modified by Dmytro Holub, 2021-2026
# heap3d@gmail.com
# --------------------------------
# modo python
# create index.xml using modo interface
# ================================
"""
This helps generate the index.xml file you need to unpack a kit using the .lpk installers.
Fill in the Setup Variables below, and the index.xml file will show up in your kit directory.
"""



import os
from typing import Iterable

import lx
import modo


KIT_FOLDER_USERVAL_NAME = 'h3d_lpk_kit_folder'
KIT_NAME_USERVAL_NAME = 'h3d_lpk_kit_name'


def list_files(l_folder):
    """
    Takes a directory to your kit and scans for files to be unpacked by the lpk file
    """
    l_files = []
    for r, d, f in os.walk(l_folder):
        for n in f:
            if '.DS_Store' not in n:
                l_files.append(os.path.join(r, n).replace(l_folder, '').replace('\\', '/'))
    return l_files


def build_index_text(x_name, x_folder, x_files, x_message, x_version):
    """
    Creates a string to be written to the index.xml
    """
    result = '<?xml version="1.0" encoding="utf-8"?>\n<package version="%s">' % x_version  # Headers
    result += ('\n\t<%s name="%s" restart="YES">' % (x_folder, x_name))  # Kit Name and Restart option
    for i in x_files:
        result += ('\n\t\t<source target="%s%s">%s</source>' % (x_name, i, i[1:]))  # Append each file to unpack
    result += ('\n\t</%s>\n\t<message button="Help">%s</message>\n</package>' % (x_folder, x_message))
    return result


def filter_files(x_files: Iterable[str]) -> list[str]:
    """
    Filters out files that are not needed in the index.xml
    """
    result: list[str] = []
    for file in x_files:
        if file.endswith('.lpk'):
            continue
        if '/index.xml' in file:
            continue
        if '/make_lpk.ps1' in file:
            continue
        if '/.git' in file:
            continue

        result.append(file)

    return result


def main():
    kit_folder = lx.eval('user.value {} ?'.format(KIT_FOLDER_USERVAL_NAME))
    if not kit_folder:
        return
    kit_folder_adopted = kit_folder.replace('\\', '/')
    kit_name = lx.eval('user.value {} ?'.format(KIT_NAME_USERVAL_NAME))
    kit_message = '%s Kit installation complete.' % kit_name
    modo_version = "801"
    install_alias = 'kit'

    dir_files = list_files(kit_folder_adopted)
    filtered_files = filter_files(dir_files)

    index = build_index_text(kit_name, install_alias, filtered_files, kit_message, modo_version)
    try:
        wfile = open(os.path.join(kit_folder_adopted, 'index.xml'), 'w+')
    except IOError:
        modo.dialogs.alert(title='index.xml', message='Error creating the file!', dtype='error')
        return
    try:
        wfile.write(index)
    except IOError:
        modo.dialogs.alert(title='index.xml', message='Error writing to file!', dtype='error')
        wfile.close()
        return

    wfile.close()

    modo.dialogs.alert(title='index.xml', message='successfully created', dtype='info')


if __name__ == "__main__":
    main()
