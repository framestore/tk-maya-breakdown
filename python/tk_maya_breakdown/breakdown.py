"""
Copyright (c) 2012 Shotgun Software, Inc
----------------------------------------------------
"""

import pymel.core as pm

import tank
from tank.errors import TankError

from . import BreakdownItem
from . import BreakdownWindow

class Breakdown(object):
    def __init__(self, app):
        self.app = app
        self._get_templates()
    
    def breakdown(self):
        self.refresh()
        window = BreakdownWindow(self._items)
    
    def refresh(self):
        self._items = []
        
        items = self.app.execute_hook("hook_scan_scene")
        
        for ref in items:
            item = self._get_breakdown_item_from_ref(ref)
            if item:
                self._items.append(item)
    
    def _get_templates(self):
        """
        Loads the templates which denote a publish in the system from the config.
        Any templates which are not recongized or cannot be resolved are ignored.
        """
        self.templates = []
        for tmpl_entry in self.app.get_setting("templates_to_look_for", []):
            tmpl = self.app.get_template_by_name(tmpl_entry)                
            self.templates.append(tmpl)
                                            
    
    def _get_template(self, path):
        for tmpl_entry in self.templates:
            if tmpl_entry.validate(path):
                return tmpl_entry
        
        return None
    
    def _get_breakdown_item_from_ref(self, ref):
        """
        Given a dict with a path and a node key, return
        """
        item = None
        path = ref["path"]
        tmpl_entry = self._get_template(path)
        
        if tmpl_entry:
            fields = tmpl_entry.get_fields(path)
            name = "%s, v%03d" % (fields["name"], fields["version"])
            
            ctx = self.app.tank.context_from_path(path)
            (latest,latest_path) = self._get_latest_version(tmpl_entry, fields)
            
            item = BreakdownItem(self.app, name, ctx.entity, ctx.step, ctx.task)
            item.scene_version = fields["version"]
            item.scene_node = ref["node"]
            item.ref_type = ref["type"]
            item.latest_version = latest
            item.latest_version_path = latest_path
        return item
    
    def _get_latest_version(self, tmpl, fields):
        latest_version = 0
        latest_path = None
        all_versions = self.app.tank.paths_from_template(tmpl, fields, skip_keys="version")
        for ver in all_versions:
            fields = tmpl.get_fields(ver)
            if fields["version"] > latest_version:
                latest_version = fields["version"]
                latest_version_path = ver
        
        return (latest_version,latest_version_path)
        
        
