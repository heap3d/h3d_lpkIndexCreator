#!/usr/bin/python
# ================================
# (C)2021 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# set dir for h3d_lpkIndexCreator kit
# ================================

import lx

kit_folder_userval_name = 'h3d_lpk_kit_folder'
kit_name_userval_name = 'h3d_lpk_kit_name'
install_alias_userval_name = 'h3d_lpk_install_alias'

kit_folder_userval = lx.eval('user.value {} ?'.format(kit_folder_userval_name))
if kit_folder_userval == '':
    exit()

kit_name_userval = kit_folder_userval.split('\\')[-1]

lx.eval('user.value {} {}'.format(kit_name_userval_name, kit_name_userval))
