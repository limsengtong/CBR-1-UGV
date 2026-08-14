#!/usr/bin/env python3
"""Export a topic from a recorded rosbag2 into CSV, for analysis outside ROS
(pandas, Excel, plotting, whatever the research actually needs).

Usage:
    ros2 run cbr1_data_pipeline bag_to_csv <bag_path> --topic /odom --output odom.csv
"""

import argparse
import csv
import pathlib

import rosbag2_py
from rclpy.serialization import deserialize_message
from rosidl_runtime_py import message_to_ordereddict
from rosidl_runtime_py.utilities import get_message


def _read_bag(bag_path: pathlib.Path, topic: str):
    storage_options = rosbag2_py.StorageOptions(uri=str(bag_path), storage_id='sqlite3')
    converter_options = rosbag2_py.ConverterOptions('', '')
    reader = rosbag2_py.SequentialReader()
    reader.open(storage_options, converter_options)

    type_map = {t.name: t.type for t in reader.get_all_topics_and_types()}
    if topic not in type_map:
        raise ValueError(
            f"Topic '{topic}' not found in bag. Available topics: {sorted(type_map)}")

    reader.set_filter(rosbag2_py.StorageFilter(topics=[topic]))
    msg_type = get_message(type_map[topic])

    while reader.has_next():
        _, data, timestamp_ns = reader.read_next()
        yield timestamp_ns, deserialize_message(data, msg_type)


def _flatten(prefix, value, out):
    if isinstance(value, dict):
        for k, v in value.items():
            _flatten(f'{prefix}.{k}' if prefix else k, v, out)
    elif isinstance(value, (list, tuple)):
        for i, v in enumerate(value):
            _flatten(f'{prefix}[{i}]', v, out)
    else:
        out[prefix] = value


def _flatten_message(msg) -> dict:
    """Flatten a ROS message (nested fields, arrays) into flat CSV column names."""
    out = {}
    _flatten('', message_to_ordereddict(msg), out)
    return out


def export_topic_to_csv(bag_path: pathlib.Path, topic: str, output_path: pathlib.Path):
    rows = []
    for timestamp_ns, msg in _read_bag(bag_path, topic):
        row = {'timestamp_ns': timestamp_ns}
        row.update(_flatten_message(msg))
        rows.append(row)

    if not rows:
        print(f"No messages found on topic '{topic}' — nothing written.")
        return

    fieldnames = sorted({k for row in rows for k in row})
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f'Wrote {len(rows)} rows ({len(fieldnames)} columns) to {output_path}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bag_path', help='Path to the rosbag2 directory (the one containing metadata.yaml + .db3 file)')
    parser.add_argument('--topic', required=True, help='Topic to export, e.g. /odom')
    parser.add_argument('--output', required=True, help='Output CSV path')
    args = parser.parse_args()

    export_topic_to_csv(pathlib.Path(args.bag_path), args.topic, pathlib.Path(args.output))


if __name__ == '__main__':
    main()
