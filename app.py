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
       from tk_maya_breakdown import Breakdown
       
       breakdown = Breakdown(self)
       self.engine.register_command("Breakdown...", breakdown.breakdown)
    
    def destroy_app(self):
        self.engine.log_debug("Destroying tk-maya-breakdown")

