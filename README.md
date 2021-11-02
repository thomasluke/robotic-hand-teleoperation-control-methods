# Robotic-Hand-Teleoperation-Control-Methods

This capstone research objectively evaluates and compares new glove and wireless hand tracking control solutions (Leap Motion Controller) for teleoperation of robotic hand manipulators. A new hybrid control method combining both gloved and wireless hand tracking control will also be proposed and evaluated to determine whether any benefits can be observed. The goal of this is to determine the strengths and weaknesses of each robotic hand control method to inform real world applications and direct future research of hand tracking control technologies.

## How to Run Program
1. Install Leap Motion drivers and SDK software V2.3.1.31549 for Windows. 
   Install link: https://developer-archive.leapmotion.com/v2?id=skeletal-beta&platform=windows&version=2.3.1.31549 
2. Install and setup Python 2 (Python 3 not supported by Leap Motion Controller) 
3. Open terminal window in robot-hand-leap-motion-teleoperation folder.
4. Type "main.py" in terminal window to run code
5. Type '1', '2', '3', '4', '5' or '6' in terminal window to select control method.
6. Keyboard control mode bindings: shift: Thumb, q: pointer finger, w: middle finger, e: ring finger, r: pinky finger
7. Glove control mode: equip flex sensor control glove
8. Leap Motion control mode: place hand above Leap Motion Controller.
9. Combined control modes: equip flex sensor control glove and place hand above Leap Motion Controller.  

## Electrical Wiring Block Diagram
![GitHub Logo](/images/electrical wiring block diagram.png)