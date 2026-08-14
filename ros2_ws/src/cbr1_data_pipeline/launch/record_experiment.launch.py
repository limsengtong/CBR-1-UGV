"""Records a research run: a rosbag2 of standard topics + a metadata.yaml
describing who ran it, when, on what code commit, and why (free-text notes).

Usage:
    ros2 launch cbr1_data_pipeline record_experiment.launch.py \
        experiment_name:=slope_test_01 \
        notes:="testing incline behavior on 15deg ramp"
"""

import datetime
import os
from pathlib import Path

import yaml
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, OpaqueFunction
from launch.substitutions import LaunchConfiguration

from cbr1_data_pipeline.experiment_metadata import write_metadata


def _launch_setup(context, *args, **kwargs):
    experiment_name = LaunchConfiguration('experiment_name').perform(context)
    notes = LaunchConfiguration('notes').perform(context)
    output_root = Path(LaunchConfiguration('output_dir').perform(context)).expanduser()
    repo_path_arg = LaunchConfiguration('repo_path').perform(context)

    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_name = experiment_name.replace(' ', '_') or 'unnamed'
    run_dir = output_root / f'{timestamp}_{safe_name}'
    bag_path = run_dir / 'bag'

    repo_path = Path(repo_path_arg).expanduser() if repo_path_arg else None
    metadata_path = write_metadata(run_dir, experiment_name, notes, repo_path=repo_path)
    print(f'Recording experiment "{experiment_name}" -> {run_dir}')
    print(f'Metadata written to {metadata_path}')

    topics_yaml = os.path.join(
        get_package_share_directory('cbr1_data_pipeline'), 'config', 'topics.yaml')
    with open(topics_yaml) as f:
        topics = yaml.safe_load(f)['topics']

    record_process = ExecuteProcess(
        cmd=['ros2', 'bag', 'record', '-o', str(bag_path), *topics],
        output='screen',
    )

    return [record_process]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'experiment_name', default_value='unnamed',
            description='Short name for this run, used in the output folder name'),
        DeclareLaunchArgument(
            'notes', default_value='',
            description='Free-text notes about this run (conditions, what changed, etc.)'),
        DeclareLaunchArgument(
            'output_dir', default_value='~/cbr1_experiments',
            description='Root directory experiment runs are saved under'),
        DeclareLaunchArgument(
            'repo_path', default_value='',
            description='Path to this repo checkout, to record the code commit hash in metadata.yaml (optional)'),
        OpaqueFunction(function=_launch_setup),
    ])
