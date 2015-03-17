# Pyxis

Shrishti 2014 project on smart whiteboard.

Uses SVM + HoG for handwriting detection and does stuff.

### Caveats

This source is full of super *dumb* decisions like

- Using a dictionary dump of `A => 0, B => 1 ...` relations while remaining completely ignorant of `ord()` and `chr()`.
- Kick-ass (and really bad) numpy indexing.
- and many more . . . go on, explore the code.

But, lets just keep it that way. Fixing old code is painful.
