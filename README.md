# Frame Merger

**Made with <3 by [Amazing Cow](http://www.amazingcow.com).**



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## Description:

```frame-merger``` - Image merging tool.

```frame-merge``` is a small tool to merge one image (_frame_) into several 
other images located (_source_) in a directory.

The frame image must be a PNG file - (Since the frame "must" support transparency)
but the source images can be any image format supported by 
[pygame](http://www.pygame.org).

The output of ```frame-merge``` is the set of merged images in the specified 
output directory.    
The output format is PNG (default) or JPG (with ```--jpg``` flag).

<br>

As usual, you are **very welcomed** to **share** and **hack** it.


<!-- ####################################################################### -->
<!-- ####################################################################### -->

## Usage:

``` bash
frame-merger [-hv]
frame-merger -f <frame-path> -i <images-path> -o <output-path> --jpg --no-colors
frame-merger --gui [-f <frame-path> -i <images-path> -o <output-path> --jpg]

Options:
 *-h --help    : Show this screen.
 *-v --version : Show app version and copyright.

  -f --frame       <frame-path>  : Path for the frame image.
  -i --images-dir  <images-path> : Path for dir of images that will be merged.
  -o --output-path <output-path> : Path of the output dir.

     --gui       : Run in graphical mode. (If any other flags are given it will
                   loaded in graphical mode too).

     --jpg       : Force all output images to be jpg.
     --no-colors : Disable the colored output.

Notes:
  Options marked with * are exclusive, i.e. the frame-merger will run that
  and exit successfully after the operation.

  In command line mode the [-f -i -o] flags are required.

  In GUI mode the [--no-colors] flag are ignored.

```

### Notes:

  1. ```frame-merger``` doesn't do any attempt to perform validation checks in 
  the size of Frame Image and the Images that will be merged.    
  So  **IS NOT REQUIRED** that them have the same size, but 
  **IF THE SIZE DO NOT MATCH** the merge will be **USELESS** since will be 
  placed into a wrong place. 


  2. Sometimes an image cannot be loaded. This is a bug with pygame we think, 
  because running application again it will load the faulty image correctly.   
  Currently we don't know how to solve this.     
  Sorry :(




<!-- ####################################################################### -->
<!-- ####################################################################### -->

## Install:

Use the Mafefile.

``` bash
    make install
```

Or to uninstall

``` bash
    make uninstall
```



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## Dependencies:

This project uses / depends on:

* Amazing Cow's 
[cowtermcolor](http://www.github.com/AmazingCow/AmazingCore-Libs/cowtermcolor_py)
package to coloring the terminal.

* [pygame](http://www.pygame.org) as a backend to image manipulations.

* [PyQt4](http://www.riverbankcomputing.com/software/pyqt/download) for the 
GUI system.


On debian based systems you can just:

``` bash
  #To install cowtermcolor - Check its repo to other install options too.
  $ wget http://opensource.amazingcow.com/cowtermcolor/dist/latest/install.sh | bash 

  #To install pygame.
  $ sudo apt-get install pygame;

  #To install PyQt4.
  $ sudo apt-get install python-qt4

```

<br>

As convenience we add a ```get_deps.sh``` script to get the dependencies in 
a debian based system. 




<!-- ####################################################################### -->
<!-- ####################################################################### -->

## License:

This software is released under GPLv3.



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## TODO:

Check the TODO file for general things.

This projects uses the COWTODO tags.   
So install [cowtodo](http://www.github.com/AmazingCow-Tools/COWTODO.html) and run:

``` bash
$ cd path/for/the/project
$ cowtodo 
```

That's gonna give you all things to do :D.




<!-- ####################################################################### -->
<!-- ####################################################################### -->

## BUGS:

We strive to make all our code the most bug-free as possible - But we know 
that few of them can pass without we notice ;).

Please if you find any bug report to [bugs_opensource@amazingcow.com]() and/or
create an issue here in Github.




<!-- ####################################################################### -->
<!-- ####################################################################### -->

## Files:

* AUTHORS.txt
* CHANGELOG.txt
* COPYING.txt
* framemerger.py
* get_deps.sh
* Makefile
* OLDREADME.md
* README.md
* TODO.txt




<!-- ####################################################################### -->
<!-- ####################################################################### -->

## Others:
Check our repos and take a look at our [open source site](http://opensource.amazingcow.com).
