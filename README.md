# SyncMMH: A Multimodal Dataset of Full-Body Motion in Manual Material Handling Tasks Integrating Motion Capture and Vision-Based Pose Estimation

**SyncMMH** integrates motion capture and vision-based pose estimation for biomechanical analysis of manual material handling (MMH) tasks.

- **35,299 trials** (~27.7 hours) from **24 participants** (12 M, 12 F)
- **7 activities**: pushing, pulling, sitting, standing, walking, lifting, carrying
- **3 modalities**: 3D motion capture (ground truth), BlazePose 3D pose (22 keypoints, 5 views), metadata

![Dataset overview](figures/dataset_overview.png)

---

## Repository Structure

```
SyncMMH/
├── data/
│   └── metadata.txt             # trial identifiers and frame indices (559 KB)
├── figures/
│   ├── dataset_overview.png
│   ├── experimental_layout.png
│   ├── mocap_marker_placement.png
│   ├── blazepose_keypoints.png
│   ├── lifting_setup.png
│   └── task_overview.png
├── scripts/
│   ├── dataset_summary.py                 # trial/frame counts by activity, camera, subject
│   ├── visualize_mocap.py                 # 3D animated skeleton from motion capture
│   ├── visualize_pose.py                  # 2D multiview skeleton from pre-processed BlazePose keypoints
│   └── pose_pipeline_sample_multiview.py  # pose estimation + preprocessing + multiview render for data/sample videos/
├── visualization/                # generated multiview clips (see Visualization section)
├── examples/                    # Jupyter notebooks (coming soon)
├── LICENSE                      # CC BY 4.0
└── README.md
```

---

## Data Download

The large data files are hosted externally. See the [Modalities](#modalities) section below for download links and the folder structure to use after downloading.

| Component | Size | Format | Host |
|---|---|---|---|
| Motion capture | 304 GB | `.trc` | *(link to be added)* |
| Pose (all cameras) | 3.62 GB | `.txt` | *(link to be added)* |
| Metadata | 559 KB | `.txt` | Included in this repo |

---

## Experimental Setup

Five GoPro cameras and 14 infrared motion capture cameras were set up to provide 360° coverage of the participant performing MMH tasks.

![Experimental layout](figures/experimental_layout.png)

Seven tasks were recorded across five sessions: pushing, pulling, sitting, standing, walking, lifting, and carrying.

![Task overview](figures/task_overview.png)

---

## Dataset Summary

Generated with `scripts/dataset_summary.py` (excludes subject `s1`, a pilot session not included in the released trials):

**Totals:** 35,299 trials · 5,965,230 frames · 1,663.84 minutes (~27.7 hours)

**By activity**

| Activity | Trials | Frames | Duration (min) |
|---|---:|---:|---:|
| Push | 923 (2.61%) | 309,749 (5.19%) | 86.65 (5.21%) |
| Pull | 899 (2.55%) | 386,376 (6.48%) | 108.16 (6.50%) |
| Sit | 424 (1.20%) | 378,817 (6.35%) | 106.17 (6.38%) |
| Stand | 420 (1.19%) | 377,558 (6.33%) | 105.82 (6.36%) |
| Walk | 2,950 (8.36%) | 753,706 (12.63%) | 210.65 (12.66%) |
| Lift | 27,632 (78.28%) | 3,297,700 (55.28%) | 917.53 (55.15%) |
| Carry | 2,051 (5.81%) | 461,324 (7.73%) | 128.86 (7.74%) |

**By camera**

| Camera | Trials | Frames | Duration (min) |
|---|---:|---:|---:|
| c1 | 7,499 (21.24%) | 1,249,279 (20.94%) | 348.42 (20.94%) |
| c2 | 7,196 (20.39%) | 1,233,744 (20.68%) | 344.15 (20.68%) |
| c3 | 7,331 (20.77%) | 1,252,018 (20.99%) | 349.24 (20.99%) |
| c4 | 6,249 (17.70%) | 1,093,355 (18.33%) | 305.02 (18.33%) |
| c5 | 7,024 (19.90%) | 1,136,834 (19.06%) | 317.01 (19.05%) |

Lifting dominates the trial count because each lift/carry repetition (a single pick-up-and-place motion) is logged as its own trial, while push/pull/sit/stand/walk trials span a longer continuous action.

---

## Quick Start

```bash
# Dataset summary — trial/frame counts by activity, camera, and subject
cd scripts
python dataset_summary.py

# Visualize a motion capture trial (motion capture data not yet released)
# python visualize_mocap.py <path_to.trc> <start_frame> <end_frame>
```

---

## File Naming Convention

All trials in `data/metadata.txt` follow this identifier format:

```
[activity]_[camera]-[subject]-[task_params]-[filename]
```

**Example:** `lift_c1-s1-sr2laf-GH010014`

| Field | Values |
|---|---|
| `activity` | `push`, `pull`, `sit`, `stand`, `walk`, `lift`, `carry` |
| `camera` | `c1`–`c5` |
| `subject` | `s1`–`s25` |
| `task_params` (push/pull) | `gc` (getting close), `gf` (getting far) |
| `task_params` (sit/stand) | `na` |
| `task_params` (walk) | `gc`/`gf` + `cv` (close-up) / `rv` (regular) |
| `task_params` (lift/carry) | `[size][direction][location][cam]` — e.g., `sr2laf` = small, right-to-left, adjacent shelf, fixed camera |
| `filename` | GoPro video filename (e.g., `GH010014`) |

The line immediately below each identifier gives `start_frame/end_frame` (1-based). Lifting and carrying trials may have multiple frame-index lines per identifier.

---

## Gallery

Multiview clips generated end-to-end from raw video via `scripts/pose_pipeline_sample_multiview.py` — pose estimation and preprocessing use the same settings as `n1_pose_estimation.py`/`n2_pre_processing.py`, cameras are auto-synced by cross-correlating joint motion across views, and all 5 cameras are rendered side by side in `c4, c5, c1, c2, c3` order. Example identifiers below use subject `s25`; see [File Naming Convention](#file-naming-convention) for what each field means.

**Push** — `c1-s25-gf`
![push multiview](visualization/push_multiview.gif)

**Pull** — `c1-s25-gc`
![pull multiview](visualization/pull_multiview.gif)

**Sit** — `c1-s25-na`
![sit multiview](visualization/sit_multiview.gif)

**Stand** — `c1-s25-na`
![stand multiview](visualization/stand_multiview.gif)

**Walk** — `c1-s25-gfrv`
![walk multiview](visualization/walk_multiview.gif)

**Lift** — `c1-s25-sr2laf`
![lift multiview](visualization/lift_multiview.gif)

**Carry** — `c1-s25-lr2ldf`
![carry multiview](visualization/carry_multiview.gif)

---

## Modalities

### 1. Motion Capture (`.trc`)

3D motion capture recordings in `.trc` format (304 GB total). Download from: *(link to be added)*

After downloading, create a `data/motion_capture/` folder and place files so the structure looks like:

```
data/motion_capture/
├── s01/
│   ├── session1_push_pull.trc
│   ├── session2_sit_stand.trc
│   ├── session3_walk.trc
│   ├── session4_lift.trc
│   └── session5_carry.trc
├── s02/
└── ...
└── s24/
```

- **System**: Motion Analysis Cortex v7, 14 infrared cameras, 60 Hz
- **Markers**: 37 reflective markers (ISB placement)
- **Coordinate system**: Origin at force plate intersection; X = mediolateral, Y = vertical, Z = anterior-posterior (mm)

![Marker placement](figures/mocap_marker_placement.png)

Thirty-seven reflective markers were attached to anatomical landmarks following ISB recommendations. The coordinate origin is defined as the intersection of the four force plates on the ground.

| Index | Marker | Index | Marker |
|-------|--------|-------|--------|
| 1 | Forehead | 2–3 | Temples (R/L) |
| 4–5 | Acromions (R/L) | 6 | C7 (base of neck) |
| 7 | Suprasternal notch | 8 | T8 (mid-back) |
| 9 | Xiphoid process | 10–11 | Lateral epicondyles (R/L) |
| 12–13 | Medial epicondyles (R/L) | 14–15 | Radial styloids (R/L) |
| 16–17 | Ulnar styloids (R/L) | 18–19 | ASIS (R/L) |
| 20–21 | PSIS (R/L) | 22–23 | Patellae (R/L) |
| 24–25 | Lateral tibial condyles (R/L) | 26–27 | Medial tibial condyles (R/L) |
| 28–29 | Lateral malleoli (R/L) | 30–31 | Medial malleoli (R/L) |
| 32–33 | Big toes (R/L) | 34–35 | Calcanei / Heels (R/L) |
| 36–37 | Right-side identifiers | | |

Five cameras were mounted on tripods at 1.4 m height, providing 360° coverage. Motion capture was recorded simultaneously at 60 Hz. For lifting tasks (Session 4), participants lifted three box sizes between two adjacent five-level shelves (small/medium) or four-level shelves (large).

![Lifting setup](figures/lifting_setup.png)

See `scripts/visualize_mocap.py` for visualization.

### 2. Vision-Based 3D Pose (`.txt`)

BlazePose 3D keypoint data in `.txt` format (3.62 GB total), organized by camera view. Download from: *(link to be added)*

After downloading, create a `data/pose/` folder and place files so the structure looks like:

```
data/pose/
├── c1/                  # Camera 1: 0° / 180°
│   ├── s01/
│   │   ├── <recording>.txt
│   │   └── ...
│   └── ...
├── c2/                  # Camera 2: 45° / 225°
├── c3/                  # Camera 3: 90° / 270°
├── c4/                  # Camera 4: 270° / 90°
└── c5/                  # Camera 5: 315° / 135°
```

- **Model**: Google BlazePose (22 keypoints)
- **Cameras**: 5 × GoPro Hero8 Black, 1920×1080, 60 Hz, 360° coverage
- **Per row**: 66 values = 22 keypoints × 3 (X, Y, Z in meters)
- **Shape after loading**: `(n_frames, 22, 3)`
- **Coordinate system**: Origin at hip midpoint; X = mediolateral, Y = vertical, Z = anterior-posterior (m)
- **Preprocessing**: Zero-phase 5th-order Butterworth low-pass filter at 5 Hz

![BlazePose 22 keypoints](figures/blazepose_keypoints.png)

Twenty-two key body joints were extracted per frame using Google BlazePose. The coordinate origin (red dot) is defined as the midpoint between the hips.

| Index | Joint | Index | Joint |
|---|---|---|---|
| 0 | L shoulder | 1 | R shoulder |
| 2 | L elbow | 3 | R elbow |
| 4 | L wrist | 5 | R wrist |
| 6 | L pinky knuckle | 7 | R pinky knuckle |
| 8 | L index knuckle | 9 | R index knuckle |
| 10 | L thumb knuckle | 11 | R thumb knuckle |
| 12 | L hip | 13 | R hip |
| 14 | L knee | 15 | R knee |
| 16 | L ankle | 17 | R ankle |
| 18 | L heel | 19 | R heel |
| 20 | L index toe | 21 | R index toe |

See `scripts/visualize_pose.py` for visualization.

### 3. Metadata (`data/metadata.txt`)
- Trial identifiers encoding activity, camera, subject, and task parameters
- Start/end frame indices for each trial (1-based)

---

## Citation

If you use SyncMMH in your research, please cite:

```bibtex
@article{jung2026syncmmh,
  title   = {SyncMMH: A Multimodal Dataset of Full-Body Motion in Manual Material
             Handling Tasks Integrating Motion Capture and Vision-Based Pose Estimation},
  author  = {Jung, Sehee and Xu, Xu},
  journal = {[journal to be added]},
  year    = {2026}
}
```

---

## License

This dataset is released under the [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE) license.
