# Research data pipeline

The first real code in this repo, `ros2_ws/src/cbr1_data_pipeline`, isn't
drive/lighting/sensor control — it's tooling for turning robot runs into
research output. The reasoning behind that choice:

## Why this, and why now

CBR-1's electronics platform isn't decided yet, which blocks writing real
hardware control code (see `docs/decisions.md`). But data pipeline tooling
doesn't depend on hardware specifics — it only cares about standard ROS 2
topics (`/odom`, `/cmd_vel`, `/imu/data`, etc.), the same interfaces this
project has already committed to following (see
`docs/reference-architectures.md`). That means it's genuinely useful *today*,
against a simulated robot, and stays useful unchanged once real hardware
exists.

## What it does

1. **Records experiments**, not just raw data — every run gets a
   `metadata.yaml` alongside the rosbag: who ran it, when, on what exact
   code commit, and free-text notes about conditions. This is the difference
   between "a folder of logs" and something citable in a paper: six months
   from now, a recording is traceable back to exactly what code produced it.
2. **Exports to CSV** — rosbag2's native format isn't directly usable in
   pandas/Excel/most plotting tools. `bag_to_csv` flattens any topic
   (including nested message fields) into a CSV, so analysis doesn't require
   staying inside the ROS ecosystem.
3. **Stays hardware-agnostic** — the topic list in `config/topics.yaml`
   matches the standard interfaces from the architecture doc, not
   CBR-1-specific topic names, so this doesn't need rework as hardware
   decisions land.

See `ros2_ws/src/cbr1_data_pipeline/README.md` for actual usage.

## What's still missing

This is recording/export tooling, not analysis. It doesn't (yet) include
example notebooks, standard plots (velocity profiles, terrain response), or
a way to compare multiple runs against each other. Good next contribution
for anyone picking this up.
