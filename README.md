# Sidney Holden's personal website

A small academic homepage for GitHub Pages. The publishable site is in `docs/`.
It uses ordinary HTML and CSS, with no installation or build step.

## Edit

- `docs/index.html`: biography, research descriptions, citations, and links.
- `docs/assets/style.css`: typography, spacing, colors, and responsive layout.
- `docs/assets/media/`: the portrait, research movies, poster frames, and retained still figures.

The research descriptions use Sidney's approved wording. The two preprints are
labeled under review; the Dedalus manuscript is labeled in preparation. The
continuum preprint is listed with its 2025 revision year. A CV and Scholar profile
can be added when their final file and URL have been selected.

## Preview

From this repository, run:

```sh
python3 -B tools/preview.py
```

Open the printed address. This serves only `docs/`, and does not publish anything.
Refresh after edits. Stop the server with Ctrl-C when finished reviewing.

## Publish with GitHub Pages

1. Create a public repository named `sidneyholden1.github.io` under the
   `sidneyholden1` account, with a README so that a `main` branch exists.
2. Add this README and the complete `docs/` directory to that repository.
   The optional `tools/` directory contains local preview and scientific-media tooling.
3. In **Settings → Pages**, choose **Deploy from a branch**, then select
   **main** and **/docs**, and save.
4. GitHub will show the website address and deployment status. After a successful
   deployment, the site will be at https://sidneyholden1.github.io/.

Subsequent changes to `docs/` on the publishing branch update the website.
The `.nojekyll` file tells GitHub to serve these files without processing them
as a Jekyll site. No custom domain is required.

Official instructions:
https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

## Content sources

- Continuum preprint: https://arxiv.org/abs/2301.07086
- Adaptive-network preprint: https://arxiv.org/abs/2605.16130
- Biography: https://www.simonsfoundation.org/people/sidney-holden/
- Portrait: photograph supplied by Sidney Holden.
- Research movies and figures: existing author-supplied project assets.

The three research sections use inline videos with still previews, native
playback controls, and no autoplay. After pressing play, each video loops.
Full-screen playback is available through the native controls.

- `spherical-network.mp4`: the original spherical-network simulation, unchanged.
- `network-flux.mp4`: the actual J_z panel from `fields_run1000.mp4`, registered
  frame by frame into a fixed plotting area. This corrects movement caused by
  the source figure's automatic layout as colour-bar labels change. The field
  has room around its edges, a small centered “Vertical flux (t = …)” title,
  and its original colour-bar values. Coordinate axes are removed. Saturation
  is increased by 25% in both the field and colour scale. All 415 frames and
  their original timing and per-frame colour limits are retained. Displayed
  integer times match the saved simulation timestamps.
- `nls-sphere-lead.mp4`: a fresh render of the saved focusing NLS (g = -5)
  complex fields. The graph and straight lead are drawn at the output resolution
  on white, with antialiased spherical arcs and Chebyshev interpolation along
  each edge. A fixed power-0.12 density colour scale makes weak propagation
  visible; the maximum is the saved trajectory's global maximum density.
  Smoothly shaded circular tubes show the pulse magnitude through their
  thickness. Their display radius is `0.082 * abs(psi) / (abs(psi) + 0.4)` in
  sphere-radius units: an exaggerated, fixed scale that keeps weaker pulses
  visible without changing the graph geometry or normalizing each frame.
  Tube surfaces use the interpolated saved field, with smooth lighting and
  depth ordering. The rear hemisphere is faded. The orthographic camera and
  small centered “Focusing NLS” title stay fixed. All 801 saved times and the original playback
  rate are retained. The simulation has a finite 12R lead with a reflecting far
  end; only 3R of that lead is visible. This illustration does not claim an
  open-lead limit.

The two edited videos use H.264 with MP4 metadata placed first for fast playback.
These are presentation exports of existing results, with no new simulation.
Original research files are preserved separately.

Each poster is a frame from its corresponding video. The former still figures
remain in the media folder for future edits. The effective-dimension still uses
an approximate plasma-to-cividis raster palette remap; the optional
`tools/recolor_network_figure.py` records that process. Original plotting code:
https://github.com/sidneyholden1/laplace_operator_metric_graph.

No analytics, third-party scripts, external fonts, or runtime dependencies are
required by the website. The optional palette script uses NumPy, SciPy,
Matplotlib, and Pillow in an existing scientific Python environment.
The optional `tools/render_research_media.py` records the animation presentation
settings; rebuilding those movies requires the author's saved fields, h5py,
Matplotlib, Pillow, NumPy, FFmpeg, and the private cluster rendering controls.
