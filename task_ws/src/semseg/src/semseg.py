#!/usr/bin/python

import roslib
import rospy
import sensor_msgs.msg
import cv_bridge
import glob
import cv2
import numpy as np
from numpy import genfromtxt
import math
import tf
import os
from watershed import img_seg

# read image names from the data folder
def collect_image_files(image_dir,file_pattern):
  images = glob.glob(image_dir + '/' + file_pattern)
  images.sort()
  return images

# Read image, publish it on ROS topic, do segmentation and publish the results on another ROS topic
def playback_images(image_dir,file_pattern,publish_rate):
  image_files = collect_image_files(image_dir,file_pattern)
  rospy.loginfo('Found %i images.',len(image_files))
  bridge = cv_bridge.CvBridge()
  rate = rospy.Rate(publish_rate)
  # Input and result publisher objects
  image_publisher = rospy.Publisher('input_images', sensor_msgs.msg.Image, queue_size = 5)
  result_publisher = rospy.Publisher('results', sensor_msgs.msg.Image, queue_size = 5)

  rospy.loginfo('Starting playback.')
  for image_file in image_files:
    if rospy.is_shutdown():
      break
    now = rospy.Time.now()
    image = cv2.imread(image_file)
    image_msg = bridge.cv2_to_imgmsg(np.asarray(image[:,:]), encoding='bgr8')
    image_msg.header.stamp = now
    image_msg.header.frame_id = "/camera"
    image_publisher.publish(image_msg)

    # Call image segmentation function
    result = img_seg(image)
    # Write segmentation results in results folder
    cv2.imwrite(results_dir+"/"+image_file.split('/')[-1][:-4]+"_result.jpg", result)
    # Publish results on ROS topic
    result = bridge.cv2_to_imgmsg(np.asarray(result[:,:]), encoding='bgr8')
    result.header.stamp = now
    result.header.frame_id = "/result"
    result_publisher.publish(result)
    
    
    rate.sleep()
  rospy.loginfo('No more images left. Stopping.')

if __name__ == "__main__":
  rospy.init_node('image_sequence_publisher')
  try:
    image_dir = rospy.get_param("/semseg/image_dir")
    results_dir = rospy.get_param("/semseg/result_dir")
    print(image_dir)
    file_pattern = rospy.get_param("/semseg/file_pattern", "*.jpg")

    frequency = rospy.get_param("~frequency", 10)

    playback_images(image_dir, file_pattern, frequency)
  except KeyError as e:
    rospy.logerr('Required parameter missing: %s', e)
  except Exception as e:
    import traceback
    traceback.print_exc()