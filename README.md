# Evolution Simulator
This repository contains an attempt to simulate evolution.  

## Table Of Contents
 * [Code walkthrough](#code-walkthrough)
 * [World](#world)
 * [Creature](#creature)
 * [Brain](#brain)
 * [Genome](#genome)
 
 ## Code walkthrough
 
 The simulator.py in simulator directory contains the Simulation class. When initialised it will read parameters from the 
 config.ini file by default. In order to change the config file, while initialising, pass the custom config file path in 
 the constructor. 
 
 The simulator generates a 2-D world for creatures. World class contains a 2-D grid which contains the indexes of creature.
 
