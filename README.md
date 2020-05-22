<h1><img src="design/weblogo.png" height="70px"/></h1>

[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)

uhue is a simple [Philips Hue](https://www2.meethue.com/en-us) web application powered by a centralized server (e.g., a [Raspberry Pi](https://www.raspberrypi.org)). uhue is divided into (1) a front-end powered by [materialize.css](https://materializecss.com) components and (2) a backend that powered by [Flask](https://palletsprojects.com/p/flask/) that serves pages and data, and communicates with the Hue Bridge.

## Road Map

### Front End

- [x] Lights (basic I/O: name, location, on/off, colors)
- [x] Groups (basic I/O: name, on/off, colors)
- [ ] Scenes 
- [ ] Animations
- [ ] Sensors
- [ ] Bridges
- [ ] Server settings
- [ ] Server Heartbeat for light updates

### Back End

- [x] Lights 
- [x] Groups
- [x] Scenes 
- [ ] Animations
- [x] Sensors
- [ ] Bridges
- [ ] Users
- [ ] Bridge Communication Optimizations

## Usage

To run uhue, clone the repository and run `python .` from the top level. Like any command line application, using the `-h` flag will print the most up to date arguments with corresponding documentation. 

By default, uhue targets port `8080` on your device, this value can be modified with the `--port` parameter.

## Development 

### Testing 

To run test cases, run `python -m unittest discover` form the top level.
