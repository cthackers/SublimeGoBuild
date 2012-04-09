# Go Build

This is a little plugin I've built for myself to help me working with Sublime Text 2 on GO projects. 


## How to install

<b>Normal Instalation</b><br>
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

<b>Install using Sublime Package Control</b><br>
Not yet

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