import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument

def generate_launch_description():
    # Check if we're told to use sim time
    use_sim_time = LaunchConfiguration('use_sim_time')
    # Set the path to this package
    pkg_share = get_package_share_directory('rover')
    # Set the path to the URDF file
    urdf_file_path = os.path.join(pkg_share, 'urdf', 'rover.urdf')

    # Robot State Publisher node
    robot_state_publisher_cmd = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': open(urdf_file_path).read(), 'use_sim_time': use_sim_time}],
        remappings=[('/robot_description', '/robot_description')])

    # Joint State Publisher node with GUI
    joint_state_publisher_gui_cmd = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen',
        parameters=[{'use_gui': 'true'}])

    # Create the launch description
    ld = LaunchDescription()

    # RViz node
    rviz_config_path = os.path.join(pkg_share, 'rviz', 'conf.rviz')
    rviz_cmd = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_path])

    # Transformations statiques pour chaque joint
    static_transform_publisher_RightBack_wheel = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            '-1.1102230246251565404e-16', 
            '-0.010000000000000064393', 
            '0.070000000000000020539', 
            '0.5000000155100947', 
            '0.5000000155100947', 
            '-0.5000000155100947', 
            '0.5000000155100947', 
            'support_moteur', 
            'roue'],
        output='screen'
    )

    static_transform_publisher_RightBackSupport = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            '-0.14295706512309536151', 
            '0.27378000351859554939', 
            '-0.047774398222807878955', 
            '-0.71', 
            '0.71', 
            '0', 
            '0', 
            'chassis', 
            'support_moteur'],
        output='screen'
    )


    static_transform_publisher_RightMid_wheel = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            '-0.25394227674212060952',       # x
            '0.011189264940975884866',       # y
            '-0.11590201700749945546',       # z
            '-0.71',                         # qw
            '0',                             # qx
            '-0.71',                         # qy
            '0',                             # qz
            'chassis',                       # parent_frame_id
            'roue_2'],                       # child_frame_id
        output='screen'
    )

    static_transform_publisher_RightFront_wheel = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            '-5.5511151231257827021e-17', 
            '-0.01000000000000014766', 
            '0.069999999999999965028', 
            '0.71',                          # qw
            '0',                             # qx
            '0',                         # qy
            '0.71',                             # qz
            'support_moteur_2',              # parent_frame_id
            'roue_3'],                       # child_frame_id
        output='screen'
    )

    static_transform_publisher_RightFrontSupport = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            '-0.1938421', 
            '-0.26350', 
            '-0.0441901', 
            '0.71',                          # qw
            '-0.71',                         # qx
            '0',                             # qy
            '0',                             # qz 
            'chassis', 
            'support_moteur_2'],
        output='screen'
    )

    static_transform_publisher_LeftFront_wheel = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            '5.5511151231257827021e-17', 
            '-0.01000000000000014766', 
            '0.069999999999999965028', 
            '0.71',                          # qw
            '0',                             # qx
            '0',                         # qy
            '0.71',                             # qz 
            'support_moteur_3', 
            'roue_4'],
        output='screen'
    )

    static_transform_publisher_LeftFrontSupport = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            '0.19394145', 
            '-0.26350778', 
            '-0.04412533', 
            '0.71',                          # qw
            '0.71',                             # qx
            '0',                          # qy
            '0',                           # qz
            'chassis', 
            'support_moteur_3'],
    output='screen'
    )


    static_transform_publisher_LeftMid_wheel = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            '0.26263534', 
            '0.01063094', 
            '-0.11533409', 
            '-0.71',                         # qw
            '0',                             # qx
            '0.71',                          # qy
            '0',                             # qz 
            'chassis', 
            'roue_5'],
        output='screen'
    )

    static_transform_publisher_LeftBack_wheel = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            '0.0', 
            '0.0', 
            '0.067125', 
            '0.71',                         # qw
            '0',                             # qx
            '0',                          # qy
            '0.71',                             # qz
            'support_moteur_4', 
            'roue_6'],
        output='screen'
    )

    static_transform_publisher_LeftBackSupport = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            '0.14294218', 
            '0.27218219', 
            '-0.04747117',  
            '0.71',                            # qw
            '0.71',                           # qx
            '0',                            # qy
            '0',                            # qz
            'chassis', 
            'support_moteur_4'],
        output='screen'
    )

    # Add each static transform publisher to the launch description
    ld.add_action(rviz_cmd)
    ld.add_action(robot_state_publisher_cmd)
    ld.add_action(joint_state_publisher_gui_cmd)
    ld.add_action(static_transform_publisher_RightBack_wheel)
    ld.add_action(static_transform_publisher_RightBackSupport)
    ld.add_action(static_transform_publisher_RightMid_wheel)
    ld.add_action(static_transform_publisher_RightFront_wheel)
    ld.add_action(static_transform_publisher_RightFrontSupport)
    ld.add_action(static_transform_publisher_LeftFront_wheel)
    ld.add_action(static_transform_publisher_LeftFrontSupport)
    ld.add_action(static_transform_publisher_LeftMid_wheel)
    ld.add_action(static_transform_publisher_LeftBack_wheel)
    ld.add_action(static_transform_publisher_LeftBackSupport)

    return ld
