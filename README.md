# 2023 Group Studies - Atom Interferometery
## Solomon Sanderson 

Working with an Arduino MKR Vidor 4000 and using its FPGA to acheive precise
timing to control a laser for atom interferometry.

The FPGA folder contains a template from here: https://github.com/vidor-libraries/VidorFPGA.
This includes a lot of files that I have not worked on or edited and configuration files. The main files containing my code are [MKRVIDOR4000_top.v](https://github.com/solomonsanderson/group-studies/blob/main/FPGA/vidordemo/projects/MKRVIDOR4000_template/MKRVIDOR4000_top.v)
and [control.v](https://github.com/solomonsanderson/group-studies/blob/main/FPGA/vidordemo/projects/MKRVIDOR4000_template/control.v).
These are both found in the folder [group-studies/FPGA/vidordemo/projects/MKRVIDOR4000_template/](https://github.com/solomonsanderson/group-studies/blob/main/FPGA/vidordemo/projects/MKRVIDOR4000_template/control.v).



Files:
* ```Analysis```: contains python scripts and the data that was output by the FPGA.
* ```arduinocode```: contains the sketch to be uploaded to the Arduino.
* ```FPGA```: contains the Verilog and quartus files for programming the FPGA on board the Arduino.
* ```bytesreverse.cmd```: is a commmand script which runs a python script to reverse a .ttf file and saves the output (app.h) in the arduino script.

