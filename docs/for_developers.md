# Developer documentation


## Requirements

There are both hardware and software requirements needed for the Durimeter to work.

### Hardware
1. Raspberry Pi 3
2. Phidget spatial sensor + GPS
3. Something to mount the spatial sensor on (binocular for example?)

Here is my test hardware setup..

<img src="../imgs/img1.jpg" width="650px">

### Getting started

* Install debian packages: `$ apt-get install git gcc python python-dev python-pip espeak`
* Install Driver (See [Phidgets website] (http://www.phidgets.com/docs/Operating_System_Support))
* Create a Python virtualenv
* Within this virtualenv, run:
  * `pip install -r requirements.txt`
* And you're golden


# Dev environment

To speed up development work you are perfectly capable to run the entire MMO server on your local Linux laptop / server, instead of booting up the Raspberry Pi.

Enable the python environment and start the "fake" server that fakes the spatial sensor and GPS:
```bash
source venv/bin/activate
python start_fake.py
```

# Prod environment

When the Raspberry Pi boots it will automatically start the MMO server like this:
```bash
source venv/bin/activate
python start_actual.py
```

# System overview

The architecture is like this:
1. Nginx is the proxy / frontend web server. Functions as a reverse-proxy.
2. Supervisor will start 2 "gunicorn" workers based on the script: `/home/pi/rdi_inclinometer/gunicorn_start`


## Gotchas

One would assume that the application will stop if running this: `$ sudo supervisorclt mmo stop`, and supervisor echo's to the prompt 
that the service is indeed stopped. However, the python processes are still running. There is an issue for this bug here: https://github.com/Statoil/rdi_inclinometer/issues/33


# Useful resources

- Sensors Info & links to other docs http://www.phidgets.com/products.php?product_id=1044
- Python Excel Library https://openpyxl.readthedocs.org/en/latest/tutorial.html

- Raspberry Pi GPIO Interrupts
    - http://raspi.tv/2013/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio
    - http://raspi.tv/2013/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio-part-2

- GPIO Diagram https://learn.adafruit.com/introducing-the-raspberry-pi-model-b-plus-plus-differences-vs-model-b/gpio-port

- GPIO Library (Python)
    - http://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
    - http://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/

- Pull-Ups Resistor (Explained) https://learn.sparkfun.com/tutorials/pull-up-resistors

# Authors

- Arve Skogvold <arve@skogvold.org>
- Asbjørn A. Fellinghaug <asbjorn@fellinghaug.com>