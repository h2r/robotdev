# Copyright (c) 2022 Boston Dynamics, Inc.  All rights reserved.
#
# Downloading, reproducing, distributing or otherwise using the SDK Software
# is subject to the terms and conditions of the Boston Dynamics Software
# Development Kit License (20191101-BDSDK-SL).

import argparse
import numpy as np
import os
import sys
from bosdyn.api.graph_nav import map_pb2
from bosdyn.client.frame_helpers import *
from bosdyn.client.math_helpers import *

"""
This example shows how to load a graph nav map and extract a point cloud in the seed frame.
This requires a map which has been globally optimized using anchoring optimization.
It will export a graph nav map as a PLY file. Use a mesh viewer (such as MeshLab or CloudCompare),
to view the output.
"""


def get_point_cloud_data_in_seed_frame(waypoints, snapshots, anchorings, waypoint_id):
    """
    Create a 3 x N numpy array of points in the seed frame. Note that in graph_nav, "point cloud" refers to the
    feature cloud of a waypoint -- that is, a collection of visual features observed by all five cameras at a particular
    point in time. The visual features are associated with points that are rigidly attached to a waypoint.
    :param waypoints: dict of waypoint ID to waypoint.
    :param snapshots: dict of waypoint snapshot ID to waypoint snapshot.
    :param anchorings: dict of waypoint ID to the anchoring of that waypoint w.r.t the map.
    :param waypoint_id: the waypoint ID of the waypoint whose point cloud we want to render.
    :return: a 3 x N numpy array in the seed frame.
    """
    wp = waypoints[waypoint_id]
    snapshot = snapshots[wp.snapshot_id]
    cloud = snapshot.point_cloud
    odom_tform_cloud = get_a_tform_b(cloud.source.transforms_snapshot, ODOM_FRAME_NAME,
                                     cloud.source.frame_name_sensor)
    waypoint_tform_odom = SE3Pose.from_obj(wp.waypoint_tform_ko)
    waypoint_tform_cloud = waypoint_tform_odom * odom_tform_cloud
    if waypoint_id not in anchorings:
        raise Exception("{} not found in anchorings. Does the map have anchoring data?".format(waypoint_id))
    seed_tform_cloud = SE3Pose.from_obj(anchorings[waypoint_id].seed_tform_waypoint) * waypoint_tform_cloud
    point_cloud_data = np.frombuffer(cloud.data, dtype=np.float32).reshape(int(cloud.num_points), 3)
    return seed_tform_cloud.transform_cloud(point_cloud_data).astype(np.float32)



def load_map(path):
    """
    Load a map from the given file path.
    :param path: Path to the root directory of the map.
    :return: the graph, waypoints, waypoint snapshots, edge snapshots, and anchorings.
    """
    with open(os.path.join(path, "graph"), "rb") as graph_file:
        # Load the graph file and deserialize it. The graph file is a protobuf containing only the waypoints and the
        # edges between them.
        data = graph_file.read()
        current_graph = map_pb2.Graph()
        current_graph.ParseFromString(data)

        # Set up maps from waypoint ID to waypoints, edges, snapshots, etc.
        current_waypoints = {}
        current_waypoint_snapshots = {}
        current_edge_snapshots = {}
        current_anchors = {}
        current_anchored_world_objects = {}

        # Load the anchored world objects first so we can look in each waypoint snapshot as we load it.
        for anchored_world_object in current_graph.anchoring.objects:
            current_anchored_world_objects[anchored_world_object.id] = (anchored_world_object,)
        # For each waypoint, load any snapshot associated with it.
        for waypoint in current_graph.waypoints:
            current_waypoints[waypoint.id] = waypoint

            if len(waypoint.snapshot_id) == 0:
                continue
            # Load the snapshot. Note that snapshots contain all of the raw data in a waypoint and may be large.
            file_name = os.path.join(path, "waypoint_snapshots", waypoint.snapshot_id)
            if not os.path.exists(file_name):
                continue
            with open(file_name, "rb") as snapshot_file:
                waypoint_snapshot = map_pb2.WaypointSnapshot()
                waypoint_snapshot.ParseFromString(snapshot_file.read())
                current_waypoint_snapshots[waypoint_snapshot.id] = waypoint_snapshot

                for fiducial in waypoint_snapshot.objects:
                    if not fiducial.HasField("apriltag_properties"):
                        continue

                    str_id = str(fiducial.apriltag_properties.tag_id)
                    if (str_id in current_anchored_world_objects and
                            len(current_anchored_world_objects[str_id]) == 1):

                        # Replace the placeholder tuple with a tuple of (wo, waypoint, fiducial).
                        anchored_wo = current_anchored_world_objects[str_id][0]
                        current_anchored_world_objects[str_id] = (anchored_wo, waypoint, fiducial)

        # Similarly, edges have snapshot data.
        for edge in current_graph.edges:
            if len(edge.snapshot_id) == 0:
                continue
            file_name = os.path.join(path, "edge_snapshots", edge.snapshot_id)
            if not os.path.exists(file_name):
                continue
            with open(file_name, "rb") as snapshot_file:
                edge_snapshot = map_pb2.EdgeSnapshot()
                edge_snapshot.ParseFromString(snapshot_file.read())
                current_edge_snapshots[edge_snapshot.id] = edge_snapshot
        for anchor in current_graph.anchoring.anchors:
            current_anchors[anchor.id] = anchor
        print("Loaded graph with {} waypoints, {} edges, {} anchors, and {} anchored world objects".
              format(len(current_graph.waypoints), len(current_graph.edges),
                     len(current_graph.anchoring.anchors), len(current_graph.anchoring.objects)))
        return (current_graph, current_waypoints, current_waypoint_snapshots,
                current_edge_snapshots, current_anchors, current_anchored_world_objects)


def load_map_as_points(path):
    """
    Given a string path to a folder that contains a downloaded GraphNav map,
    loads the map as point cloud and returns a (N,3) numpy array.

    If asfloat is True, the output numpy array will have type np.float32.
    """
    (current_graph, current_waypoints, current_waypoint_snapshots, current_edge_snapshots,
     current_anchors, current_anchored_world_objects) = load_map(path)

    # Concatenate the data from all waypoints.
    data = None  # will be a 3XN numpy array
    for wp in current_graph.waypoints:
        cloud_data = get_point_cloud_data_in_seed_frame(
            current_waypoints, current_waypoint_snapshots, current_anchors, wp.id)
        if data is None:
            data = cloud_data
        else:
            data = np.concatenate((data, cloud_data))
    print(data[:10])
    print(data.shape)
    print(data.dtype)
    # import open3d as o3d
    # pcd = o3d.geometry.PointCloud()
    # pcd.points = o3d.utility.Vector3dVector(data)
    # viz = o3d.visualization.Visualizer()
    # viz.create_window()
    # viz.add_geometry(pcd)
    # opt = viz.get_render_option()
    # opt.show_coordinate_frame = True
    # viz.run()
    # viz.destroy_window()
    return data
