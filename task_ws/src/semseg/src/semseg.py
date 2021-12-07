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


def collect_image_files(image_dir,file_pattern):
  images = glob.glob(image_dir + '/' + file_pattern)
  images.sort()
  return images

def collect_poses(file):
  poses = genfromtxt(file, delimiter=',')
  return poses

def playback_images(image_dir,file_pattern,publish_rate):
  image_files = collect_image_files(image_dir,file_pattern)
  rospy.loginfo('Found %i images.',len(image_files))
  bridge = cv_bridge.CvBridge()
  rate = rospy.Rate(publish_rate)
  image_publisher = rospy.Publisher('camera/image_color', sensor_msgs.msg.Image, queue_size = 5)
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

    print(image_file)
    result = img_seg(image)
    # result = image
    cv2.imwrite(results_dir+"/"+image_file.split('/')[-1][:-4]+"_result.jpg", result)
    
    rate.sleep()
  rospy.loginfo('No more images left. Stopping.')

if __name__ == "__main__":
  rospy.init_node('image_sequence_publisher')
  try:
    image_dir = rospy.get_param("~image_dir", "/home/zeeshan/personal/Jared_task_adinkra/task_ws/src/semseg/data")
    results_dir = rospy.get_param("~image_dir", "/home/zeeshan/personal/Jared_task_adinkra/task_ws/src/semseg/results")
    print(image_dir)
    file_pattern = rospy.get_param("~file_pattern", "*.jpg")

    frequency = rospy.get_param("~frequency", 10)

    playback_images(image_dir, file_pattern, frequency)
  except KeyError as e:
    rospy.logerr('Required parameter missing: %s', e)
  except Exception as e:
    import traceback
    traceback.print_exc()