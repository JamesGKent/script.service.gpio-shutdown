import xbmc
import xbmcaddon
import time
import os
from datetime import datetime
import pigpio

__settings__   = xbmcaddon.Addon(id='script.service.gpio-shutdown')
__cwd__        = __settings__.getAddonInfo('path')
__icon__       = os.path.join(__cwd__,"icon.png")
__scriptname__ = "GPIO Shutdown"

def log(loglevel, msg):
  xbmc.log("### [%s] - %s" % (__scriptname__,msg,), level=loglevel)
  
global g_pi
global g_gpio_pin
global g_hibernate_time
global g_shutdown_time
global g_reboot_time
global g_pressed_time
global g_cb

def initDefaults():
  global g_gpio_pin
  global g_shutdown_time
  global g_reboot_time
  global g_pressed_time
  g_gpio_pin = 3
  g_shutdown_time = 500
  g_reboot_time = 1000
  g_pressed_time = None
  
def checkSettings():
  global g_pi
  global g_gpio_pin
  global g_shutdown_time
  global g_reboot_time
  global g_cb
  pin = int(__settings__.getSetting("gpiopin"))
  g_shutdown_time = int(__settings__.getSetting("shutdowntime"))
  g_reboot_time = int(__settings__.getSetting("reboottime"))
  if (g_gpio_pin != pin):
    g_gpiopin = pin
    g_pi.set_pull_up_down(g_gpio_pin, pigpio.PUD_UP)
    g_cb.cancel()
    g_cb = g_pi.callback(g_gpio_pin, pigpio.EITHER_EDGE, pin_changed)

def pin_changed(gpio, level, tick):
  global g_gpio_pin
  global g_shutdown_time
  global g_reboot_time
  global g_pressed_time
  if (level == 0):
    g_pressed_time = datetime.now()
##    xbmc.executebuiltin("XBMC.Notification(%s,%s,%s,%s)" % (__scriptname__,"Shut:"+str((float(g_shutdown_time) - g_hibernate_time)/1000),1,__icon__))
##    xbmc.executebuiltin("XBMC.Notification(%s,%s,%s,%s)" % (__scriptname__,"Reb:"+str((float(g_reboot_time) - g_shutdown_time)/1000),1,__icon__))
##    time.sleep(float(g_shutdown_time)/1000)
##    lev = g_pi.read(g_gpio_pin)
##    if (lev == 0):
##      xbmc.executebuiltin("XBMC.Notification(%s,%s,%s,%s)" % (__scriptname__,"Shutdown",1,__icon__))
##    else:
##      return
##    time.sleep((float(g_reboot_time) - g_shutdown_time)/1000)
##    lev = g_pi.read(g_gpio_pin)
##    if (lev == 0):
##      xbmc.executebuiltin("XBMC.Notification(%s,%s,%s,%s)" % (__scriptname__,"Reboot",1,__icon__))
##    else:
##      return
  elif (level == 1):
    curtime = datetime.now()
    timediff = curtime - g_pressed_time
    ms = timediff.seconds*1000+timediff.microseconds/1000
    if ms > g_reboot_time:
      xbmc.executebuiltin("XBMC.Notification(%s,%s,%s,%s)" % (__scriptname__,"Rebooting",10,__icon__))
      time.sleep(5)
      xbmc.restart()
    elif ms > g_shutdown_time:
      xbmc.executebuiltin("XBMC.Notification(%s,%s,%s,%s)" % (__scriptname__,"Shuting down",10,__icon__))
      time.sleep(5)
      xbmc.shutdown()

def mainloop():
  global g_pi
  global g_gpio_pin
  global g_cb
  g_pi = pigpio.pi()
  g_pi.set_pull_up_down(g_gpio_pin, pigpio.PUD_UP)
  g_cb = g_pi.callback(g_gpio_pin, pigpio.EITHER_EDGE, pin_changed)
  while not xbmc.abortRequested:
    time.sleep(1)
    checkSettings()
  g_cb.cancel()
  g_pi.stop()
  
initDefaults()
checkSettings()
mainloop()

