# GPIO PWM Backlight
Provides a hardware button to shutdown/restart a raspberry pi running kodi via the GPIO pins of the raspberry pi.
This relies on the pigpio library being present and the system daemon running.
See:
https://github.com/JamesGKent/script.module.pigpio-master for the raspberry pi 2 version.

At the time of writing a version has not been compiled for the raspberry pi 1

As the raspberry pi does not support other sleep modes such as hibernate only shutdown and reboot are supported.
It  is recommended GPIO3 is used as the input pin as then the same button can be used to wake the pi once it has been shut down.

This addon offers:
- Setting any GPIO pin as the shutdown pin
- Setting a time the button must be held to shut down
- Setting a time the button must be held to reboot