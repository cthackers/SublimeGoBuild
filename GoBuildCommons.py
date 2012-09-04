import os, sys, glob
import json
import sublime, sublime_plugin
import thread
import subprocess
import functools

def hasValidStructure(project_path):
	if not os.path.exists(os.path.join(project_path, "src")):
		return False
	if not os.path.exists(os.path.join(project_path, "pkg")):
		return False
	if not os.path.exists(os.path.join(project_path, "bin")):
		return False
	return True
 
def createValidStructure(project_path):
	if not os.path.exists(os.path.join(project_path, "src")):
		os.mkdir(os.path.join(project_path, "src"))
	if not os.path.exists(os.path.join(project_path, "pkg")):
		os.mkdir(os.path.join(project_path, "pkg"))
	if not os.path.exists(os.path.join(project_path, "bin")):
		os.mkdir(os.path.join(project_path, "bin"))

	os.mkdir(os.path.join(project_path, "pkg", getArch()))
	os.mkdir(os.path.join(project_path, "bin", getArch()))

def getArch():
    result = ""
    if "windows" in sublime.platform():
        result = "windows_"
    else:
        result = "linux_"
    if sublime.arch() == "x64":
        result += "amd64"
    else:
        result += "386"
    return result

def getProject(filename=""):
	if len(filename) == 0:
		filename = getFileName()

	if len(filename) == 0:
		return (False, False)

	dirname = os.path.dirname(filename)
	if os.path.exists(dirname):
		os.chdir(dirname);
		findings = glob.glob("*.sublime-project")
		if len(findings):
			return (findings[0].replace(".sublime-project", ""), os.path.join(dirname, findings[0]))
		elif os.path.ismount(dirname):
			return (False, False)
		else:
			return getProject(dirname)
	return (False, False)

def isGoProject():
	project_name, project_path = getProject()

	if not project_path:
		return False

	infile = open(project_path, "r")
	project = json.loads(infile.read())

	result = False
	if not "settings" in project:
		result = False
	else:
		if "go_project" in project["settings"]:
			result = True

	infile.close()
	return result

def getFileName():
	win = sublime.active_window()
	if win:
		view = win.active_view()
		if view and view.file_name():
			return view.file_name()
	return ""		

def getView():
	win = sublime.active_window()
	return win.active_view()


def isGoFile(file_name=getFileName()):
	return file_name.endswith(".go")

class ProcessListener(object):
    def on_data(self, proc, data):
        pass

    def on_finished(self, proc):
        pass

class AsyncProcess(object):

    def __init__(self, arg_list, env, listener, path="", shell=False):

        self.listener = listener
        self.killed = False

        startupinfo = None
        if os.name == "nt":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        if path:
            old_path = os.environ["PATH"]
            os.environ["PATH"] = os.path.expandvars(path).encode(sys.getfilesystemencoding())
        proc_env = os.environ.copy()
        proc_env.update(env)
        for k, v in proc_env.iteritems():
            proc_env[k] = os.path.expandvars(v).encode(sys.getfilesystemencoding())

        self.proc = subprocess.Popen(arg_list, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, startupinfo=startupinfo, env=proc_env, shell=shell)

        if path:
            os.environ["PATH"] = old_path
        if self.proc.stdout:
            thread.start_new_thread(self.read_stdout, ())
        if self.proc.stderr:
            thread.start_new_thread(self.read_stderr, ())

    def kill(self):
        if not self.killed:
            self.killed = True
            self.proc.kill()
            self.listener = None

    def poll(self):
        return self.proc.poll() == None

    def read_stdout(self):
        while True:
            data = os.read(self.proc.stdout.fileno(), 2**15)
            if data != "":
                if self.listener:
                    self.listener.on_data(self, data)
            else:
                self.proc.stdout.close()
                if self.listener:
                    self.listener.on_finished(self)
                break

    def read_stderr(self):
        while True:
            data = os.read(self.proc.stderr.fileno(), 2**15)
            if data != "":
                if self.listener:
                    self.listener.on_data(self, data)
            else:
                self.proc.stderr.close()
                break

class ExecCommand(sublime_plugin.WindowCommand, ProcessListener):

    def run(self, cmd = [], file_regex = "", line_regex = "", working_dir = "", encoding = "utf-8", env = {}, quiet = False, kill = False, **kwargs):

        if kill:
            if self.proc:
                self.proc.kill()
                self.proc = None
                self.append_data(None, "[Cancelled]")
            return

        if not hasattr(self, 'output_view'):
            self.output_view = self.window.get_output_panel("exec")

        if (working_dir == "" and self.window.active_view() and self.window.active_view().file_name() != ""):
            working_dir = os.path.dirname(self.window.active_view().file_name())
       
        env["GOPATH"] = working_dir

        self.output_view.settings().set("result_file_regex", file_regex)
        self.output_view.settings().set("result_line_regex", line_regex)
        self.output_view.settings().set("result_base_dir", working_dir)
        self.window.get_output_panel("exec")
        self.encoding = encoding
        self.quiet = quiet
        self.proc = None
        if not self.quiet:
            print "Running " + " ".join(cmd)

        self.window.run_command("show_panel", {"panel": "output.exec"})

        merged_env = env.copy()
        if self.window.active_view():
            user_env = self.window.active_view().settings().get('build_env')
            if user_env:
                merged_env.update(user_env)

        if working_dir != "":
            os.chdir(working_dir)

        err_type = OSError
        if os.name == "nt":
            err_type = WindowsError

        self.append_data(None, "Executing: " + " ".join(cmd) + "\n\n")

        try:
            self.proc = AsyncProcess(cmd, merged_env, self, **kwargs)
        except err_type as e:
            self.append_data(None, str(e) + "\n")
            if not self.quiet:
                self.append_data(None, "[Finished]")

    def is_enabled(self, kill = False):
        if kill:
            return hasattr(self, 'proc') and self.proc and self.proc.poll()
        else:
            return True

    def append_data(self, proc, data):
        if proc != self.proc:
            if proc:
                proc.kill()
            return

        try:
            str = data.decode(self.encoding)
        except:
            str = "[Decode error - output not " + self.encoding + "]"
            proc = None

        str = str.replace('\r\n', '\n').replace('\r', '\n')

        selection_was_at_end = (len(self.output_view.sel()) == 1 and self.output_view.sel()[0] == sublime.Region(self.output_view.size()))
        self.output_view.set_read_only(False)
        edit = self.output_view.begin_edit()
        self.output_view.insert(edit, self.output_view.size(), str)
        if selection_was_at_end:
            self.output_view.show(self.output_view.size())
        self.output_view.end_edit(edit)
        self.output_view.set_read_only(True)

    def finish(self, proc):
        if not self.quiet:
            self.append_data(proc, "\n\n[Finished]")
        if proc != self.proc:
            return

        edit = self.output_view.begin_edit()
        self.output_view.sel().clear()
        self.output_view.sel().add(sublime.Region(0))
        self.output_view.end_edit(edit)

    def on_data(self, proc, data):
        sublime.set_timeout(functools.partial(self.append_data, proc, data), 0)

    def on_finished(self, proc):
        sublime.set_timeout(functools.partial(self.finish, proc), 0)        