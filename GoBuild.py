import sublime, sublime_plugin
import os, glob
import ctypes
from GoBuildCommons import *

MessageBox = ctypes.windll.user32.MessageBoxA

class GoBuildCommand(sublime_plugin.WindowCommand):

	type = "RUN"
	project_name = ""
	project_path = ""
	valid_structure = False

 	def run(self, type="RUN"):
		self.type = type;
		self.file_name = getFileName();
		
		if isGoProject():
			self.executeProject()
		else:
			if isGoFile():
				self.executeFile()
			else:
				sublime.status_message("Cannot " + type.lower() + " a non go file")

	def append_data(self, proc, data):
	
		try:
			str = data.decode("utf8")
		except:
			str = "[Decode error - output not utf8]"
		

		# Normalize newlines, Sublime Text always uses a single \n separator
		# in memory.
		str = str.replace('\r\n', '\n').replace('\r', '\n')

		selection_was_at_end = (len(self.output_view.sel()) == 1 and self.output_view.sel()[0] == sublime.Region(self.output_view.size()))
		self.output_view.set_read_only(False)
		edit = self.output_view.begin_edit()
		self.output_view.insert(edit, self.output_view.size(), str)
		if selection_was_at_end:
			self.output_view.show(self.output_view.size())
		self.output_view.end_edit(edit)
		self.output_view.set_read_only(True)

	def setEnv(self):
		append = ""
		if "GOPATH" in os.environ:
			self.GOPATH = os.environ['GOPATH']
			append = self.GOPATH + ";"
        
		os.environ['GOPATH'] = append + self.project_path
		os.putenv("GOPATH", append + self.project_path)

	def restoreEnv(self):
		if self.GOPATH != "":
			os.environ['GOPATH'] = self.GOPATH
			os.putenv("GOPATH", self.GOPATH)

		self.GOPATH = ""

	def executeFile(self):
		self.output_view = self.window.get_output_panel("exec")
 		self.window.get_output_panel("exec")
 		self.window.run_command("show_panel", {"panel": "output.exec"})
 		import subprocess as sub

		if self.type == "RUN":
			p = sub.Popen("go run " + self.file_name,stdout=sub.PIPE,stderr=sub.PIPE)
		elif self.type == "BUILD":
			p = sub.Popen("go build -x -v " + self.file_name + " -o bin\\" + os.basename(self.file_name),stdout=sub.PIPE,stderr=sub.PIPE)
		elif self.type == "TEST":
			p = sub.Popen("go test " + self.file_name,stdout=sub.PIPE,stderr=sub.PIPE)
		else:
			self.errorMessage("Unknown command: " + self.type)

		output, errors = p.communicate()
		self.append_data(None, output)
		self.append_data(None, errors)

	def executeProject(self):
		self.project_name, self.project_path = getProject()
		base_path = os.path.dirname(self.project_path)

		project_name = self.getProjectName()

		if project_name == "":
			project_name = self.project_name

		sublime.status_message("Building project: " + project_name)

		self.setEnv()

		if self.type == "RUN":
			command = "go run " + self.file_name.replace(os.path.dirname(self.project_path) + "\\", "")
		elif self.type == "BUILD":
			if (hasValidStructure(base_path)):
				if sublime.arch() == "x64":
					output = "bin\\windows_amd64\\" + project_name + ".exe"
				else:
					output = "bin\\windows_386\\" + project_name + ".exe"
			command = "go build -x -v" + " -o " + output + " " + self.file_name.replace(os.path.dirname(self.project_path) + "\\", "")
		elif self.type == "TEST":
			command = "go test " + self.file_name
		else:
			self.errorMessage("Unknown command: " + self.type)
			self.restoreEnv()
			return

		getView().window().run_command("exec", { 'kill': True })
		getView().window().run_command("exec", {
			'shell': True,
			'cmd': [command],
			'working_dir' : os.path.dirname(self.project_path),
			'file_regex': '^(.+\.go):([0-9]+):(?:([0-9]+):)?\s*(.*)',
		})

		self.restoreEnv()

	def getProjectName(self):
		infile = open(self.project_path, "r")
		project = json.loads(infile.read())
		name = project["settings"]["name"]
		infile.close()
		return name

	
