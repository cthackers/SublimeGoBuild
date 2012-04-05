# Go Build

This is a little plugin I've built for myself to help me working with Sublime Text 2 on GO projects. 

Note that this is build especially for Windows users

## How to install

<b>Normal Instalation</b>
Download the [package](https://github.com/cthackers/SublimeGoBuild/zipball/master)

Go to `%APPDATA%\Sublime Text 2\Packages` and extract the archive in a new folder

<b>Install using git</b>
Open up a `cmd`, go to `%APPDATA%\Sublime Text 2\Packages` and type
`git clone git://github.com/cthackers/SublimeGoBuild.git`

<b>Install using Sublime Package Control<b>
Not yet

## How To use
Create and save a new Sublime Text project, then from the Project menu bar select `Create GO Project`. 
It will ask you to give the project a name. This name will be used as your executable output name.
If your project doesn't have the usual structure it will be created. All code should go in the `src` folder

Use:
  * `F5` to run your project 
  * `F7` to build
  * `CTRL + F5` to run tests


You don't need to worry about setting the `GOPATH` variable. It will be automaticall set based on the project of which the file you're editing belongs to.