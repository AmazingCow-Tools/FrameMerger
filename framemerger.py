#!/usr/bin/python
#coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███                                                  ##
##            █ █        █ █        framemerger.py                            ##
##             ████████████         frame-merger                              ##
##           █              █       Copyright (c) 2015 AmazingCow             ##
##          █     █    █     █      www.AmazingCow.com                        ##
##          █     █    █     █                                                ##
##           █              █       N2OMatt - n2omatt@amazingcow.com          ##
##             ████████████         www.amazingcow.com/n2omatt                ##
##                                                                            ##
##                                                                            ##
##                  This software is licensed as GPLv3                        ##
##                 CHECK THE COPYING FILE TO MORE DETAILS                     ##
##                                                                            ##
##    Permission is granted to anyone to use this software for any purpose,   ##
##   including commercial applications, and to alter it and redistribute it   ##
##               freely, subject to the following restrictions:               ##
##                                                                            ##
##     0. You **CANNOT** change the type of the license.                      ##
##     1. The origin of this software must not be misrepresented;             ##
##        you must not claim that you wrote the original software.            ##
##     2. If you use this software in a product, an acknowledgment in the     ##
##        product IS HIGHLY APPRECIATED, both in source and binary forms.     ##
##        (See opensource.AmazingCow.com/acknowledgment.html for details).    ##
##        If you will not acknowledge, just send us a email. We'll be         ##
##        *VERY* happy to see our work being used by other people. :)         ##
##        The email is: acknowledgmentopensource@AmazingCow.com               ##
##     3. Altered source versions must be plainly marked as such,             ##
##        and must notbe misrepresented as being the original software.       ##
##     4. This notice may not be removed or altered from any source           ##
##        distribution.                                                       ##
##     5. Most important, you must have fun. ;)                               ##
##                                                                            ##
##      Visit opensource.amazingcow.com for more open-source projects.        ##
##                                                                            ##
##                                  Enjoy :)                                  ##
##----------------------------------------------------------------------------##

## Imports ##
import os;
import os.path;
import sys;
import getopt;
import termcolor;
#COWTODO: Today we're using pygame to merge the photos.
#COWTODO: But the desired is to use ImageMagick...
import pygame;

################################################################################
## Globals                                                                    ##
################################################################################
class Globals:
    frame_image_path = None;
    images_dir_path  = None;
    output_dir_path  = None;

################################################################################
## Constants                                                                  ##
################################################################################
class Constants:
    #Flag.
    FLAG_HELP             = "h", "help";
    FLAG_VERSION          = "v", "version";
    FLAG_FRAME_IMAGE_PATH = "f", "frame";
    FLAG_IMAGES_DIR_PATH  = "i", "images-dir";
    FLAG_OUTPUT_DIR_PATH  = "o", "output-dir";

    ALL_FLAGS_SHORT = "hvf:i:o:";
    ALL_FLAGS_LONG  = [
        FLAG_HELP            [1],
        FLAG_VERSION         [1],
        FLAG_FRAME_IMAGE_PATH[1] + "=",
        FLAG_IMAGES_DIR_PATH [1] + "=",
        FLAG_OUTPUT_DIR_PATH [1] + "="
    ];

    #Image formats
    IMAGE_FORMATS = [".png", ".jpg", ".jpeg"];

    #App.
    APP_NAME      = "frame-merger";
    APP_VERSION   = "0.1.0";
    APP_AUTHOR    = "N2OMatt <n2omatt@amazingcow.com>"
    APP_COPYRIGHT = "\n".join(("Copyright (c) 2015 - Amazing Cow",
                               "This is a free software (GPLv3) - Share/Hack it",
                               "Check opensource.amazingcow.com for more :)"));


################################################################################
## Color Functions                                                            ##
################################################################################
class C:
    @staticmethod
    def red(msg)    : return termcolor.colored(msg, "red");
    @staticmethod
    def green(msg)  : return termcolor.colored(msg, "green");
    @staticmethod
    def blue(msg)   : return termcolor.colored(msg, "blue");
    @staticmethod
    def magenta(msg): return termcolor.colored(msg, "magenta");
    @staticmethod
    def yellow(msg) : return termcolor.colored(msg, "yellow");


################################################################################
## Print Functions                                                            ##
################################################################################
def print_help():
    #COWTODO: Implement.
    help = """Usage:
  """;
    print help;
    exit(0);

def print_version():
    print "{} - {} - {}".format(Constants.APP_NAME,
                                Constants.APP_VERSION,
                                Constants.APP_AUTHOR);
    print Constants.APP_COPYRIGHT;
    print;
    exit(0);

def print_fatal(msg):
    print C.red("[FATAL]"), msg;
    exit(1);


################################################################################
## Helper Functions                                                           ##
################################################################################
def system_cmd(cmd, expected_ret_val = 0):
    ret = os.system(cmd);
    if(ret != expected_ret_val):
        print_fatal("cmd:", cmd);

def expand_path(path):
    return os.path.abspath(os.path.expanduser(path));

################################################################################
## Processsing                                                                ##
################################################################################
def get_only_image_files():
    #COWTODO: Comment.
    image_filenames = [];

    filenames = os.listdir(Globals.images_dir_path);
    for filename in filenames:
        name, ext = os.path.splitext(filename);
        if(ext in Constants.IMAGE_FORMATS):
            image_filenames.append(filename);

    return image_filenames;

def merge_photo(input_filename, output_filename):
    #COWTODO: Comment.
    try:
        frame_surface = pygame.image.load(Globals.frame_image_path);
        image_surface = pygame.image.load(input_filename);

        image_surface.blit(frame_surface, (0,0));

        pygame.image.save(image_surface, output_filename);

    except Exception, e:
        msg = "{} ({}) - Exception: {}".format("Error while merging photo",
                                               C.blue(input_filename),
                                               str(e))
        print_fatal(msg);


def run():
    #COWTODO: Comment.
    pygame.init();

    image_filenames = get_only_image_files();
    images_count    = len(image_filenames);

    print "Images found: ({})".format(images_count);

    for i in xrange(0, images_count):

        image_filename  = os.path.join(Globals.images_dir_path, image_filenames[i]);
        output_filename = os.path.join(Globals.output_dir_path, image_filenames[i]);

        print "Processing image {} of {}".format(i+1, images_count);
        print "Image Filename : ({})".format(C.yellow(image_filename));
        print "Output Filename: ({})".format(C.green(output_filename));

        merge_photo(image_filename, output_filename);
        print "done...";


################################################################################
## Script Initialization                                                      ##
################################################################################
def main():
    #Get the command line options.
    try:
        options = getopt.gnu_getopt(sys.argv[1:],
                                    Constants.ALL_FLAGS_SHORT,
                                    Constants.ALL_FLAGS_LONG);
    except Exception, e:
        print_fatal(e);

    #Parse the options.
    for option in options[0]:
        key, value = option;
        key = key.lstrip("-");

        #Help/Version.
        if  (key in Constants.FLAG_HELP   ): print_help();
        elif(key in Constants.FLAG_VERSION): print_version();

        #Frame and Images path.
        elif(key in Constants.FLAG_FRAME_IMAGE_PATH):
             Globals.frame_image_path = value;
        elif(key in Constants.FLAG_IMAGES_DIR_PATH):
             Globals.images_dir_path = value;

        #Output path.
        elif(key in Constants.FLAG_OUTPUT_DIR_PATH):
            Globals.output_dir_path = value;


    #COWTODO: Perform sanity check on values.
    Globals.frame_image_path = expand_path(Globals.frame_image_path);
    Globals.images_dir_path  = expand_path(Globals.images_dir_path);
    Globals.output_dir_path  = expand_path(Globals.output_dir_path);

    run();

if(__name__ == "__main__"):
    main();

