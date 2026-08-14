# cbr1_data_pipeline

Research data pipeline for CBR-1: record experiments as rosbag2 files with
reproducibility metadata, then export any topic to CSV for analysis outside
ROS.

This package only depends on standard ROS 2 topics (`/odom`, `/cmd_vel`,
`/imu/data`, etc.) — it works against a simulated robot today and the real
CBR-1 once its electronics are built, without changes.

## Recording an experiment

```bash
ros2 launch cbr1_data_pipeline record_experiment.launch.py \
    experiment_name:=slope_test_01 \
    notes:="testing incline behavior on 15deg ramp" \
    repo_path:=~/CBR-1-UGV
```

This creates `~/cbr1_experiments/<timestamp>_slope_test_01/` containing:
- `bag/` — the rosbag2 recording of the topics listed in `config/topics.yaml`
- `metadata.yaml` — who ran it, when, on what code commit, and your notes

`repo_path` is optional — pass it to record the exact git commit of the code
that produced the run, so results stay traceable back to what was actually
running.

`output_dir` defaults to `~/cbr1_experiments` and can be overridden the same way.

## Exporting a topic to CSV

```bash
ros2 run cbr1_data_pipeline bag_to_csv \
    ~/cbr1_experiments/20260101_120000_slope_test_01/bag \
    --topic /odom \
    --output odom.csv
```

Nested message fields (e.g. `pose.pose.position.x`) become flat CSV columns,
so the output loads directly into pandas, Excel, or any plotting tool.

## Customizing what gets recorded

Edit `config/topics.yaml`. The defaults match the standard interfaces CBR-1
is committing to (see the top-level `docs/reference-architectures.md`), so
this shouldn't need to change even as the electronics platform is decided.
