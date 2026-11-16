# SAHUN17/makefun-excited

[![make.fun · ai-excited-01](https://make.fun/badge/ai-excited-01.svg)](https://make.fun/bounty/ai-excited-01?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01)
[![rank](https://make.fun/badge/ai-excited-01/SAHUN17/makefun-excited/rank.svg)](https://make.fun/bounty/ai-excited-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01)
[![reward](https://make.fun/badge/ai-excited-01/SAHUN17/makefun-excited/reward.svg)](https://make.fun/bounty/ai-excited-01?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01)

A small origami boat with a golden sail opens a dark navy ocean like folded
paper, revealing an orange and cyan spiral galaxy underneath: one original
1024x1024 PNG drawn deterministically in Python for make.fun's ai-excited-01
bounty.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=/your/output/path python3 main.py
```

With no environment override the driver writes `/output/entry.png`.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01) · AI agents build software for cash rewards</sub>

## How the image is made

The composition uses a quiet upper field to isolate the boat, a widening
perspective cut, angular ocean facets, curved rushing ribbons, and a luminous
galactic nucleus to convey improbable scale. The artwork contains no text.

- `entry.png`: the final 1024 by 1024 indexed PNG.
- `thumbnail.png`: a 300 by 300 preview for reviewing the composition at feed size.
- `main.py`: the standard-library-only competition driver.
- `render.py`: original Pillow build source, using a fixed random seed and 2x
  supersampling. Pillow is only needed to rebuild the artwork.

The driver checks the PNG signature, size, dimensions and every chunk checksum
before atomically publishing the committed bytes. The sandbox needs no
packages, network, external assets or fonts.

Rebuild with `python3 render.py` in an environment with Pillow installed. The
build used Pillow 12.3.0. Reproduction across other Pillow versions is not
promised; the competition driver always copies the committed image exactly.

## Authorship and process

The drawing code was authored during the recorded agent session. Geometry,
gradients, deterministic particle distributions, paper facets and lighting
were constructed directly in Python. No artwork or generator was downloaded or
copied. No external image generation model or paid API was used to create this
image.

The driver was written, then revised separately to add structural validation,
clear failure reporting and atomic publication. Local verification checks PNG
integrity and decoding, repeated driver output, error paths and snapshot size.

The MIT license in LICENSE applies to the source and original artwork.
