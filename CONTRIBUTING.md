# Contributing to CBR-1 UGV

This is an early-stage, open, academic-research project — contributions of
all sizes are welcome, from fixing a typo in the docs to implementing a full
`ros2_control` hardware interface.

## Ways to contribute right now

- **Research**: extend `docs/reference-architectures.md` with other public
  UGV platforms (TurtleBot, Husarion ROSbot, AgileX, or others), or go
  deeper on the ones already listed.
- **Code**: once the base `ros2_control` scaffolding exists, driver
  implementations, simulation support, and navigation integration are all
  open.
- **Documentation**: setup guides, architecture explanations, diagrams.

## How to contribute

1. Open an issue describing what you want to work on before starting on
   anything non-trivial — helps avoid duplicate or conflicting effort this
   early in the project.
2. Fork the repo, make your changes on a branch, and open a pull request.
3. Keep PRs focused — one topic per PR is easier to review than a bundle of
   unrelated changes.
4. For code changes: explain *why* the change is needed, not just what it
   does, in the PR description.

## Code style

- Python: follow ROS 2's standard style (`ament_flake8`, `ament_pep257`) —
  the same conventions used throughout the ROS 2 ecosystem.
- C++: standard ROS 2 C++ style guide.

## Questions

Open an issue with the `question` label if anything about the project's
direction or architecture is unclear — that feedback also helps improve the
docs for the next person.
