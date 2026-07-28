# Open decisions

Things blocking real progress that need an answer before code gets written,
tracked here so they don't get lost between conversations.

## Electronics platform (blocking wheel/light/sensor control code)

**Status: open, as of this writing CBR-1's electronics are not finalized.**

There's a private, related codebase (for a different robot — an arm-equipped
demining platform, not CBR-1) with working ROS 2 wheel control, light
control, and motherboard/temperature-sensing code. It's tempting to reuse
it, but it won't actually work for CBR-1 as-is: it's written against a
specific CAN bus protocol tied to that robot's own custom PCBs (arbitration
IDs, byte-scaling factors, motor controller addresses). Contract/SOW
references suggest CBR-1 may end up on different electronics entirely
(ESP32-based rather than CAN), which would mean a different communication
protocol from the ground up (e.g. serial/WiFi instead of CAN).

Copying that code over now would produce something that *looks* like
working wheel/light/temperature control but silently doesn't talk to real
hardware — worse than having no code, since it hides the actual gap.

**Once CBR-1's electronics are decided**, the useful thing to reuse from
that other codebase isn't the CAN protocol specifics — it's the **ROS 2
architecture pattern**: how control is split into nodes (drive, lighting,
sensing), what topics/message types they publish, and the
timer-callback-based control loop structure. See
`docs/reference-architectures.md` for the broader design direction (this
project should move toward `ros2_control` + `diff_drive_controller` rather
than copying that pattern verbatim anyway).

**Next step**: once the electronics platform is chosen, revisit this and
scope the actual driver work.
