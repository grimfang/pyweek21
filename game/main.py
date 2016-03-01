#!/usr/bin/python
# -*- coding: utf-8 -*-

# Python imports
import __builtin__
import sys
import os
import logging
import gettext

# Panda3D imoprts
from direct.showbase.ShowBase import ShowBase
from direct.fsm.FSM import FSM
from panda3d.core import (
    AntialiasAttrib,
    ConfigPageManager,
    ConfigVariableBool,
    OFileStream,
    WindowProperties,
    loadPrcFileData,
    loadPrcFile,
    MultiplexStream,
    Notify,
    Filename,
    VirtualFileSystem,
    CollisionTraverser,
    AudioSound,)

from panda3d.physics import (
    ForceNode,
    LinearVectorForce,)

# Game imports
from core import helper
from gui.mainmenu import Mainmenu
from gui.optionsmenu import Optionsmenu
from world import World

__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

#
# PATHS AND CONFIGS
#
# set the application Name
__builtin__.companyName = "Grimfang Studio"
__builtin__.appName = "Little Drop"
__builtin__.versionstring = "16.02"
home = os.path.expanduser("~")
__builtin__.basedir = os.path.join(
    home,
    __builtin__.companyName,
    __builtin__.appName)
__builtin__.rootdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(__builtin__.rootdir)
if not os.path.exists(__builtin__.basedir):
    os.makedirs(__builtin__.basedir)
prcFile = os.path.join(__builtin__.basedir, "%s.prc"%__builtin__.appName)
if os.path.exists(prcFile):
    mainConfig = loadPrcFile(Filename.fromOsSpecific(prcFile))
loadPrcFileData("",
"""
    window-title %s
    cursor-hidden 0
    notify-timestamp 1
    #show-frame-rate-meter 1
    model-path $MAIN_DIR/assets/
    framebuffer-multisample 1
    texture-anisotropic-degree 0
"""%__builtin__.appName)
vfs = VirtualFileSystem.getGlobalPtr()
vfs.mount(
    Filename(os.path.join(__builtin__.rootdir, "assets")),
    ".",
    VirtualFileSystem.MFReadOnly
)
gettext.bindtextdomain(__builtin__.appName, "localedir")
gettext.textdomain(__builtin__.appName)
__builtin__._ = gettext.lgettext
#
# PATHS AND CONFIGS END
#

#
# LOGGING
#
# setup Logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s",
    filename=os.path.join(__builtin__.basedir, "game.log"),
    datefmt="%d-%m-%Y %H:%M:%S",
    filemode="w")

# First log entry, the program version
logging.info("Version %s" % __builtin__.versionstring)

# redirect the notify output to a log file
nout = MultiplexStream()
Notify.ptr().setOstreamPtr(nout, 0)
nout.addFile(Filename(os.path.join(__builtin__.basedir, "game_p3d.log")))
#
# LOGGING END
#

class Main(ShowBase, FSM):
    """Main function of the application
    initialise the engine (ShowBase)"""

    def __init__(self):
        """initialise the engine"""
        ShowBase.__init__(self)
        FSM.__init__(self, "FSM-Game")

        #
        # BASIC APPLICATION CONFIGURATIONS
        #
        # disable pandas default camera driver
        self.disableMouse()
        helper.show_cursor()
        # set background color to black
        self.setBackgroundColor(0, 0, 0)
        # set antialias for the complete sceen to automatic
        self.render.setAntialias(AntialiasAttrib.MAuto)

        #
        # CONFIGURATION LOADING
        #
        # load given variables or set defaults
        # check if audio should be muted
        mute = ConfigVariableBool("audio-mute", False).getValue()
        if mute:
            self.disableAllAudio()
        else:
            self.enableAllAudio()

        def setFullscreen():
            """Helper function to set the window fullscreen
            with width and height set to the screens size"""
            # get the displays width and height
            w = self.pipe.getDisplayWidth()
            h = self.pipe.getDisplayHeight()
            # set window properties
            # clear all properties not previously set
            base.win.clearRejectedProperties()
            # setup new window properties
            props = WindowProperties()
            # Fullscreen
            props.setFullscreen(True)
            # set the window size to the screen resolution
            props.setSize(w, h)
            # request the new properties
            base.win.requestProperties(props)

        # check if the config file hasn't been created
        if not os.path.exists(prcFile):
            setFullscreen()
        elif base.appRunner:
            # When the application is started as appRunner instance, it
            # doesn't respect our loadPrcFiles configurations specific
            # to the window as the window is already created, hence we
            # need to manually set them here.
            for dec in range(mainConfig.getNumDeclarations()):
                # check if we have the fullscreen variable
                if mainConfig.getVariableName(dec) == "fullscreen":
                    setFullscreen()
        # automatically safe configuration at application exit
        base.exitFunc = self.__writeConfig

        # due to the delayed window resizing and switch to fullscreen
        # we wait some time until everything is set so we can savely
        # proceed with other setups like the menus
        if base.appRunner:
            # this behaviour only happens if run from p3d files and
            # hence the appRunner is enabled
            taskMgr.doMethodLater(0.5, self.postInit,
                "post initialization", extraArgs=[])
        else:
            self.postInit()

    def postInit(self):
        #
        # initialize game content
        #

        # Menus
        self.mainmenu = Mainmenu()
        self.optionsmenu = Optionsmenu()

        # collision setup
        base.cTrav = CollisionTraverser("base collision traverser")
        base.cTrav.setRespectPrevTransform(True)
        # setup default physics
        base.enableParticles()

        self.music_menu = loader.loadMusic("music/menu.ogg")
        self.music_menu.setLoop(True)
        self.music_game = loader.loadMusic("music/game.ogg")
        self.music_game.setLoop(True)

        #
        # Event handling
        #
        self.accept("escape", self.__escape)
        # accept menu events
        self.accept("menu_start", self.request, ["Game"])
        self.accept("menu_options", self.request, ["Options"])
        self.accept("menu_quit", self.quit)
        self.accept("options_back", self.request, ["Menu"])

        #
        # Start with the menu
        #
        self.request("Menu")

    #
    # FSM PART
    #

    def enterMenu(self):
        """Enter the main menu state"""
        self.mainmenu.show()
        if self.music_menu.status() != AudioSound.PLAYING:
            self.music_menu.play()

    def exitMenu(self):
        """Leave the main menu state"""
        self.mainmenu.hide()


    def enterOptions(self):
        """Enter the options menu state"""
        self.optionsmenu.show()

    def exitOptions(self):
        """Leave the options menu state"""
        self.optionsmenu.hide()

    def enterGame(self):
        # main game code should be called here
        print _("Enter Game")
        helper.hide_cursor()
        self.music_menu.stop()
        self.music_game.play()
        self.world = World()
        self.world.start()

    def exitGame(self):
        # cleanup for game code
        print _("Exit Game")
        helper.show_cursor()
        self.world.stop()
        del self.world

    #
    # FSM PART END
    #

    #
    # BASIC FUNCTIONS
    #

    def __escape(self):
        if self.state == "Menu":
            self.quit()
        elif self.state == "Game":
            if self.world.requestEscape():
                self.request("Menu")
        else:
            self.request("Menu")

    def quit(self):
        """This function will stop the application"""
        self.userExit()

    def __writeConfig(self):
        """Save current config in the prc file or if no prc file exists
        create one. The prc file is set in the prcFile variable"""
        page = None

        volume = str(round(base.musicManager.getVolume(), 2))
        mute = "#f" if base.AppHasAudioFocus else "#t"
        customConfigVariables = [
            "", "audio-mute", "audio-volume"]
        if os.path.exists(prcFile):
            # open the config file and change values according to current
            # application settings
            page = loadPrcFile(Filename.fromOsSpecific(prcFile))
            removeDecls = []
            for dec in range(page.getNumDeclarations()):
                # Check if our variables are given.
                # NOTE: This check has to be done to not loose our base or other
                #       manual config changes by the user
                if page.getVariableName(dec) in customConfigVariables:
                    decl = page.modifyDeclaration(dec)
                    removeDecls.append(decl)
            for dec in removeDecls:
                page.deleteDeclaration(dec)
            # NOTE: audio-mute are custom variables and
            #       have to be loaded by hand at startup
            # audio
            page.makeDeclaration("audio-volume", volume)
            page.makeDeclaration("audio-mute", mute)
        else:
            # Create a config file and set default values
            cpMgr = ConfigPageManager.getGlobalPtr()
            page = cpMgr.makeExplicitPage("%s Pandaconfig"%appName)
            # set OpenGL to be the default
            page.makeDeclaration("load-display", "pandagl")
            # get the displays width and height
            w = self.pipe.getDisplayWidth()
            h = self.pipe.getDisplayHeight()
            # set the window size in the config file
            page.makeDeclaration("win-size", "%d %d"%(w, h))
            # set the default to fullscreen in the config file
            page.makeDeclaration("fullscreen", "1")
            # audio
            page.makeDeclaration("audio-volume", volume)
            page.makeDeclaration("audio-mute", "#f")
        # create a stream to the specified config file
        configfile = OFileStream(prcFile)
        # and now write it out
        page.write(configfile)
        # close the stream
        configfile.close()

    #
    # BASIC END
    #
# CLASS Main END

Game = Main()
Game.run()

