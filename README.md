# Matrix Mesh

A minimal interactive elastic mesh desktop toy for Linux, inspired by the eerie green aesthetic of *The Matrix*.

Drag your mouse through the mesh and watch it ripple, stretch, and snap back with soft-body spring physics.

## Preview
(assets/image.png)
## Features

- Interactive elastic mesh
- Matrix-inspired neon green visual style
- Soft-body spring simulation
- Borderless desktop toy window
- Lightweight Python + Pygame setup
- Startup intro screen: **WELCOME TO THE MATRIX**

## Demo

The mesh reacts to mouse movement by applying force to nearby nodes.  
It uses:
- horizontal and vertical springs
- optional diagonal support springs
- damping for smooth settling
- return-to-base restoring force

## Tech Stack

- Python
- Pygame

## Run Locally

Clone the repo:

```bash
git clone https://github.com/adityakumar221210008/matrix-mesh.git
cd matrix-mesh
pip install -r requirements.txt
python3 main.py