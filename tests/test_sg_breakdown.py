"""
Copyright (c) 2012 Shotgun Software, Inc
----------------------------------------------------
"""
from test_sg_maya import *

class TestSgBreakdown(MayaEngineTestBase):
    def setUp(self):
        super(TestSgBreakdown, self).setUp()
        self.app_name = "sg_breakdown"
        self.app = self.engine.apps.get(self.app_name)

    def test_is_app(self):
        self.assertIsInstance(self.app, tank.system.application.Application)

