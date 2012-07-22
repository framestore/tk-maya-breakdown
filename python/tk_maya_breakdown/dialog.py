"""
Copyright (c) 2012 Shotgun Software, Inc
----------------------------------------------------
"""
import tank
import os
import sys
import threading

from PyQt4 import QtCore, QtGui
from .ui.dialog import Ui_Dialog

class AppDialog(QtGui.QDialog):

    
    def __init__(self, app):
        QtGui.QDialog.__init__(self)
        self._app = app
        # set up the UI
        self.ui = Ui_Dialog() 
        self.ui.setupUi(self)
        
        # set up the browsers
        self.ui.left_browser.set_app(self._app)
        self.ui.right_browser.set_app(self._app)
        self.ui.left_browser.set_label("In your Scene")
        self.ui.right_browser.set_label("Available Versions")
        
        self.ui.left_browser.selection_changed.connect( self.load_versions )
        
        self.ui.chk_green.toggled.connect(self.setup_scene_list)
        self.ui.chk_red.toggled.connect(self.setup_scene_list)
                
        self.ui.right_browser.action_requested.connect( self.update_item )
                
        # load data from shotgun
        self.setup_scene_list()     
        self.ui.right_browser.set_message("Please select an item in the list on the left.")   
        
    ########################################################################################
    # make sure we trap when the dialog is closed so that we can shut down 
    # our threads. Nuke does not do proper cleanup on exit.
    
    def _cleanup(self):
        self.ui.left_browser.destroy()
        self.ui.right_browser.destroy()
        
    def closeEvent(self, event):
        self._cleanup()
        # okay to close!
        event.accept()
        
    def accept(self):
        self._cleanup()
        QtGui.QDialog.accept(self)
        
    def reject(self):
        self._cleanup()
        QtGui.QDialog.reject(self)
        
    def done(self, status):
        self._cleanup()
        QtGui.QDialog.done(self, status)
        
    ########################################################################################
    # basic business logic        
        
    def update_item(self):
            
        curr_selection = self.ui.right_browser.get_selected_item()
        if curr_selection is None:
            return
            
        node_name = curr_selection.data["node_name"]
        node_type = curr_selection.data["node_type"]
        path = curr_selection.data["path"]
        new_version = curr_selection.data["fields"]["version"]
            
        res = QtGui.QMessageBox.question(self,
                                         "Load version?",
                                         "Update the node '%s' to use version %03d?" % (node_name, new_version),
                                         QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel)

        if res == QtGui.QMessageBox.Ok:            
            # call out to hook
            self._app.execute_hook("hook_update", node=node_name, node_type=node_type, new_path=path)
            # finally refresh the UI
            self.setup_scene_list()
    
        
    def setup_scene_list(self): 
        self.ui.left_browser.clear()
        self.ui.right_browser.clear()
        
        d = {}
        
        # now analyze the filters
        if self.ui.chk_green.isChecked() and self.ui.chk_red.isChecked():
            # show everything
            d["show_red"] = True
            d["show_green"] = True
        elif self.ui.chk_green.isChecked() and not self.ui.chk_red.isChecked():
            d["show_red"] = False
            d["show_green"] = True
        elif not self.ui.chk_green.isChecked() and self.ui.chk_red.isChecked():
            d["show_red"] = True
            d["show_green"] = False
        else:
            # show all
            d["show_red"] = True
            d["show_green"] = True
            
        self.ui.left_browser.load(d)

    def load_versions(self): 
        self.ui.right_browser.clear()
        
        curr_selection = self.ui.left_browser.get_selected_item()
        if curr_selection is None:
            return
        
        self.ui.right_browser.load(curr_selection.data)
        
        
        
        