import os
from ament_index_python.packages import get_package_share_directory
from launch_ros.parameter_descriptions import ParameterValue
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.substitutions import Command, FindExecutable, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit

def generate_launch_description():
    model_arg = DeclareLaunchArgument(
        name='model',
        description='Absolute path to robot urdf file'
    )

    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    use_sim_time = LaunchConfiguration('use_sim_time')
    package_name = 'rover'  # Change this to your actual package name
    pkg_share = FindPackageShare(package=package_name).find(package_name)
    pkg_gazebo_ros = FindPackageShare(package='gazebo_ros').find('gazebo_ros')

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        name='use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    )

    robot_name_in_model = 'rover'  # Change this to your actual robot name

    # Get URDF via xacro
    urdf_file_name = 'rover.urdf'  # Change this to your actual URDF file name
    urdf = os.path.join(
        get_package_share_directory('rover'),  # Change this to your actual package name
        'urdf',
        urdf_file_name
    )
    with open(urdf, 'r') as infp:
        robot_desc = infp.read()

    robot_description = {"robot_description": robot_desc}

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'use_sim_time': use_sim_time, 'robot_description': robot_desc}],
        name='robot_state_publisher',
    )

    spawn = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=["-topic", "/robot_description",
                   "-entity", robot_name_in_model,
                   "-x", '0.0',
                   "-y", '0.0',
                   "-z", '0.05',
                   "-Y", '0.0']
    )

    gazebo = ExecuteProcess(
        cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so',
             '-s', 'libgazebo_ros_init.so'], output='screen',
    )

    return LaunchDescription([
        declare_use_sim_time_cmd,
        spawn,
        robot_state_publisher_node,
        gazebo
    ])
