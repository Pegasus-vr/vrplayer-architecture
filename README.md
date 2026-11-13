# vrplayer architecture

Primary views:

1. **User flow** — what the Quest wearer does
2. **Logic / behavior** — what the app does (states, decisions, events)
3. **Tech stack** — inventory poster (Blueprint A picks)

Also kept: how a VR clip gets to your eyes (pipeline story with eng labels + workspace strip), dense C4.

Site: https://pegasus-vr.github.io/vrplayer-architecture/

Rebuild:

```bash
python3 build-user-flow-diagram.py
python3 build-logic-behavior-diagram.py
python3 build-architecture-diagram.py
# tech-stack-diagram.png/.svg are the existing poster (no redesign)
```
