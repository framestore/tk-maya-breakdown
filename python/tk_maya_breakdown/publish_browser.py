"""
Copyright (c) 2012 Shotgun Software, Inc
----------------------------------------------------
"""
import tank
import os
import sys
import datetime
import threading 


from PySide import QtCore, QtGui
from .browser_widget import BrowserWidget
from .browser_widget import ListItem
from .browser_widget import ListHeader

class PublishBrowserWidget(BrowserWidget):

    
    def __init__(self, parent=None):
        BrowserWidget.__init__(self, parent)
    
    def get_file_owner(self, path):
        """
        Returns the owner of a file, the way it is stored in the FS.
        Does not work on windows, returns None
        """
        try:
            import pwd # wont work on windows
            owner = pwd.getpwuid(os.stat(path).st_uid).pw_name
            return owner
        except Exception, e:
            return None    
    
    def get_data(self, data):
        
        # get the data
        self._nuke_node = data["node"]
        self._template = data["template"]
        self._curr_fields = data["fields"]
        self._curr_path = self._template.apply_fields(self._curr_fields) 
        
        ###########################################################################
        # Pass 1 - get ALL FILES on disk
        #
        # first get all files on disk with same fields
        # note - this will get all the individual frames
        # and assumes that there is a field named SEQ and one named eye
        all_versions = self._app.tank.paths_from_template(self._template, 
                                                          self._curr_fields, 
                                                          skip_keys=["version", "SEQ", "eye"])
        
        ###########################################################################
        # Pass 2 - group it into "abstract form" with %04d, %V etc.
        #
        # now collapse it down so that there is a single entry per sequence.
        # before collapsing, pick the attributes from these files
        all_sequences = set()
        attributes = {}
        for file in all_versions:
            fields = self._template.get_fields(file)
            fields["SEQ"] = "%04d"
            fields["eye"] = "%V"
            normalized_path = self._template.apply_fields(fields)
            all_sequences.add(normalized_path)
            if normalized_path not in attributes:
                attributes[normalized_path] = {"mtime": os.path.getmtime(file), 
                                               "owner": self.get_file_owner(file)}
        all_sequences = list(all_sequences)

        ###########################################################################
        # Pass 3 - see if they are published in shotgun
        #        
        fields = ["image", "description", "created_by", "created_at"]        
        sg_data = tank.util.find_publish(self._app.tank, all_sequences, fields=fields)

        ###########################################################################
        # Pass 4 - create result data
        #        
        # create dictionary keyed by abstract path
        result = {}
        for path in all_sequences:
            result[path] = {}
            result[path]["node"] = self._nuke_node
            result[path]["path"] = path
            result[path]["fields"] = self._template.get_fields(path)
            # use the stuff we collected based on individual sequence files
            result[path]["mtime"] = attributes.get(path).get("mtime")
            result[path]["owner"] = attributes.get(path).get("owner")
            # shotgun metadata
            if path in sg_data:
                result[path]["sg_data"] = sg_data[path]
            else:
                result[path]["sg_data"] = None

        return result
            
    
    def _render_item(self, data):
        """
        Generate a standard item for a version 
        """
        i = self.add_item(ListItem)
        i.data = data
        
        content = []
        content.append("Version: %03d" % data.get("fields").get("version"))
            
        if data.get("sg_data"):
            sg_data = data.get("sg_data")
            content.append("Created: %s" % sg_data.get("created_at")) 
            content.append("Created By: %s" % sg_data.get("created_by").get("name"))
            content.append("Comments: %s" % sg_data.get("description"))
            if sg_data.get("image"):
                i.set_thumbnail(sg_data.get("image"))
        
        else:
            content.append("Created: %s" % datetime.datetime.fromtimestamp(data["mtime"]))    
            if data.get("owner"):
                content.append("Created By: %s" % data.get("owner"))
        
        i.set_details("<br>".join(content))
        
        

    def process_result(self, result):

        # first display the current item used
        i = self.add_item(ListHeader)
        i.set_title("Version Currently Used")
        curr_item = result.get(self._curr_path)
        if curr_item:
            self._render_item(curr_item)

        # and now show all versions
        i = self.add_item(ListHeader)
        i.set_title("All Available Versions")
        # sort by version number        
        for data_item in sorted(result.values(), key=lambda x:x["fields"]["version"], reverse=True):        
            self._render_item(data_item)

