Frame Merger
====
Made with <3 by [Amazing Cow](http://www.amazingcow.com).

## Intro:
In an app named **Photo Totem** that we made for our partners at 
[Imidiar](http://www.imidiar.com/br) 
we have an optimization trade-off that we did.   
The **Photo Totem** hardware is not powerful enough to run the application
at full speed (i.e. +30FPS) and make the image processing at same time.  
So knowing that, you chose to not merge the "Client" frame with the photo
that was taken in real-time but let this operation to be done in a post run time.   
This is inconvenient, but works... So until **Photo Totem** gets a better hardware, 
we cannot do much more to solve this.

This application is the current solution to merge the "Client's" frame.    

The **Frame Merger** offers a command line interface that could be called from 
a shell script and a GUI interface for those that don't want mess with the terminal
 (Despite that is very, very straightforward the usage in shell).

We're now using a back-end based in Pygame to merge the photos since is very common to 
do the merging operation at the same machine that was used to run
the **Photo Totem** and the Pygame package is already installed in those machines 
since the **Photo Totem** requires it.   
But in the future we want to replace this back-end in Pygame with another one
in ImageMagick, since some times the Pygame could not load the image correctly.  
This is a very annoying bug that we cannot discovered the solution yet. :(


The goal is very specific but we hope that you find another good ways to use it.

As usual, you are **very welcomed** to **share** and **hack** it.

## Notes:
1. The program doesn't do any attempt to perform validation checks in the size of  
Frame Image and the Images that will be merged. So **IS NOT REQUIRED** that them have the 
same size, but **IF THE SIZE DO NOT MATCH** the merge will be **USELESS**
since will be placed into a wrong place. 
2. Sometimes an image cannot be loaded. This is a bug with pygame game we think, 
because running application again it will load the faulty image correctly.   
Currently we don't know how to solve this. Sorry :(


## Install:
Use the Makefile (installing by hand is possible, but again why not using the easy solution?)

```
    make install
```

## Usage:

```
  frame-merger [-hv] [-f <frame-path>] [-i <images-path>] [-o <output-path>]
  frame-merger --gui

Options:
 *-h --help    : Show this screen.
 *-v --version : Show app version and copyright.
 *   --gui     : Run in graphical mode.
     
  -f --frame       <frame-path>  : Path for the frame image.
  -i --images-dir  <images-path> : Path for dir of images that will be merged.
  -o --output-path <output-path> : Path of the output dir.
     --jpg                       : Force all output images to be jpg.
```

##### Notes:
  Options marked with * are exclusive, i.e. the ```frame-merger``` will run that
  and exit successfully after the operation.

  In command line mode the [-f -i -o] flags are required.

## License:
This software is released under GPLv3.

## TODO:
Check the TODO file.

## Others:
Check our repos and take a look at our [open source site](http://opensource.amazingcow.com).
