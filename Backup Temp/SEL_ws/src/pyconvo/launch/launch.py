import os
import launch
import launch_ros.actions

from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python import get_package_share_directory
from launch_ros.actions import Node


def generate_launch_description():

    ld = launch.LaunchDescription()

    panda = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('moveit_resources_panda_moveit_config'), 
                'launch/demo.launch.py')
        )
    )

    serial = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('pyconvo'), 
                'launch/serial.launch.py')
        )
    )
    
    pyconvo = Node(
        package='pyconvo',
        executable='convo')


    ld.add_action(panda)
    ld.add_action(serial)
    ld.add_action(pyconvo)
    return ld    

