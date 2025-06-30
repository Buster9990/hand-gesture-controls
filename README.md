# Introduction
Hi! This code uses gestures to control the mouse.\
The aim of this project is to enable users to do as much as possible without touching the mouse.\
This could be used for people who have hurt their hands using mice, or if their laptop is connected to the home TV and they dont feel like getting up to change to the next Youtube video.
# Requirements
To be able to use this, you must:
 - Have a camera connected to the PC. (Gesture detection)
 - Have a fairly decent CPU. (Calculations are a little complex, and this is to be used in the background of course.)
# Setup
Run main.py\
The camera will open.\
Use your right index finger to point as instructed in the app, this represents the position your hand must take for the mouse to be on the part of the screen indicated in the app. (ex: Top-left: this is the hand position you'll do to access the top left of the screen)
# Controls
Mouse movement: Follows the right hand's index finger.\
Left click: Raise the left hand's index finger fully.\
Changing sensitibity: Peace sign  with left hand, and move the left hand to increase/decrease sensitivity as indicated by the bounding box in the camera.
Dragging bounding box: To change the position of where the box is, relative to the camera, just move the right index finger beyond the box in the direction wanted.