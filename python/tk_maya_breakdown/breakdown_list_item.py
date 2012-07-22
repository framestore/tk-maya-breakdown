"""
Copyright (c) 2012 Shotgun Software, Inc
----------------------------------------------------
"""
import urlparse
import os
import urllib
import shutil
import sys

from PySide import QtCore, QtGui

from .browser_widget import ListItem


class BreakdownListItem(ListItem):
    
    def __init__(self, app, worker, parent=None):
        ListItem.__init__(self, app, worker, parent)
        self._green_pixmap = QtGui.QPixmap(":/res/green_overlay.png")
        self._red_pixmap = QtGui.QPixmap(":/res/red_overlay.png")

    def calculate_status(self, template, fields, show_red, show_green, entity_dict = None):
        """
        Figure out if this is a red or a green one. Also get thumb if possible
        """
        # we can only process stuff with a version
        if "version" not in fields:
            raise Exception("Fields must have a version!")
        
        # start spinner
        self._timer.start(100)

        # store data
        self._template = template
        self._fields = fields
        self._show_red = show_red
        self._show_green = show_green
        self._sg_data = entity_dict

        # kick off the worker!
        self._worker_uid = self._worker.queue_work(self._calculate_status, {})
        self._worker.work_completed.connect(self._on_worker_task_complete)
        self._worker.work_failure.connect( self._on_worker_failure)
        
    def _calculate_status(self, data):
        """
        The computational payload that downloads thumbnails and figures out the 
        status for this item. This is run in a worker thread.
        """
        # set up the payload
        output = {} 
        
        ########################################################################
        # stage 1: calculate the thumbnail

        # set default
        output["thumbnail"] = ":/res/thumb_empty.png"
        
        # see if we can download a thumbnail
        # thumbnail can be in any of the fields
        # entity.Asset.image
        # entity.Shot.image
        # entity.Scene.image
        # entity.Sequence.image
        if self._sg_data:
             
            thumb_url = None
            if thumb_url is None:
                thumb_url = self._sg_data.get("entity.Asset.image")
            if thumb_url is None:
                thumb_url = self._sg_data.get("entity.Shot.image")
            if thumb_url is None:
                thumb_url = self._sg_data.get("entity.Scene.image")
            if thumb_url is None:
                thumb_url = self._sg_data.get("entity.Sequence.image")
            
            if thumb_url is not None:
                # input is a dict with a url key
                # returns a dict with a  thumb_path key
                ret = self._download_thumbnail({"url": thumb_url})
                if ret:
                    output["thumbnail"] = ret.get("thumb_path")
                
                
        
        ########################################################################
        # stage 2: calculate visibility
        # check if this is the latest item
        
        # note - have to do some tricks here to get sequences and stereo working
        # need to fix this in Tank platform
        
        # get all eyes, all frames and all versions
        # potentially a HUGE glob, so may be really SUPER SLOW...
        # todo: better support for sequence iterations
        all_versions = self._app.tank.paths_from_template(self._template, 
                                                          self._fields, 
                                                          skip_keys=["version", "SEQ", "eye"])
        
        # now look for the highest version number...
        latest_version = 0
        for ver in all_versions:
            fields = self._template.get_fields(ver)
            if fields["version"] > latest_version:
                latest_version = fields["version"]
        
        current_version = self._fields["version"]
        output["up_to_date"] = (latest_version == current_version)
            
        return output
        
    def _on_worker_failure(self, uid, msg):
        
        if self._worker_uid != uid:
            # not our job. ignore
            return

        # finally, turn off progress indication and turn on display
        self._timer.stop()
    
        # show error message
        self._app.log_warning("Worker error: %s" % msg)
        
        
    def _on_worker_task_complete(self, uid, data):
        """
        Called when the computation is complete and we should update widget
        with the result
        """
        if uid != self._worker_uid:
            return
            
        # stop spin
        self._timer.stop()
            
        # set thumbnail        
        self.ui.thumbnail.setPixmap(QtGui.QPixmap(data["thumbnail"]))

        # set overlay - red or green
        # overlay the green or red mask on top of the thumbnail
        if data["up_to_date"]:
            icon = self._green_pixmap
        else:
            icon = self._red_pixmap
        thumb = self.ui.thumbnail.pixmap()
        painter = QtGui.QPainter(thumb)
        painter.drawPixmap(0,0, icon)
        painter.end()
            
        # figure out if this item should be hidden
        if data["up_to_date"] == True and self._show_green == False:
            self.setVisible(False) 
        if data["up_to_date"] == False and self._show_red == False:
            self.setVisible(False)
    