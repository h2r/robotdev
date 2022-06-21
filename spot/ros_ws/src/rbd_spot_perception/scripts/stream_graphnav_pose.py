#!/usr/bin/env python
# Streams graphnav pose; assumes a graph has been uploaded.
import sys
import time
import argparse

import rospy
#http://wiki.ros.org/tf2/Tutorials/Writing%20a%20tf2%20broadcaster%20%28Python%29
from tf2_ros import TransformBroadcaster
import geometry_msgs.msg

import rbd_spot


def _body_pose_to_tf(body_pose, map_frame, base_frame):
    # publish body pose transform
    t = geometry_msgs.msg.TransformStamped()
    t.header.stamp = rospy.Time.now()
    t.header.frame_id = base_frame
    t.child_frame_id = map_frame
    t.transform.translation.x = body_pose.position.x
    t.transform.translation.y = body_pose.position.y
    t.transform.translation.z = body_pose.position.z
    t.transform.rotation.x = body_pose.rotation.x
    t.transform.rotation.y = body_pose.rotation.y
    t.transform.rotation.z = body_pose.rotation.z
    t.transform.rotation.w = body_pose.rotation.w
    return t


def main():
    parser = argparse.ArgumentParser("stream graphnav pose")
    parser.add_argument("-p", "--pub", action="store_true", help="publish stamped poses as"
                        "tf transforms between map frame and base link frame")
    parser.add_argument("--base-frame", type=str, help="tf frame of the robot base. Default 'body'",
                        default='body')
    parser.add_argument("--map-frame", type=str, help="tf frame of the map. Default 'graphnav_map'",
                        default='graphnav_map')
    parser.add_argument("-t", "--timeout", type=float, help="time to keep streaming")
    args = parser.parse_args()

    if args.pub:
        rospy.init_node("stream_graphnav_pose")
        tf_br = TransformBroadcaster()


    conn = rbd_spot.SpotSDKConn(sdk_name="StreamImageClient")
    graphnav_client = rbd_spot.graphnav.create_client(conn)

    _start_time = time.time()
    while True:
        try:
            state_result, _used_time = rbd_spot.graphnav.getLocalizationState(graphnav_client)
            print("GetLocalizationState took %.3fs" % _used_time)
            body_pose = rbd_spot.graphnav.get_pose(state_result, frame='seed')
            waypoint_id, _ = rbd_spot.graphnav.get_pose(state_result, frame='waypoint')
            print("body pose (seed frame):")
            print(body_pose)
            print(f"waypoint id: {waypoint_id}")
            print("----")

            if args.pub:
                t = _body_pose_to_tf(body_pose, args.map_frame, args.base_frame)
                tf_br.sendTransform(t)
            _used_time = time.time() - _start_time
            if args.timeout and _used_time > args.timeout:
                break
        finally:
            if args.pub and rospy.is_shutdown():
                sys.exit(1)


if __name__ == "__main__":
    main()
