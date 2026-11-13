# vrplayer architecture

Primary views:

<<<<<<< HEAD
Primary: five-step gold path (file → decode → JNI → place → eyes) with short eng labels + thin workspace strip.
Secondary: dense C4 container poster + tech-stack inventory.
=======
1. **User flow** — what the Quest wearer does
2. **Logic / behavior** — what the app does (states, decisions, events)

Also kept: how a VR clip gets to your eyes (pipeline story), dense C4, tech-stack inventory.
>>>>>>> pegasus/user-flow-logic-diagrams-856a

Site: https://pegasus-vr.github.io/vrplayer-architecture/

Rebuild:

```bash
python3 build-user-flow-diagram.py
python3 build-logic-behavior-diagram.py
python3 build-architecture-diagram.py
```
