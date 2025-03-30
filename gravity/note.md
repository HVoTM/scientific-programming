# How pymunk works
## Space
- An area where physics is calculated
- Continuously update the simulation

## Physical objects
- Body: an atom that is affected by physics
- Shape: an area around the body that can collide

## Physical bodies in pymunk
- Static body: A body that doesn't move but other bodies can collide with it
- Dynamic body: A body that can be moved by physics
- Kinematic body: A body that can be moved by the player (or other non-physical code)
