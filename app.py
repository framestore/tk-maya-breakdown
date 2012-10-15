"""
Copyright (c) 2012 Shotgun Software, Inc
----------------------------------------------------

A breakdown app which shows what in the scene is out of date.

"""

from tank.platform import Application

import sys
import os

class MayaBreakdown(Application):
    
    def init_app(self):
        tk_maya_breakdown = self.import_module("tk_maya_breakdown")
        self.app_handler = tk_maya_breakdown.AppHandler(self)
        
        # add stuff to main menu
        self.engine.register_command("Scene Breakdown...", self.app_handler.show_dialog)



