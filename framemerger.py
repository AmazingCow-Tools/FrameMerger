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
try:
    from termcolor import colored;
except Exception, e:
    def colored(msg, color):
        return msg;

#COWTODO: Today we're using pygame to merge the photos.
#COWTODO: But the desired is to use ImageMagick...
import pygame;
#For GUI :)
from PyQt4.QtCore import *
from PyQt4.QtGui  import *

################################################################################
## Constants                                                                  ##
################################################################################
class Constants:
    #Flag.
    FLAG_HELP             = "h", "help";
    FLAG_VERSION          = "v", "version";
    FLAG_GUI              = "" , "gui";
    FLAG_FRAME_IMAGE_PATH = "f", "frame";
    FLAG_IMAGES_DIR_PATH  = "i", "images-dir";
    FLAG_OUTPUT_DIR_PATH  = "o", "output-dir";
    FLAG_FORCE_JPG        =  "", "jpg";

    ALL_FLAGS_SHORT = "hvf:i:o:";
    ALL_FLAGS_LONG  = [
        FLAG_HELP            [1],
        FLAG_VERSION         [1],
        FLAG_GUI             [1],
        FLAG_FRAME_IMAGE_PATH[1] + "=",
        FLAG_IMAGES_DIR_PATH [1] + "=",
        FLAG_OUTPUT_DIR_PATH [1] + "=",
        FLAG_FORCE_JPG       [1],
    ];

    #Image formats.
    IMAGE_FORMATS = [".png", ".jpg", ".jpeg"];

    #App.
    APP_NAME      = "frame-merger";
    APP_VERSION   = "0.1.4";
    APP_AUTHOR    = "N2OMatt <n2omatt@amazingcow.com>"
    APP_COPYRIGHT = "\n".join(("Copyright (c) 2015 - Amazing Cow",
                               "This is a free software (GPLv3) - Share/Hack it",
                               "Check opensource.amazingcow.com for more :)"));



################################################################################
## GUI                                                                        ##
################################################################################
class GUI(QWidget):
    ############################################################################
    ## Static Run Method                                                      ##
    ############################################################################
    @staticmethod
    def run():
        app = QApplication(sys.argv);
        gui = GUI();
        gui.show();
        sys.exit(app.exec_())


    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        QWidget.__init__(self);

        #UI Elements.
        #Frame.
        self.__frame_image_label  = None;
        self.__frame_image_text   = None;
        self.__frame_image_button = None;
        #Images Dir.
        self.__images_dir_label  = None;
        self.__images_dir_text   = None;
        self.__images_dir_button = None;
        #Output Dir.
        self.__output_dir_label  = None;
        self.__output_dir_text   = None;
        self.__output_dir_button = None;
        #Merge Button.
        self.__run_button = None;
        #Layout.
        self.__root_layout = None;
        #Merge Progress Dialog.
        self.__progess_dialog = None;

        #The Merge Process object.
        self.__merge_process  = None;

        #Initialize the UI.
        self.init_ui();


    ############################################################################
    ## UI Initializer                                                         ##
    ############################################################################
    def init_ui(self):
        #Set the window properties.
        self.setWindowTitle("{} - {} - {}".format(Constants.APP_NAME,
                                                  Constants.APP_VERSION,
                                                  "Amazing Cow"));
        #Set the window properties.
        self.setGeometry(0, 0, 480, 200);

        #Create the widgets.
        #Frame Image.
        self.__frame_image_label = QLabel("Frame Image Path:");

        self.__frame_image_text = QLineEdit();
        self.__frame_image_text.textChanged.connect(self.__on_text_changed);

        self.__frame_image_button = QPushButton("...");
        self.__frame_image_button.clicked.connect(self.__on_frame_image_button_pressed);

        #Images Dir.
        self.__images_dir_label = QLabel("Images Directory Path:");

        self.__images_dir_text  = QLineEdit();
        self.__images_dir_text.textChanged.connect(self.__on_text_changed);

        self.__images_dir_button = QPushButton("...");
        self.__images_dir_button.clicked.connect(self.__on_images_dir_button_pressed);

        #Output Dir.
        self.__output_dir_label = QLabel("Output Directory Path:");

        self.__output_dir_text  = QLineEdit();
        self.__output_dir_text.textChanged.connect(self.__on_text_changed);

        self.__output_dir_button = QPushButton("...");
        self.__output_dir_button.clicked.connect(self.__on_output_dir_button_pressed);

        #Run Button.
        self.__run_button = QPushButton("Start merge!");
        self.__run_button.setEnabled(False);
        self.__run_button.clicked.connect(self.__on_run_button_pressed);

        #Force JPG checkbox.
        self.__force_jpg_checkbox = QCheckBox("Force save in JPG", self);

        #Create the layout.
        self.__root_layout = QGridLayout(self);

        #Add the widgets to layout.
        #Frame Image.
        self.__root_layout.addWidget(self.__frame_image_label,  1, 1);
        self.__root_layout.addWidget(self.__frame_image_text,   2, 1);
        self.__root_layout.addWidget(self.__frame_image_button, 2, 2);
        #Images Dir.
        self.__root_layout.addWidget(self.__images_dir_label,  3, 1);
        self.__root_layout.addWidget(self.__images_dir_text,   4, 1);
        self.__root_layout.addWidget(self.__images_dir_button, 4, 2);
        #Output Dir.
        self.__root_layout.addWidget(self.__output_dir_label,  5, 1);
        self.__root_layout.addWidget(self.__output_dir_text,   6, 1);
        self.__root_layout.addWidget(self.__output_dir_button, 6, 2);
        #Merge Button.
        self.__root_layout.addWidget(self.__run_button, 7, 1, 2, 1 );
        #Force JPG checkbox.
        self.__root_layout.addWidget(self.__force_jpg_checkbox, 7, 2, 2, 1 );


    ############################################################################
    ## Button Callbacks                                                       ##
    ############################################################################
    def __on_frame_image_button_pressed(self):
        #Create a string with the supported image formats to pass to QFileDialog.
        #The string will have the format of Images Files (*.FMT1 *.FMT2 *.FMTN)
        #This is need to ensure that user will selected a valid image format.
        image_formats_str = "Image Files (*{})".format(" *".join(Constants.IMAGE_FORMATS));
        file_selected = QFileDialog.getOpenFileName(self,
                                                    "Select Frame Image",
                                                    "",
                                                    image_formats_str);

        self.__frame_image_text.setText(file_selected);

    def __on_images_dir_button_pressed(self):
        #The user press the ... button of the Images Dir.
        #Set the Dialog to let user selected a directory that will
        #be used to get the photos list.
        dir_selected = QFileDialog.getExistingDirectory(self,
                                                        "Select Images Directory",
                                                        "",
                                                        QFileDialog.ShowDirsOnly);
        self.__images_dir_text.setText(dir_selected);

    def __on_output_dir_button_pressed(self):
        #The user press the ... button of the Output Dir.
        #Set the Dialog to let user selected a directory that will
        #be used to place the merged photos.
        dir_selected = QFileDialog.getExistingDirectory(self,
                                                        "Select Output Directory",
                                                        "",
                                                        QFileDialog.ShowDirsOnly);
        self.__output_dir_text.setText(dir_selected);

    def __on_run_button_pressed(self):
        #Merge the photos and update the Progress Dialog if needed.
        try:
            self.__create_and_init_merge_process();
            self.__create_and_init_process_dialog();

            #Keep merging the photos and updating the progress interface
            #until all photos are merged or user wants to quit.
            while(self.__merge_process.has_image_to_merge()):
                self.__merge_process.merge();
                index = self.__merge_process.get_current_image_index()
                self.__progress_dialog.setValue(index);

                #User wants to quit.
                if(self.__progress_dialog.wasCanceled()):
                    return;

            #Set the all things are done.
            images_count = self.__merge_process.get_images_count();
            self.__progress_dialog.setValue(images_count);

            #Show to user that processing was complete.
            QMessageBox.information(self,
                                    "Frame Merger",
                                    "Processing complete...",
                                    QMessageBox.Ok);

        #This except block will catch all types of exceptions generated
        #by the try block above and will show them in a "nice" Error Dialog
        #to user.
        except Exception, e:
            QMessageBox.critical(self,
                                 "Frame Merger",
                                 str(e),
                                 QMessageBox.Ok);


    ############################################################################
    ## Text Box Callbacks                                                     ##
    ############################################################################
    def __on_text_changed(self):
        #We only enable the run button if user fills all the text boxes.
        frame_len  = len(self.__frame_image_text.text());
        images_len = len(self.__images_dir_text.text());
        output_len = len(self.__output_dir_text.text());

        all_filled = (frame_len != 0) and (images_len != 0) and (output_len != 0);
        self.__run_button.setEnabled(all_filled);


    ############################################################################
    ## Helper Methods                                                         ##
    ############################################################################
    def __create_and_init_merge_process(self):
        self.__merge_process = MergeProcess();

        self.__merge_process.set_frame_path (str(self.__frame_image_text.text()));
        self.__merge_process.set_images_path(str(self.__images_dir_text.text ()));
        self.__merge_process.set_output_path(str(self.__output_dir_text.text ()));
        self.__merge_process.set_save_in_jpg(self.__force_jpg_checkbox.isChecked());

        self.__merge_process.init();

    def __create_and_init_process_dialog(self):
        self.__progress_dialog = QProgressDialog("Merging Photos",
                                                 "Cancel",
                                                 0,
                                                 self.__merge_process.get_images_count(),
                                                 self);
        self.__progress_dialog.setWindowModality(Qt.WindowModal);


################################################################################
## MergeProcess                                                               ##
################################################################################
class MergeProcess:
    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        self.__frame_path  = None; #Path of the Frame Image.
        self.__images_path = None; #Path of dir that holds the images to be merged.
        self.__output_path = None; #Path of dir that merge images will be placed.

        self.__force_jpg  = False;

        self.__images_filenames     = None; #Will hold only valid image filenames.
        self.__current_photo_index  = 0;

    ############################################################################
    ## Initializer Method                                                     ##
    ############################################################################
    def init(self):
        #We must assure that paths give are valid
        #and that the list of image filenames contains
        #only valid image filenames.
        self.__check_paths();
        self.__clean_images_filenames_list();


    ############################################################################
    ## Setters                                                                ##
    ############################################################################
    def set_frame_path(self, path):
        self.__frame_path = path;

    def set_images_path(self, path):
        self.__images_path = path;

    def set_output_path(self, path):
        self.__output_path = path;

    def set_save_in_jpg(self, b):
        self.__force_jpg = b;

    ############################################################################
    ## Merge Process State Getters                                            ##
    ############################################################################
    def get_images_count(self):
        return len(self.__images_filenames);

    def get_current_image_index(self):
        return self.__current_photo_index;

    def has_image_to_merge(self):
        return self.__current_photo_index < self.get_images_count();


    ############################################################################
    ## Action Method                                                          ##
    ############################################################################
    def merge(self):
        #Grab the name of the current image.
        #Canonize it's path and create the output path based in it's name.
        #Next merge the photo and advance the image index.
        image_filename = self.__images_filenames[self.__current_photo_index];

        image_fullpath  = os.path.join(self.__images_path, image_filename);
        output_fullpath = os.path.join(self.__output_path, image_filename);

        #If is to save in JPG, change the output filename to JPG.
        if(self.__force_jpg):
            output_fullpath = output_fullpath.replace(".png", ".jpg");

        self.__merge_photo(image_fullpath, output_fullpath);

        self.__current_photo_index += 1;

    ############################################################################
    ## Helper Methods                                                         ##
    ############################################################################
    def __check_paths(self):
        #Paths could came with any format, so first we will canonize them.
        #i.e. make them absolute paths. Those method will return a path
        #in it's absolute form or None if an absolute path cannot be formed.

        #Canonize the paths...
        self.__frame_path  = self.__canonize_path(self.__frame_path);
        self.__images_path = self.__canonize_path(self.__images_path);
        self.__output_path = self.__canonize_path(self.__output_path);

        #If any path cannot be formed fail now.
        if(self.__frame_path is None or not os.path.isfile(self.__frame_path)):
            raise Exception("Frame Image Path is not a valid.");

        if(self.__images_path is None or not os.path.isdir(self.__images_path)):
            raise Exception("Images Dir Path is not a valid.");

        if(self.__output_path is None):
            raise Exception("Output Dir Path is not a valid.");

        #An output path can not exists yet so create it now.
        #We're using the mkdir -p to ensure that the full tree
        #is created or if it already exists the call doesn't fail.
        if(os.system("mkdir -p {}".format(self.__output_path)) != 0):
            raise Exception("Output dir path is not valid and cannot be created.");


    def __canonize_path(self, path):
        if(path is None):
            return None;
        return os.path.abspath(os.path.expanduser(path));

    def __clean_images_filenames_list(self):
        clean_filenames = [];

        #Iterate for all files in the images directory and
        #only selects those that is like to be an image.
        #This not means that the file is a valid image, but it
        #will be handled after.
        filenames = os.listdir(self.__images_path);
        for filename in filenames:
            name, ext = os.path.splitext(filename);
            if(ext in Constants.IMAGE_FORMATS):
                clean_filenames.append(filename);

        self.__images_filenames = clean_filenames;


    def __merge_photo(self, input_filename, output_filename):
        #Load both the Frame Image and the Image that will be merged.
        #Merge them an then save the merged image into disk.
        try:
            frame_surface = pygame.image.load(self.__frame_path);
            image_surface = pygame.image.load(input_filename);

            image_surface.blit(frame_surface, (0,0));

            pygame.image.save(image_surface, output_filename);

        #If anything went wrong, so fail now.
        except Exception, e:
            msg = "{} ({}) - Exception: {}".format("Error while merging photo",
                                                   input_filename,
                                                   str(e))
            raise Exception(msg);



################################################################################
## Color Functions                                                            ##
################################################################################
class C:
    @staticmethod
    def red(msg) :
        return colored(msg, "red");
    @staticmethod
    def green(msg) :
        return colored(msg, "green");
    @staticmethod
    def blue(msg) :
        return colored(msg, "blue");
    @staticmethod
    def magenta(msg) :
        return colored(msg, "magenta");
    @staticmethod
    def yellow(msg) :
        return colored(msg, "yellow");


################################################################################
## Print Functions                                                            ##
################################################################################
def print_help():
    help = """Usage:
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

Notes:
  Options marked with * are exclusive, i.e. the frame-merger will run that
  and exit successfully after the operation.

  In command line mode the [-f -i -o] flags are required.
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
def run(frame_path, images_path, output_path, save_in_jpg):
    #Merge all photos.
    try:
        merge_process = MergeProcess();

        merge_process.set_frame_path (frame_path);
        merge_process.set_images_path(images_path);
        merge_process.set_output_path(output_path);
        merge_process.set_save_in_jpg(save_in_jpg);

        merge_process.init();

        print "Images found: {}".format(merge_process.get_images_count());
        while(merge_process.has_image_to_merge()):
            print "{} ({}) of ({})".format("Merging image",
                                            merge_process.get_current_image_index() + 1,
                                            merge_process.get_images_count());
            merge_process.merge();
        print "Done...";

    #This except block will catch all types of exceptions generated
    #by the try block above and will show them in a "nice" error message
    #to user.
    except Exception, e:
        print_fatal(str(e));


################################################################################
## Script Initialization                                                      ##
################################################################################
def main():
    if(len(sys.argv[1:]) == 0):
        print_help();

    #Get the command line options.
    try:
        options = getopt.gnu_getopt(sys.argv[1:],
                                    Constants.ALL_FLAGS_SHORT,
                                    Constants.ALL_FLAGS_LONG);
    except Exception, e:
        print_fatal(e);

    #Vars to hold the values of the non exclusive command line options.
    opt_frame_image_path = None;
    opt_images_dir_path  = None;
    opt_output_dir_path  = None;
    opt_save_in_jpg      = False;

    #Parse the options.
    for option in options[0]:
        key, value = option;
        key = key.lstrip("-");

        #Help/Version. - EXCLUSIVE OPTIONS : Run and quit.
        if  (key in Constants.FLAG_HELP   ): print_help();
        elif(key in Constants.FLAG_VERSION): print_version();

        #GUI - EXCLUSIVE OPTION : Run and quit.
        elif(key in Constants.FLAG_GUI):
            GUI.run();
            exit(0);

        #NON EXCLUSIVE OPTIONS : Grab the info to use later.
        #Frame and Images path.
        elif(key in Constants.FLAG_FRAME_IMAGE_PATH):
             opt_frame_image_path = value;
        elif(key in Constants.FLAG_IMAGES_DIR_PATH):
             opt_images_dir_path = value;
        #Output path.
        elif(key in Constants.FLAG_OUTPUT_DIR_PATH):
            opt_output_dir_path = value;
        #Save in JPG.
        elif(key in Constants.FLAG_FORCE_JPG):
            opt_save_in_jpg = True;


    #Will run in text mode.
    run(opt_frame_image_path,
        opt_images_dir_path,
        opt_output_dir_path,
        opt_save_in_jpg);

if(__name__ == "__main__"):
    main();

