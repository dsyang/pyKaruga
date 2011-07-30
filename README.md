# pyKaruga: a 2D space shooter like IKaruga.

a python game written with pyGame and 2 player support because I can't find good vertical scrolling shooters.  

You control a special spaceship that has special "polarity" power. While enemy ships can only be one polarity (white or black), your ship can switch between the two.  

Your ship's shield system is also unique. If your ship is in white polarity and gets hit by a white bolt, it absorbs the energy and increases its shield power, but if it's hit by a black polarity bolt, its shields take a hit. The opposite happens when your ship is in black polarity.

Enemy ships however, are not as sophisticated as yours.  If they get hit by a bolt of of the same polarity, they will take damage.  However, if they are hit by a bolt of the opposite polarity, they will take double the damage!

Can you survive the onslaught? Find out by playing!

**Requirements:**

+  Python
+  pyGame

**Controls:**

Player 1:

+  Left/Right/Up/Down: arrow keys
+  Shoot: hold space bar
+  Switch polarity: b

Player 2:

+  Left/Right/Up/Down: a/d/w/s
+  Shoot: hold z
+  Switch polarity: x

Pause: RET(enter) key
Controls can be configured by changing the bindings in configs.py

**Enabling second player:**

Change NUM_PLAYERS in configs.py from 1 to 2
