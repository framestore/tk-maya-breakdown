"""
Copyright (c) 2012 Shotgun Software, Inc
----------------------------------------------------
"""

class BreakdownItem(object):
    def __init__(self, app, name, version, context, node, ref_type, latest, latest_path):
        
        self._app = app
        self._name = name
        self._version = version
        self._context = context
        self._node = node
        self._ref_type = ref_type
        self._latest_version = latest
        self._latest_path = latest_path
    
    @property
    def name(self):
        return self._name
    
    @property
    def version(self):
        return self._version

    @property
    def entity(self):
        return self._context.entity
    
    @property
    def step(self):
        return self._context.step
    
    def is_latest_version(self):
        return self._latest_version == self._version
    
    def update_to_latest(self):
        self._app.execute_hook("hook_update",
                                node=self._node, 
                                node_type=self._ref_type,
                                new_path=self._latest_path)
        
        self._version = self._latest_version
        

    

    