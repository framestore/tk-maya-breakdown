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
        self.ui.browser.set_app(self._app)
        self.ui.browser.set_label("Items in your Scene")
        self.ui.browser.enable_multi_select(True)
                
        self.ui.chk_green.toggled.connect(self.setup_scene_list)
        self.ui.chk_red.toggled.connect(self.setup_scene_list)
                
        self.ui.update.clicked.connect(self.update_items)
        self.ui.select_all.clicked.connect(self.select_all)
        
        # load data from shotgun
        self.setup_scene_list()     
           
        
    ########################################################################################
    # make sure we trap when the dialog is closed so that we can shut down 
    # our threads. Nuke does not do proper cleanup on exit.
    
    def _cleanup(self):
        self.ui.browser.destroy()
        
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
        
    def select_all(self):
        for x in self.ui.browser.get_items():
            self.ui.browser.select(x)
        
        
    def update_items(self):
            
        curr_selection = self.ui.browser.get_selected_items()
            
        if len(curr_selection) == 0:
            QtGui.QMessageBox.information(self, "Please select", "Please select items to update!")            
            return
        
        data = []
        for x in curr_selection:
            d = {}
            d["node_name"] = curr_selection.data["node_name"]
            d["node_type"] = curr_selection.data["node_type"] 
            d["path"] = curr_selection.data["path"]
            data.append(d)
            
        res = QtGui.QMessageBox.question(self, "Update?", "Update the selected nodes?",
                                         QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel)

        if res == QtGui.QMessageBox.Ok:            
            # call out to hook
            self._app.execute_hook("hook_update", items=data)
            # finally refresh the UI
            self.setup_scene_list()
    
        
    def setup_scene_list(self): 
        self.ui.browser.clear()
        
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
            
        self.ui.browser.load(d)

        
        
        