#!/usr/bin/env bash
# 
# Copyright (c) 2008 Shotgun Software, Inc
# ----------------------------------------------------

echo "building user interfaces..."
pyuic4 --from-imports dialog.ui > ../python/tk_maya_breakdown/ui/dialog.py

echo "building resources..."
pyrcc4 resources.qrc > ../python/tk_maya_breakdown/ui/resources_rc.py
