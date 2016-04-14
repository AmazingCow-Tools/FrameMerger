##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███        get_deps.sh                               ##
##            █ █        █ █        FrameMerger                               ##
##             ████████████                                                   ##
##           █              █       Copyright (c) 2015, 2016                  ##
##          █     █    █     █      AmazingCow - www.AmazingCow.com           ##
##          █     █    █     █                                                ##
##           █              █       N2OMatt - n2omatt@amazingcow.com          ##
##             ████████████         www.amazingcow.com/n2omatt                ##
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
##        The email is: acknowledgment_opensource@AmazingCow.com              ##
##     3. Altered source versions must be plainly marked as such,             ##
##        and must not be misrepresented as being the original software.      ##
##     4. This notice may not be removed or altered from any source           ##
##        distribution.                                                       ##
##     5. Most important, you must have fun. ;)                               ##
##                                                                            ##
##      Visit opensource.amazingcow.com for more open-source projects.        ##
##                                                                            ##
##                                  Enjoy :)                                  ##
##----------------------------------------------------------------------------##

################################################################################
##  This script checks if the current system has all the dependencies needed  ##
##  to run the frame-merger and tries to install any missing required part.   ##
##                                                                            ##
##              This only works for DEBIAN BASED SYSTEMS                      ##
##             But is very easy to adapt to other systems!                    ##
################################################################################

## Query python about the packages ##
python -c "import cowtermcolor" 2> /dev/null;
HAS_COWTERMCOLOR="$?"

python -c "import pygame" 2> /dev/null;
HAS_PYGAME="$?";

python -c "import PyQt4" 2> /dev/null;
HAS_PYQT="$?";


## If any of them aren't installed, install! ##
## COWTERMCOLOR ##
echo "---------------------------------------------------------------------"
if [ "$HAS_COWTERMCOLOR" != "0" ]; then
    CMD="COWTODO: Implement...."
    echo "Installing cowtermcolor: "
    echo "cmd used: '$CMD'";
    $CMD;
else
    echo "Already have [cowtermcolor] ;D";
fi;


## PYGAME ##
echo "---------------------------------------------------------------------"
if [ "$HAS_PYGAME" != "0" ]; then
    CMD="sudo apt-get install python-pygame";
    echo "Installing pygame: "
    echo "cmd used: '$CMD'";
    $CMD;
else
    echo "Already have [pygame] ;D";
fi;

## PYQT4 ##
echo "---------------------------------------------------------------------"
if [ "$HAS_PYQT" != "0" ]; then
    CMD="sudo apt-get install python-qt4";
    echo "Installing python-qt4: "
    echo "cmd used: '$CMD'";
    $CMD;
else
    echo "Already have [pyqt4] ;D";
fi;

echo "---------------------------------------------------------------------"
echo "Done...";
