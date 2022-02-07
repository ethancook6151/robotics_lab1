#!/usr/bin/env python3

# import ROS for developing the node
import rospy 
# import geometry_msgs/Twist for control commands 
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose 
from robotics_lab1.msg import Turtlecontrol


pos_msg = Pose()
turtle_msg = Turtlecontrol()
twist = Twist()


def pose_callback(data):
	global pos_msg
	pos_msg.x = data.x
	
def control_callback(data):
	global turtle_msg
	turtle_msg.xd = data.xd
	turtle_msg.kp = data.kp


if __name__ == '__main__':
	rospy.init_node('ControlNode', anonymous=True)
	rospy.Subscriber('/turtle1/pose', Pose, pose_callback)
	rospy.Subscriber('/turtle1/control_params', Turtlecontrol, control_callback)
	pos_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
	loop_rate = rospy.Rate(10)

	# run a control loop on a regular basis (every 0.1 second)
	while not rospy.is_shutdown():
		twist.linear.x = turtle_msg.kp * (turtle_msg.xd - pos_msg.x)
		pos_pub.publish(twist) 
		# wait for 0.1 of a second and go to next step 
		loop_rate.sleep()
