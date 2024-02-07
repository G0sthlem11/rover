#!/usr/bin/env python3
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch_ros.actions import Node

def generate_launch_description():

    # Replace 'rover' with the correct package name if needed
    pkg_rover_gazebo = get_package_share_directory('rover')

    # Controller Manager Node
    controller_manager_path = os.path.join(pkg_rover_gazebo, 'lib', 'rover', 'controller_manager', 'controller_manager')
    controller_manager = Node(
        package='controller_manager',
        executable=controller_manager_path,
        output='screen',
    )

    # Joint State Controller Spawner Node
    joint_state_controller_spawner_path = os.path.join(pkg_rover_gazebo, 'lib', 'rover', 'controller_manager', 'spawner')
    joint_state_controller_spawner = Node(
        package='controller_manager',
        executable=joint_state_controller_spawner_path,
        name='joint_state_controller_spawner',
        output='screen',
        arguments=['joint_state_controller', '--controller-manager', '/controller_manager'],
    )

    # Joint State Broadcaster Spawner Node
    joint_state_broadcaster_spawner_path = os.path.join(pkg_rover_gazebo, 'lib', 'rover', 'controller_manager', 'spawner')
    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable=joint_state_broadcaster_spawner_path,
        name='joint_state_broadcaster_spawner',
        output='screen',
        arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
    )

    # Robot Controller Spawner Node
    robot_controller_spawner_path = os.path.join(pkg_rover_gazebo, 'lib', 'rover', 'controller_manager', 'spawner')
    robot_controller_spawner = Node(
        package='controller_manager',
        executable=robot_controller_spawner_path,
        name='robot_controller_spawner',
        output='screen',
        arguments=['joint_trajectory_controller', '--controller-manager', '/controller_manager'],
    )

    return LaunchDescription([
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=joint_state_broadcaster_spawner,
                on_exit=[robot_controller_spawner],
            )
        ),
        controller_manager,
        joint_state_broadcaster_spawner,
        robot_controller_spawner,
        joint_state_controller_spawner,
    ])


