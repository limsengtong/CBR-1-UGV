# Reference architectures: how other public UGVs are built

This document surveys publicly available UGV codebases to inform CBR-1's
design. It's meant to be read, not just linked to — the goal is to
understand *why* mature platforms are built the way they are, so CBR-1 can
follow the same reasoning rather than reinvent it.

## Clearpath Husky (the primary reference)

Repos: [`clearpath_common`](https://github.com/clearpathrobotics/clearpath_common),
[`clearpath_robot`](https://github.com/clearpathrobotics/clearpath_robot)
(both target ROS 2 Jazzy / Ubuntu 24.04 as of this writing). Husky is a
commercially deployed, actively maintained differential-drive UGV — the most
credible public reference for this kind of platform.

### The pattern

Husky's wheels are not driven by hand-written publisher/subscriber nodes.
Instead:

1. **A `ros2_control` hardware interface** (`clearpath_hardware_interfaces`)
   implements `hardware_interface::SystemInterface` — a standard C++ base
   class with lifecycle methods (`on_init`, `on_activate`, `read()`,
   `write()`). `read()` reports current wheel position/velocity from the
   motor controllers; `write()` sends commanded wheel velocities. This is
   the *only* place hardware-specific code (their CAN motor driver,
   `puma_motor_driver`) lives.
2. **`diff_drive_controller`** (a stock ROS 2 package, not custom code) sits
   on top of that hardware interface. It converts between wheel-level
   velocities and robot-level motion, and does three things automatically:
   - Publishes `/odom` (odometry) and the TF transform from it
   - Subscribes to `/cmd_vel` (standard robot velocity command topic)
   - Publishes `/joint_states` for the wheels
3. **URDF/xacro robot description** (`clearpath_description`) — an actual 3D
   model of the robot's physical shape, wheel positions, and dimensions.
   This is what lets RViz visualize the robot and what navigation/planning
   tools use to reason about the robot's footprint.
4. **`twist_mux`** arbitrates between multiple things that might try to
   drive the robot at once (joystick teleop, an autonomy stack, a safety
   stop) by priority, so they can't fight each other.
5. **`diagnostic_updater`/aggregator** (`clearpath_diagnostics`) — a
   standardized health-reporting pattern (battery, motor temperature, etc.)
   that plugs into common ROS 2 monitoring tools, instead of one-off custom
   topics.
6. **A YAML-driven config generator** (`clearpath_generator_common`) — since
   Clearpath ships several robot variants (Husky, Jackal, Warthog...) from
   one codebase, a single YAML file describing the robot's configuration
   generates the URDF, `ros2_control` config, and launch files. Not needed
   for a single-variant project, but worth knowing the pattern exists if
   CBR-1 ever has multiple hardware variants.

### Why this matters

The reason to do it this way, rather than custom topics like
`/robot/wheels/command/speed`, is **compatibility**: `/cmd_vel` and `/odom`
are what Nav2 (autonomous navigation), SLAM packages, `teleop_twist_keyboard`,
RViz's interactive markers, and simulators all expect out of the box. A
robot built on custom topics has to write a bridge/adapter for every one of
those tools individually; a robot built on `ros2_control` +
`diff_drive_controller` gets them for free.

## MobileRobots Pioneer

Community ROS 2 ports exist (e.g.
[`grupo-avispa/pioneer_ros2`](https://github.com/grupo-avispa/pioneer_ros2),
various university course projects), but none are an actively maintained,
authoritative reference the way Husky's stack is — mostly small, single-
purpose repos built for a specific course or paper. Worth knowing they
exist, but not a primary architecture reference.

## Other public platforms worth exploring

Not deep-researched yet (contributions welcome — see `CONTRIBUTING.md`):

- **TurtleBot3/4** — the official ROS reference platform, widely used in
  education specifically because the codebase is meant to be read.
- **Husarion ROSbot** — an open, education-oriented UGV with ROS 2 support.
- **AgileX Scout/Hunter** — common in academic/research fleets, ROS 2
  drivers available.

## What CBR-1 will follow

Based on the above, CBR-1's control stack should be built on:
- `ros2_control` for the drive motors (not custom pub/sub nodes)
- `diff_drive_controller` for odometry and `/cmd_vel`
- A URDF description of the actual chassis
- `diagnostic_updater` for health reporting
- `twist_mux` once there's more than one thing that can command motion (e.g.
  joystick + autonomy)

This is a deliberate departure from how the CAN motor control code was first
written for an earlier, related project (custom rclpy nodes, custom message
types) — that approach was right for a fast, faithful ROS 1 → ROS 2 port of
an existing working robot, but isn't the right foundation for a new
platform meant to plug into the wider ROS 2 ecosystem.
