import sublime, sublime_plugin
import os, glob
import json
from GoBuildCommons import *

class NewGoCommand(sublime_plugin.WindowCommand):
	

	def run(self, type):
		self.file_name = getFileName()

		if isGoProject():
			sublime.error_message("Your project is already a GO project")
			return

		(self.project_name, self.project_path) = getProject()

		if self.project_name:
			self.window.show_input_panel("Project Name: ", self.project_name, self.setName, None, None)
		else:
			sublime.error_message("There is no opened project to convert.\nPlease save your project first")	
	
	def setName(self, name):
		if len(name) == 0:
			return
 
		infile = open(self.project_path, "r+")
		project = json.loads(infile.read())
		if not "settings" in project:
			project["settings"] = {
				"name": name,
				"go_project": True
			}
		else:
			project["settings"]["name"] = name
			project["settings"]["go_project"] = True

		infile.truncate(0)
		infile.seek(0)
		infile.write(json.dumps(project, indent=4))
		infile.close()

		self.checkStructure()

	def checkStructure(self):
		if not hasValidStructure(os.path.dirname(self.project_path)):
			createValidStructure(os.path.dirname(self.project_path))
