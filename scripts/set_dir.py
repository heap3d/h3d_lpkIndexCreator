#!/usr/bin/python
# ================================
# (C)2021 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# set dir for h3d_lpkIndexCreator kit
# ================================

import modo
import lx

kit_folder_userval_name = "h3d_lpk_kit_folder"

current_path = lx.eval("user.value {} ?".format(kit_folder_userval_name))

result = modo.dialogs.dirBrowse(title="set kit folder", path=current_path)
if result is not None:
    lx.eval("user.value {} {{{}}}".format(kit_folder_userval_name, result))
    lx.eval("@{scripts/fill_fields.py}")
