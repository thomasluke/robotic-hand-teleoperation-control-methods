################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import Leap
import sys
import threading
import time
import serial
import numpy
import struct
import json
import keyboard
import time
import csv
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from serial import SerialException
import random

arduino = serial.Serial('COM3', 9600, timeout=0.1)
# self.servo_angles = []

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / numpy.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return numpy.arccos(numpy.clip(numpy.dot(v1_u, v2_u), -1.0, 1.0))

class SampleListener(Leap.Listener):
    
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END'] 

    def on_init(self, controller):
        print "Initialized"
        self.start_leap = time.time()
        self.end_leap = time.time()
        self.latency_leap = 0.0

        self.start_arduino = time.time()
        self.end_arduino = time.time()
        self.latency_arduino = 0.0

        self.latency_total_start = time.time()
        self.latency_total_end = time.time()
        self.latency_total = 0.0

        self.global_time_start = time.time()

        self.iterator = 0.1
        self.rows = []
        self.number = 0
        self.lock = False
        self.lock2 = False
        self.lock3 = False

        self.servo_angles = [0,0,0,0,0]
        self.data_confidence = 0
        self.roll = 0

        self.start_time = time.time()
        self.time_passed=[0,0,0,0,0]
        self.rows2 = []
        self.close = 120
        self.open = 80
        self.poses = [[self.close,self.open,self.open,self.open,self.open],[self.open,self.close,self.open,self.open,self.open],[self.open,self.open,self.close,self.open,self.open],[self.open,self.open,self.open,self.close,self.close],[self.close,self.close,self.close,self.close,self.close],[self.open,self.open,self.open,self.open,self.open]]
        self.indicies = []
        self.pose = 0

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def run(self):
        # threading.Thread(target = main, args=(self,)).start()
        # threading.Thread(target = self.measure_latency).start()
        # threading.Thread(target = self.measure_gestures()).start()
        threading.Thread(target = self.MeasureAngles).start()

    
    def measure_latency(self):
            # interp_arduino_latency = []

            while True:
                count = 0
                # time.sleep(0.02)

                if (arduino.inWaiting() > 0):
                    if arduino.read() == "\n":
                        try:
                            latency = [0,0]

                            latency[0] = int(arduino.readline().decode("utf-8").strip('\n').strip('\r'))
                            latency[1] = int(arduino.readline().decode("utf-8").strip('\n').strip('\r'))
                            
                            self.latency_arduino = float(min(latency))/1000
                            self.latency_total = float(max(latency))/1000
                            # self.latency_arduino = int(arduino.readline().decode("utf-8").strip('\n').strip('\r'))
                            # average_interp_arduino_latency = int(arduino.readline().decode("utf-8").strip('\n').strip('\r'))                     
                        except ValueError: # this deals with the error
                            pass # if we don't change the value of myData it stays a string                
                                # time.sleep(0.002)
                        # arduino.reset_input_buffer()
                        count+=1
                        
                        self.number+=1

                        # self.latency_arduino = array[0]/array[1]

                        # self.latency_total_end = time.time()
                        # self.latency_total = (self.latency_total_end - self.latency_total_start) * 1000
                        # self.latency_total_start = time.time()
                        # print self.latency_total/10

                        latency_serial_leap = self.latency_total - self.latency_arduino

                        # print("Latency Leap (ms): " + str(self.latency_leap) + " Latency Arduino (ms): " + str(self.latency_arduino) + "Latency Average Interp Arduino (ms): " + str(average_interp_arduino_latency) + " Latency Serial (ms): " + str(latency_serial) + " Latency total (ms): " + str(self.latency_total))

                        # self.rows.append([str(self.number),str(self.latency_leap),str(self.latency_arduino),str(average_interp_arduino_latency),str(latency_serial),str(self.latency_total)])

                        # print("Latency Leap (ms): " + str(self.latency_leap) + " Latency Arduino (ms): " + str(self.latency_arduino) + " Latency Serial (ms): " + str(latency_serial) + " Latency total (ms): " + str(self.latency_total))
                        print("Latency Arduino (ms): " + str(self.latency_arduino) + " Latency Serial and Leap (ms): " + str(latency_serial_leap) + " Latency total (ms): " + str(self.latency_total))

                        self.rows.append([str(self.number),str(self.latency_arduino),str(latency_serial_leap),str(self.latency_total)])
                        
                    if keyboard.is_pressed("s"):
                            
                        fields = ["Number", "Latency Arduino", "Latency Serial and Leap", "Latency Total"]
                        # fields = ["Number", "Latency Leap", "Latency Arduino", "Latency Average Interp Arduino", "Latency Serial", "Latency Total"]

                        # name of csv file 
                        filename = "Latency Data.csv"
                
                        # writing to csv file 
                        with open(filename, 'wb') as csvfile: 
                            # creating a csv writer object 
                            csvwriter = csv.writer(csvfile) 
                                
                            # writing the fields 
                            csvwriter.writerow(fields) 
                                
                            # writing the data rows 
                            csvwriter.writerows(self.rows)
                        
                        print "LATENCY DATA SAVED TO CSV FILE" 
    
    def MeasureAngles(self):
        
        while True:
            count = 0
            finger_angles = []
            # print finger_angles
            if (arduino.inWaiting() > 0):
                if arduino.read() == "\n":
                    while count < 5:
                        try:
                            # This will make it an integer, if the string is not an integer it will throw an error
                            finger_angles.append(int(arduino.readline().decode("utf-8").strip('\n').strip('\r'))) 
                        except ValueError: # this deals will the error
                            pass # if we don't change the value of myData it stays a string                
                                # time.sleep(0.002)
                        count += 1
                # self.number+=1
                # line = arduino.readline().strip()
                # finger_angles = line.decode('ascii').split(',')
                # finger_angles.append(list(arduino.read(1)))
                    current_time = time.time() - self.global_time_start
                    self.rows.append([current_time, finger_angles[0], finger_angles[1], finger_angles[2], finger_angles[3], finger_angles[4]])
                    # print finger_angles
                    
                    measure_gestures(self,finger_angles)
            
            if keyboard.is_pressed("s"):
                                        
                    # fields = ["Thumb Flex","Pointer Flex", "Middle Flex", "Ring and Pinky Flex", "Fist", "Open Hand"]
                    fields = ["Thumb Flex","Pointer Flex", "Middle Flex", "Ring and Pinky Flex", "Fist"]

                    # name of csv file 
                    filename = str("Gesture Latency Data.csv")

                    # writing to csv file 
                    with open(filename, 'wb') as csvfile: 
                        # creating a csv writer object 
                        csvwriter = csv.writer(csvfile) 
                            
                        # writing the fields 
                        csvwriter.writerow(fields) 
                            
                        # writing the data rows 
                        csvwriter.writerows(self.rows)
        
                    print "LATENCY DATA SAVED TO CSV FILE"                   
            # if keyboard.is_pressed("s"):
                                
            #                 fields = ["Time","Thumb", "Pointer", "Middle", "Ring", "Pinky"]

            #                 # name of csv file 
            #                 filename = "Measure Angle Data.csv"
                    
            #                 # writing to csv file 
            #                 with open(filename, 'wb') as csvfile: 
            #                     # creating a csv writer object 
            #                     csvwriter = csv.writer(csvfile) 
                                    
            #                     # writing the fields 
            #                     csvwriter.writerow(fields) 
                                    
            #                     # writing the data rows 
            #                     csvwriter.writerows(self.rows)
                            
            #                 print "LATENCY DATA SAVED TO CSV FILE"       
    
    
    def on_frame(self, controller):
        # time.sleep(0.003)
        # Get the most recent frame and report some basic information
        frame = controller.frame()  # Frame sent from Leap Motion Controller to computer

        if self.lock == False:
                
            self.run()
            self.lock = True

        self.iterator = self.iterator + 1

        # Get hands data from each frame
        # For loop repeats for each hand present in the frame
        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

            # Get the hand's normal vector and direction
            normal = hand.palm_normal  # Normal vectors points outwards from palm
            direction = hand.direction  # Direction vector points from palm towards fingertips
            self.data_confidence = hand.confidence           
            arm = hand.arm
            self.roll = int((normal.roll * Leap.RAD_TO_DEG)+90)

            resultant_vector_mag = [None] * 5
            
            # Reset variables
            finger_flexion = []
            self.servo_angles = []
            index = 0
            
            # Get fingers
            for finger in hand.fingers:

                # Converting finger and hand vectors in numpy library arrays
                finger_vector = numpy.array([finger.direction[0],finger.direction[1],finger.direction[2]])
                hand_vector = numpy.array([hand.direction[0],hand.direction[1],hand.direction[2]])
                hand_normal_vector = numpy.array([hand.palm_normal[0],hand.palm_normal[1],hand.palm_normal[2]])
                
                # If tracked finger is thumb, then measure its flexion angle with respect to the hand/palm normal vector
                if index == 0:
                    # Calculating angle between finger and hand vectors ensures that hand orientation does not matter.
                    finger_flexion.append(angle_between(finger_vector, hand_normal_vector)) 
                    # Conversion factor finger flexion values to servo motor rotation angle.  
                    self.servo_angles.append(int(abs((180*3)-(finger_flexion[index]*(180/0.5))))) 
                
                # If the tracked finger is not a thumb then measure its flexion angle with respect to the hand/palm vector
                else:
                    # Calculating angle between finger and hand vectors ensures that hand orientation does not matter.
                    finger_flexion.append(angle_between(finger_vector, hand_vector))
                    # Conversion factor finger flexion values to servo motor rotation angle. 
                    
                    self.servo_angles.append(int(finger_flexion[index]*(180/2.5)))
                
                # Iterate index value used for array indexing
                index = index + 1

            self.end_leap = time.time()
            self.latency_leap = (self.end_leap - self.start_leap)*1000
            self.start_leap = time.time()
          
            # arduino.reset_output_buffer()

            # # Serial write newline character which to inidcate where to start reading bytes in the Arduino code
            # arduino.write('\n')
                             
            # Serial write servo rotation angles in byte (binary) form to the Arduino code. Divide values sent to keep in the required byte range of -128<=value<=128. Values multiplied back in Arduino code. 
            # arduino.write(struct.pack('>8b',int(0),self.servo_angles[0]-127, self.servo_angles[1]-127, self.servo_angles[2]-127, self.servo_angles[3]-127, self.servo_angles[4]-127, self.roll/4, int(self.data_confidence*100)))
            arduino.write(struct.pack('>7b',int(0),self.servo_angles[0]-127, self.servo_angles[1]-127, self.servo_angles[2]-127, self.servo_angles[3]-127, self.servo_angles[4]-127, int(self.data_confidence*100)))
            # arduino.write(struct.pack('>7b',self.servo_angles[0]/4, self.servo_angles[1]/4, self.servo_angles[2]/4, self.servo_angles[3]/4, self.servo_angles[4]/4, self.roll/4, int(self.data_confidence*100)))
                       # arduino.reset_output_buffer()
            # print arduino.out_waiting

            self.iterator = 0

            # print "Finger Angles: " + str(self.servo_angles) + " Leap Data Confidence: " + str(int(self.data_confidence*100))
            
def measure_gestures(self,finger_angles):
    
    latencies = []
    index = 0
    checker = True
    pose_names = ["Thumb Flex","Pointer Flex", "Middle Flex", "Ring and Pinky Flex", "Fist", "Open Hand"]

    if len(self.indicies) < 1:
            
            self.indicies = [0,1,2,3,4]
            self.rows.append(self.time_passed)
            self.time_passed = [0,0,0,0,0]

    while index < 5:
            finger_pose = self.poses[self.pose][index]
            if   finger_pose == self.open:
                if finger_angles[index]>self.open:
                    checker = False
            elif finger_pose == self.close:
                if finger_angles[index]<self.close:
                    checker = False

            index+=1

    if checker == True and self.pose == 5:
            
            self.pose=random.choice(self.indicies)

            print "Next Pose: " + str(pose_names[self.pose])

            checker = False

            self.start_time = time.time()
    
    if checker == True:
            latency = time.time()-self.start_time
            print str(pose_names[self.pose]) + " Latency: " + str(latency) 
            self.time_passed[self.pose] = latency
            
            self.indicies.remove(self.pose)
            self.pose = 5
            print str(pose_names[self.pose]) + " For Next Pose"

def main():
    
    print "Select Control Mode: Please type 1, 2, 3, 4, 5 or 6"
    print "Mode 1: Automatic Control Selection (Not Implemented. Does Not WorkQQQ)" # Switches automatically between Leap Motion and glove control based on whether the Leap Motion is receiving frame data
    print "Mode 2: Leap Motion Control" # Leap Motion hand tracking control
    print "Mode 3: Glove Control" # Glove hand tracking control
    print "Mode 4: Keyboard Control" # Shift, q, w, e, r keyboard press control
    print "Mode 5: Combined Control " # Combined leap motoon and glove hand tracking control for potentially imporved accuracy
    print "Mode 6: Combined Control Interpolated Leap Data" # Combined leap motoon and glove hand tracking control for potentially imporved accuracy


    while 1:

        mode = raw_input()

        if mode == "1" or mode == "2" or mode == "3" or mode == "4" or mode == "5" or mode == "6": 
            
            print "Control mode " + mode + " selected"
            
            # Serial write newline character which to inidcate where to start reading bytes in the Arduino code
            arduino.write('\n')
                
            # Serial write servo rotation angles in byte (binary) form to the Arduino code.
            arduino.write(struct.pack('>1b', int(mode)))

            break
            
        else:

            print "Invalid mode selected. Please type '1', '2', '3', '4', '5' or '6'"

    if mode == "1" or mode == "2" or mode == "3" or  mode == "5" or mode == "6":

        # Create a sample listener and controller
        listener = SampleListener()
        controller = Leap.Controller()
        
        # Have the sample listener receive events from the controller
        controller.add_listener(listener)

        # Keep this process running until Enter is pressed
        print "Press Enter to quit..."
        try:
            sys.stdin.readline()
        except KeyboardInterrupt:
            pass
        finally:
            # Remove the sample listener when done
            controller.remove_listener(listener)

    elif mode == "4":

        while True:

            servo_angles = []

            finger_keys = ["shift", "q", "w", "e", "r"]

            for key in finger_keys:

                if keyboard.is_pressed(key):
                    servo_angles.append(180)
                else:
                    servo_angles.append(0)
                    # servo_angles[idx] = 180       

            # Serial write newline character which to inidcate where to start reading bytes in the Arduino code
            arduino.write('\n')
                
            # Serial write servo rotation angles in byte (binary) form to the Arduino code. Divide values sent to keep in the required byte range of -128<=value<=128. Values multiplied back in Arduino code. 
            
            arduino.write(struct.pack('>6b', int(0),servo_angles[0]-127, servo_angles[1]-127., servo_angles[2]-127, servo_angles[3]-127, servo_angles[4]-127))

            # Print terminal message showing servo motor rotation values being sent to Arduino via serial communication
            print "Finger Angles: " + str(servo_angles)
            # time.sleep(0.1)
            
            # measure_latency("Keyboard")
    
if __name__ == "__main__":
    main()
