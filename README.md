# CBR-1 UGV

An open, ROS 2-based unmanned ground vehicle (UGV) base platform, built for
academic research and open collaboration.

CBR-1 is a **base platform only** — drive, sensing, and control. It has no
arm or manipulator. The goal is a modern, well-documented reference stack
that's actually useful to study: built to the same architectural patterns
used by established open UGV platforms (Clearpath Husky and others), with
the reasoning for those choices written down, not just the code.

## Status

Early stage. Right now this repo contains architecture research and project
scaffolding — see [`docs/reference-architectures.md`](docs/reference-architectures.md)
for a detailed comparison of how other public UGV platforms are built and
what CBR-1 will follow. Actual ROS 2 packages land here as they're built.

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
