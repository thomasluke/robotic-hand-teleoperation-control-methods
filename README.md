# Robotic-Hand-Teleoperation-Control-Methods

This capstone research objectively evaluates and compares new glove and wireless hand tracking control solutions (Leap Motion Controller) for teleoperation of robotic hand manipulators. A new hybrid control method combining both gloved and wireless hand tracking control will also be proposed and evaluated to determine whether any benefits can be observed. The goal of this is to determine the strengths and weaknesses of each robotic hand control method to inform real world applications and direct future research of hand tracking control technologies.

## Complete Robotic Hand System
![picture](/images/complete_robotic_system.jpg?raw=true "Complete Robotic Hand System")

## How to Run Program
1. Install Leap Motion drivers and SDK software V2.3.1.31549 for Windows. 
2. Install link: https://developer-archive.leapmotion.com/v2?id=skeletal-beta&platform=windows&version=2.3.1.31549 
3. Install and setup Python 2 (Python 3 not supported by Leap Motion Controller) 
4. Open terminal window in robot-hand-leap-motion-teleoperation folder.
5. Type "main.py" in terminal window to run code
6. Type '1', '2', '3', '4', '5' or '6' in terminal window to select control method.
7. Keyboard control mode bindings: shift: Thumb, q: pointer finger, w: middle finger, e: ring finger, r: pinky finger
8. Glove control mode: equip flex sensor control glove
8. Leap Motion control mode: place hand above Leap Motion Controller.
10. Combined control modes: equip flex sensor control glove and place hand above Leap Motion Controller.  

## Electrical Wiring Block Diagram
![picture](/images/electrical_wiring_block_diagram.png?raw=true "Electrical Wiring Block Diagram")