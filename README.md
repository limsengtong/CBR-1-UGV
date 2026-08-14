# CBR-1 UGV

An open, ROS 2-based unmanned ground vehicle (UGV) base platform, built for
academic research and open collaboration.

CBR-1 is a **base platform only** — drive, sensing, and control. It has no
arm or manipulator. The goal is a modern, well-documented reference stack
that's actually useful to study: built to the same architectural patterns
used by established open UGV platforms (Clearpath Husky and others), with
the reasoning for those choices written down, not just the code.

## Status

Early stage. Architecture research is written up in
[`docs/reference-architectures.md`](docs/reference-architectures.md) — a
comparison of how other public UGV platforms (Clearpath Husky and others)
are built, and what CBR-1 will follow.

CBR-1's electronics platform isn't finalized yet, which currently blocks
writing real drive/lighting/sensor code — see
[`docs/decisions.md`](docs/decisions.md) for why, and what's reusable from
elsewhere once that's settled.

## What's actually here

- **[`ros2_ws/src/cbr1_data_pipeline`](ros2_ws/src/cbr1_data_pipeline)** —
  the first real code in this repo. Records robot experiments (rosbag2 +
  reproducibility metadata: who/when/what code/notes) and exports topics to
  CSV for analysis. Hardware-agnostic by design — see
  [`docs/research-data-pipeline.md`](docs/research-data-pipeline.md) for why
  this was the right first thing to build while the electronics decision is
  still open.

## Why this exists

Most UGV codebases you can find publicly are either full commercial stacks
(hard to learn from — deeply tied to specific hardware) or toy examples (too
simple to reflect how a real robot is actually built). CBR-1 aims to sit in
between: real architecture (ros2_control, standard ROS 2 interfaces,
diagnostics), documented clearly enough for someone studying robotics to
follow along and contribute.

## Contributing

Contributions are welcome — see [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

MIT — see [`LICENSE`](LICENSE).
