#!/usr/bin/python
# ================================
# created by Jensenmike, 15:08, 24 March 2015
# https://modosdk.foundry.com/wiki/File:LpkIndexCreator.zip
# modified by Dmytro Holub, 2021
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
import lx
import modo

kit_folder_userval_name = 'h3d_lpk_kit_folder'
kit_name_userval_name = 'h3d_lpk_kit_name'
# install_alias_userval_name = 'h3d_lpk_install_alias'

# Setup Variables for Kit
# kit_folder = '/Users/testing/Documents/MyKit'

kit_folder = lx.eval('user.value {} ?'.format(kit_folder_userval_name))
kit_folder_adopted = kit_folder.replace('\\', '/')
# kit_name = 'MyKit_v1'
kit_name = lx.eval('user.value {} ?'.format(kit_name_userval_name))
kit_message = '%s Kit installation complete.' % kit_name
modo_version = "801"
install_alias = 'kit'
# install_alias = lx.eval('user.value {} ?'.format(install_alias_userval_name))


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


# Main execution
dir_files = list_files(kit_folder_adopted)
index = build_index_text(kit_name, install_alias, dir_files, kit_message, modo_version)
try:
    wfile = open(os.path.join(kit_folder_adopted, 'index.xml'), 'w+')
except IOError:
    modo.dialogs.alert(title='index.xml', message='Error creating the file!', dtype='error')
    exit()
try:
    wfile.write(index)
except IOError:
    modo.dialogs.alert(title='index.xml', message='Error writing to file!', dtype='error')
    wfile.close()
    exit()

wfile.close()

modo.dialogs.alert(title='index.xml', message='successfully created', dtype='info')
