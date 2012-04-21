# Go Build

Sublime Go Build is a plugin for Sublime Text 2 that will help you create a Go project structure, and run/build/test your project from withing the editor.

## How to install

<b>Install using Sublime Package Control (recommended)</b><br>
Sublime Package Control allows you to easily install or remove SublimeGoBuild(and many other ST2 packages) from within the editor. It offers automatically updating packages as well so you no longer need to keep track of changes in SublimeGoBuild.

1. Install Sublime Package Control (if you haven't done so already) from http://wbond.net/sublime_packages/package_control . Be sure to restart ST2 to complete the installation.

2. Bring up the command palette (default `ctrl+shift+p` or `cmd+shift+p`) and start typing `Package Control: Install Package` then press return or click on that option to activate it. You will be presented with a new Quick Panel with the list of available packages. Type `Go Build` and press return or on its entry to install SublimeGoBuild. If there is no entry for SublimeGoBuild, you most likely already have it installed.

<b>Manual Instalation</b><br>
Download the [package](https://github.com/cthackers/SublimeGoBuild/zipball/master)<br><br>
* For Windows:<br>
Go to `%APPDATA%\Sublime Text 2\Packages` and extract the archive in a new folder<br>
* For Linux:<br>
Go to `~/.config/Sublime Text 2/Packages` and extract the archive in a new folder

<b>Install using git</b><br>
* For Windows:<br>
Open a `cmd`, go to `%APPDATA%\Sublime Text 2\Packages` and type...<br>
* For Linux:<br>
Open a shell, go to `~/.config/Sublime Text 2/Packages` and type...<br>
<br>
`git clone git://github.com/cthackers/SublimeGoBuild.git`

## How To use
Create and save a new Sublime Text project, then from the Project menu bar select `Create GO Project`. 
It will ask you to give the project a name. This name will be used as your executable output name.
If your project doesn't have the usual structure it will be created. All code should go in the `src` folder

You can edit the project file (.sublime-project) and add a new key at the settings called `main` 

```
	"settings": {
        "go_project": true, 
        "name": "HelloW",
        "main" : "src/main.go"
    }
```

If the project file contains the main setting, then wherever you are in a project, pressing `F5` or `F7` 
will run or build the main file indicated by the setting

Use:<br>
	* `F5` to run your project<br>
	* `F7` to build<br>
	* `CTRL + F5` to run tests<br>


You don't need to worry about setting the `GOPATH` variable. It will be automaticall set based on the project of which the file you're editing belongs to.