"""
Copyright (c) 2012 Shotgun Software, Inc
----------------------------------------------------
"""

import pymel.core as pm
from pymel.core import Callback

class BreakdownWindow(object):
    def __init__(self, items):
        self._items = items
        self._init_layout()
    
    def on_close(self):
        self._window.delete()
    
    def on_update(self, item):
        item.update_to_latest()
        
        self._body_layout.clear()
        pm.setParent(self._body_layout)
        self._render_items()
    
    def _init_layout(self):
        
        # note! Need to version up the window name whenever the layout changes
        # this is so that Maya can adjust the size properly - otherwise it will
        # use the previous size, which may not be large enough and can be 
        # very confusing for users (buttons no longer visible etc)
        org_window_name = "breakdownWindow"        
        
        # name window breakdownWindow, breakdownWindow1, breakdownWindow2 etc
        window_idx = 0
        window_name = org_window_name
        while pm.window(window_name, exists=True):
            window_idx += 1
            window_name = "%s%d" % (org_window_name, window_idx)
        
        with pm.window(window_name, title="Tank Breakdown", widthHeight=(500, 300)) as self._window:
            with pm.formLayout() as form:
                
                title = pm.text(label=("<b>The list below shows all scene inputs<br>"
                                       "recognized by Tank.</b>"), 
                                align="left")
                
                with pm.scrollLayout(childResizable=True) as body_scroll:
                    with pm.columnLayout(adjustableColumn=True) as self._body_layout:
                        self._render_items()
                
                with pm.rowLayout(numberOfColumns=4, adjustableColumn=1) as button_row:
                    for row_idx in range(1, 6):
                        button_row.rowAttach((row_idx, "both", 0))
                    
                    cb = Callback(self.on_close)
                    self._ok_button = pm.button(label="Close", recomputeSize=False, width=100, command=cb)

                form.attachForm(title, "top", 5)
                form.attachForm(title, "left", 5)
                form.attachForm(title, "right", 5)
                
                form.attachForm(body_scroll, "top", 40)
                form.attachForm(body_scroll, "bottom", 40)
                form.attachForm(body_scroll, "left", 5)
                form.attachForm(body_scroll, "right", 5)
                
                form.attachControl(button_row, "top", 5, body_scroll)
                form.attachForm(button_row, "bottom", 5)
                form.attachForm(button_row, "left", 5)
                form.attachForm(button_row, "right", 5)
    
    def _render_items(self):
        
        if len(self._items) == 0:
            # no items found!
            with pm.rowLayout(numberOfColumns=1, adjustableColumn=1) as item_row:
                item_row.rowAttach((1, "both", 0))                
                
                msg = ("Could not find any references or other inputs<br>"
                       "that Tank recognizes.")
                pm.text(label="<i>%s</i>" % msg)
                    
        
        for item in self._items:
            with pm.rowLayout(numberOfColumns=3, adjustableColumn=2) as item_row:
                for row_idx in range(1, 4):
                    item_row.rowAttach((row_idx, "both", 0))
                
                entity_name = item.entity["name"] if item.entity else "No Entity"
                step_name = item.step["name"] if item.step else "No Step"
                name = "%s (%s, %s)" % (item.name, entity_name, step_name)
                
                pm.text(label=name)
                pm.separator(style="none")
                
                cb = Callback(self.on_update, item)
                pm.button(label="Update", 
                          annotation="A more recent version is available. Click to update.",
                          enable=not item.is_latest_version(), 
                          command=cb)

    

            
        
        
                

        
