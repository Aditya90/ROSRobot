#!/usr/bin/env python
'''
'''
import sys
import rospy
import cv2

from sensor_msgs.msg import Image, CameraInfo
import numpy as np
from cv_bridge import CvBridge, CvBridgeError


class ImageCapture:

    def __init__(self):

        self.node_name = 'ImageCapture'
        rospy.init_node(self.node_name, anonymous=True)

        # What we do during shutdown
        rospy.on_shutdown(self.cleanup)

        # Create the cv_bridge object
        self.bridge = CvBridge()

        # Subscribe to the
        self.image_sub = rospy.Subscriber("/cv_camera/image_raw", Image, self.image_capture_callback)

    def image_capture_callback(self, opencv_image):
        # Use cv_bridge() to convert the ROS image to OpenCV format
        try:
            cv_image = self.bridge.imgmsg_to_cv2(opencv_image, "bgr8")
        except CvBridgeError as e:
            print(e)

        # Convert the image to a Numpy array since most cv2 functions
        # require Numpy arrays.
        # @todo - Create a topic to publish this data for opencv processing
        # np_data = np.array(frame, dtype=np.uint8)

        # Display the image.
        cv2.imshow(self.node_name, cv_image)

        # Use the wait key to make sure the window is populated
        # with the image.
        cv2.waitKey(3)

    def cleanup(self):
        cv2.destroyAllWindows()

if __name__ == '__main__':

    # Start the camera capture object
    ImageCapture()

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")