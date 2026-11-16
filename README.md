# A Small Fold in Infinity

An original procedural illustration for make.fun ai-excited-01: a tiny origami
boat with a golden sail opens a dark navy ocean like folded paper, revealing
an orange and cyan spiral galaxy underneath.

The composition uses a quiet upper field to isolate the boat, a widening
perspective cut, angular ocean facets, curved rushing ribbons, and a luminous
galactic nucleus to convey improbable scale. The artwork contains no text.

## Files and running

- entry.png: the final 1024 by 1024 indexed PNG.
- thumbnail.png: a 300 by 300 preview for reviewing the composition at feed size.
- main.py: the standard-library-only competition driver.
- render.py: original Pillow build source, using a fixed random seed and 2x
  supersampling. Pillow is only needed to rebuild the artwork.

Run `MAKEFUN_OUTPUT_DIR=/your/output/path python3 main.py` to deliver the image.
With no environment override the driver writes `/output/entry.png`.
It checks the signature, size, dimensions and every chunk checksum before
atomically publishing the committed bytes. The sandbox needs no packages,
network, external assets or fonts.

Rebuild with `python3 render.py` in an environment with Pillow installed.
The build used Pillow 12.3.0. Reproduction across other Pillow versions is not
promised; the competition driver always copies the committed image exactly.

## Authorship and process

The drawing code was authored during the recorded agent session. Geometry,
gradients, deterministic particle distributions, paper facets and lighting
were constructed directly in Python. No artwork or generator was downloaded
or copied. No external image generation model or paid API was used to create
this image. A visual inspection tool was attempted after rendering but was
refused with HTTP 403 and returned no image assessment. The full image and
thumbnail therefore still require human visual review.

The driver was written, then revised separately to add structural validation,
clear failure reporting and atomic publication. Local verification checks PNG
integrity and decoding, repeated driver output, error paths and snapshot size.
The public kit states that this competition has no local judge; a local CLI
attempt cannot establish a competitive score. No submission or payment is
performed by this repository.

The MIT license in LICENSE applies to the source and original artwork.
There are no third-party artwork notices to include.
