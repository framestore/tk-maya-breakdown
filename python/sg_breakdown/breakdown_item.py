"""
Copyright (c) 2012 Shotgun Software, Inc
----------------------------------------------------
"""

class BreakdownItem(object):
    def __init__(self, app, name, entity, step=None, task=None):
        self._name = name
        self._app = app
        self._entity = entity
        self._step = step
        self._task = task
        
        scene_version = None
        scene_node = None
        ref_type = None
        latest_version = None
        latest_version_path = None
    
    @property
    def name(self):
        return self._name
    
    @property
    def entity(self):
        return self._entity
    
    @property
    def step(self):
        return self._step
    
    def is_latest_version(self):
        return self.latest_version == self.scene_version
    
    def update_to_latest(self):
        params = {}
        params["node"] = self.scene_node
        params["type"] = self.ref_type 
        params["new_path"] = self.latest_version_path
        
        self._app.execute_hook_from_setting("hook_update",
                                            node=self.scene_node, 
                                            node_type=self.ref_type,
                                            new_path=self.latest_version_path)
        
        self.scene_version = self.latest_version
        

    

    