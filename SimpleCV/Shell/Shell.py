#!/usr/bin/python

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# SimpleCV
# a kinder, gentler machine vision python library
#-----------------------------------------------------------------------
# SimpleCV is an interface for Open Source machine
# vision libraries in Python.
# It provides a consise, readable interface for cameras,
# image manipulation, feature extraction, and format conversion.
# Our mission is to give casual users a comprehensive interface
# for basic machine vision functions and an
# elegant programming interface for advanced users.
#
# more info:
# http://www.simplecv.org
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


#load system libraries
from SimpleCV.__init__ import *

from subprocess import call, Popen
import platform
import subprocess
import time

#Load simpleCV libraries
from SimpleCV.Shell.Tutorial import *
from SimpleCV.Shell.Cheatsheet import *
from SimpleCV.Shell.Example import *
from SimpleCV import __version__ as SIMPLECV_VERSION

IPVER = 0


#libraries for the shell

#if ipython version < 0.11
try:
  from IPython.Shell import IPShellEmbed
  IPVER = 10
except:
  try:
    import IPython
    from IPython.config.loader import Config
    from IPython.frontend.terminal.embed import InteractiveShellEmbed
    IPVER = 11
  except Exception as e:
    raise(e)


#Command to clear the shell screen
def shellclear():
  if platform.system() == "Windows":
    return
  call("clear")

def plot(arg):
  try:
    import matplotlib.pyplot as plt
  except:
    logger.warning("Matplotlib is not installed and required")
    return


  print "args", arg
  print "type", type(arg)
  plt.plot(arg)
  plt.show()


def magic_clear(self, arg):
  shellclear()


"""
If you run SimpleCV directly, it will launch an ipython shell
"""

def setup_shell():

  banner = '+-----------------------------------------------------------+\n'
  banner += ' SimpleCV '
  banner += SIMPLECV_VERSION
  banner += ' [interactive shell] - http://simplecv.org\n'
  banner += '+----------------------------------------------------------+\n'
  banner += '\n'
  banner += 'Commands: \n'
  banner += '\t"exit()" or press "Ctrl+ D" to exit the shell\n'
  banner += '\t"clear" to clear the shell screen\n'
  banner += '\t"tutorial" to begin the SimpleCV interactive tutorial\n'
  banner += '\t"cheatsheet" gives a cheatsheet of all the shell functions\n'
  banner += '\t"example" gives a list of examples you can run'
  banner += '\n'
  banner += 'Usage:\n'
  banner += '\tdot complete works to show library\n'
  banner += '\tfor example: Image().save("/tmp/test.jpg") will dot complete\n'
  banner += '\tjust by touching TAB after typing Image().\n'
  banner += 'Documentation:\n'
  banner += '\texample:'
  banner += 'help Image or ?Image\n'
  banner += '\t\twill give the in-depth information about that class\n'
  banner += '\t"?function_name" will give the quick API documentation\n'
  banner += '\t\texample:'
  banner += '?Image.save\n'
  banner += '\t\twill give help on the image save function'
  exit_msg = '\n... [Exiting the SimpleCV interactive shell] ...\n'


  #IPython version is less than 11
  if IPVER <= 10:
    #setup terminal to show SCV prompt
    argsv = ['-pi1','SimpleCV:\\#>','-pi2','   .\\D.:','-po','SimpleCV:\\#>','-nosep']

    scvShell = IPShellEmbed(argsv)
    scvShell.set_banner(banner)
    scvShell.set_exit_msg(exit_msg)
    scvShell.IP.api.expose_magic("tutorial",magic_tutorial)
    scvShell.IP.api.expose_magic("clear", magic_clear)
    scvShell.IP.api.expose_magic("cheatsheet", magic_cheatsheet)
    scvShell.IP.api.expose_magic("example", magic_examples)

    return scvShell

  #IPython version 0.11 or higher
  else:
    cfg = Config()
    cfg.PromptManager.in_template = "SimpleCV:\\#> "
    cfg.PromptManager.out_template = "SimpleCV:\\#: "
    #~ cfg.InteractiveShellEmbed.prompt_in1 = "SimpleCV:\\#> "
    #~ cfg.InteractiveShellEmbed.prompt_out="SimpleCV:\\#: "
    scvShell = InteractiveShellEmbed(config=cfg, banner1=banner, exit_msg = exit_msg)
    scvShell.define_magic("tutorial",magic_tutorial)
    scvShell.define_magic("clear", magic_clear)
    scvShell.define_magic("cheatsheet", magic_cheatsheet)
    scvShell.define_magic("example", magic_examples)

    return scvShell



def main(*args):

    log_level = logging.WARNING
    if len(args) and len(args[0]) > 1:
      for flag in args[0]:
        if flag in ["--headless","headless"]:
          # set SDL to use the dummy NULL video driver,
          #   so it doesn't need a windowing system.
          os.environ["SDL_VIDEODRIVER"] = "dummy"

        elif flag in ['--nowarnings','nowarnings']:
          log_level = logging.INFO

        elif flag in ['--debug','debug']:
          log_level = logging.DEBUG

    init_logging(log_level)
    shellclear()

    scvShell = setup_shell()
    #Note that all loaded libraries are inherited in the embedded ipython shell
    sys.exit(scvShell())
