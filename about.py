#
# Sublime Text plugin to support Corona Editor
#
# Copyright (c) 2013 Corona Labs Inc. A mobile development software company. All rights reserved.
#
# MIT License - see https://raw.github.com/coronalabs/CoronaSDK-SublimeText/master/LICENSE

import sublime, sublime_plugin
import os.path
import platform
import json
import datetime

try:
  from . import _corona_utils # P3
except:
  import _corona_utils # P2

"""
# This is run by ST3 after the plugins have loaded (and the ST API is ready for calls)
def plugin_loaded():
  corona_utils.Init()

# This fakes the above functionality on ST2.
# It's important that this is called from a module that isn't imported by any other modules or
# the code gets run multiple times in ST2
if corona_utils.SUBLIME_VERSION < 3000:
  corona_utils.Init()
"""

class AboutCoronaEditorCommand(sublime_plugin.WindowCommand):
  _about_info = None
  _dev_about_info = '{"url": "https://www.coronalabs.com/", "version": "<development>", "description": "Corona Editor is the official Corona SDK plugin for Sublime Text"}'

  def run(self):
    self.load_json("package-manifest.json")
    sublime_info = "[Sublime Text " + sublime.version() +"/"+ sublime.channel() +"/"+ sublime.platform() +"/"+ sublime.arch() +"]"
    canary_file = os.path.join(_corona_utils.PACKAGE_DIR, "about.py") if _corona_utils.SUBLIME_VERSION < 3000 else _corona_utils.PACKAGE_DIR
    install_info = "Installed: " + str(datetime.datetime.fromtimestamp(os.path.getmtime(canary_file)))
    sublime.message_dialog("Corona Editor for Sublime Text\n\nVersion: "+ self._about_info['version'] +"\n\n"+ install_info +"\n\n"+ self._about_info['description'] +"\n\n"+ sublime_info)

  # If we're running ST2, load JSON from file
  # else, load JSON from member of package
  def load_json(self, filename):
    if (_corona_utils.SUBLIME_VERSION < 3000):
      file_path = os.path.join(_corona_utils.PACKAGE_DIR, filename)
      try:
        json_data = open(file_path)
        self._about_info = json.load(json_data)
      except:
        self._about_info = json.loads(self._dev_about_info)
      else:
        json_data.close()

    else: # we're on ST3

      try:
        self._about_info = json.loads(sublime.load_resource(_corona_utils.ST_PACKAGE_PATH + filename))
      except:
        self._about_info = json.loads(self._dev_about_info)

    # pprint(self._about_info)
    # print("About: " + str(self._about_info))

