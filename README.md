# Atmospheric Shower Simulation Workflow

## Overview

This project provides a complete workflow for simulating atmospheric particle showers using CORSIKA, with advanced visualization capabilities including 2D plots and animations in Blender.

## Features

- Interactive parameter configuration for CORSIKA simulations;
- Automated execution of the full simulation pipeline;
- Multiple visualization options:
  - 2D track projections (x-z, y-z, x-y);
  - Animated shower development.
- Customizable visualization parameters:
  - Type of particle to simulate;
  - Energy range;
  - Variation in zenith and azimuthal angles;
  - Energy cut.

## Workflow limitations

The animation is generated with a limited number of lines of the electromagnetic file produced by CORSIKA, as it generates a very large amount of data. By default, this limit is set to 5000 lines, but it can be changed by modifying the workflow.py file on lines 270 and 506, selecting after the "-n" the number of lines desired to run the animation (with the possibility of error during execution).

## Usage

Run the main workflow script using "python3 workflow.py"

## Acknowledgement

Bruno Zanetti, for providing the Blender script to produce animations.
Gabriel Chiritoi, for helping us in translating the CORSIKA outputs into text format.
