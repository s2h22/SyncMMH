# SyncMMH: A Multimodal Dataset of Full-Body Motion in Manual Material Handling Tasks Integrating Motion Capture and Vision-Based Pose Estimation

**SyncMMH** integrates motion capture and vision-based pose estimation for biomechanical analysis of manual material handling (MMH) tasks.

- **35,299 trials** (~27.7 hours) from **24 participants** (12 M, 12 F)
- **7 activities**: pushing, pulling, sitting, standing, walking, lifting, carrying
- **3 modalities**: 3D motion capture (ground truth), vision-based 3D pose (BlazePose, 22 keypoints), metadata

![Dataset overview](figures/dataset_overview.png)

Generated with `scripts/dataset_summary.py` (excludes subject `s1`, a pilot participant not part of the 24 released participants); **5,965,230 frames** total. Lifting dominates the trial count because each lift/carry trial is a single pick-up-and-place motion, while push/pull/sit/stand/walk trials span a longer continuous action.

---

## Gallery

Multiview clips: all 5 camera views of the same trial, synchronized and arranged side by side in `c4, c5, c1, c2, c3` order. Each clip below is captioned with its trial identifier (subject `s25` and task parameters); see [File Naming Convention](#file-naming-convention) for what each task parameter means.

**Push** — `s25-gf`
![push multiview](visualization/push_multiview.gif)

**Pull** — `s25-gc`
![pull multiview](visualization/pull_multiview.gif)

**Sit** — `s25-na`
![sit multiview](visualization/sit_multiview.gif)

**Stand** — `s25-na`
![stand multiview](visualization/stand_multiview.gif)

**Walk** — `s25-gfrv`
![walk multiview](visualization/walk_multiview.gif)

**Lift** — `s25-sr2laf`
![lift multiview](visualization/lift_multiview.gif)

**Carry** — `s25-lr2ldf`
![carry multiview](visualization/carry_multiview.gif)

---

## Data Download

The large data files are hosted externally. See the [Modalities](#modalities) section below for download links and the folder structure to use after downloading.

| Component | Size | Format | Host | Remark |
|---|---|---|---|---|
| Motion capture | 304 GB | `.trc` + Cortex-associated files | Available upon request — contact the first author ([apps.ehee@gmail.com](mailto:apps.ehee@gmail.com)) | `.trc` (coordinate data) plus Cortex auxiliary files (`.add`, `.cap`, `.trb`) and mocap camera video (`.avi`) |
| Pose (all cameras) | 1.80 GB (zipped) | `.txt` | [Google Drive](https://drive.google.com/file/d/1zpLqrGyzlRVKZg8QC4l3IDiTPQ7q8J5y/view?usp=sharing) | 4 files after unzipping: `raw_poses_3d_normalized.txt` (1.76 GB), `raw_poses_3d_world.txt` (1.85 GB), `pre_processed_poses_3d_normalized.txt` (1.82 GB), `pre_processed_poses_3d_world.txt` (1.91 GB) |
| Metadata | 559 KB | `.txt` | Included in this repo (`data/metadata.txt`) | |

---

## Experimental Setup

Five GoPro Hero8 Black cameras (1920×1080, 60 Hz, 122.6° horizontal / 94.4° vertical FOV) and a 14-camera infrared motion capture system (Cortex v7.02.1815, Motion Analysis Corp.) were mounted on tripods at 1.4 m height to provide 360° coverage — front, back, diagonal, and side views — of the participant performing MMH tasks.

![Experimental layout](figures/experimental_layout.png)

Seven tasks were recorded across five sessions (with a 10-min break between sessions): pushing and pulling a cart, sitting and standing, walking, lifting, and carrying.

![Task overview](figures/task_overview.png)

---

## Quick Start

```bash
# Dataset summary — trial/frame counts by activity, camera, and subject
cd scripts
python dataset_summary.py
```

---

## File Naming Convention

The activity and experimental conditions for each trial are encoded into a **trial identifier** in `data/metadata.txt`, following this format:

```
[activity]_[camera]-[subject]-[task parameters]-[filename]
```

**Example:** `lift_c1-s1-sr2laf-GH010014` — a lifting trial using a small box, moved right-to-left, at an adjacent shelf location, recorded by fixed cameras.

| Field | Values |
|---|---|
| `activity` | `push`, `pull`, `sit`, `stand`, `walk`, `lift`, `carry` |
| `camera` | `c1`–`c5` |
| `subject` | `s2`–`s25` |
| `filename` | GoPro video filename (e.g., `GH010014`) |

**`task parameters`** — the tag's structure depends on the activity:

| Activity | Tag structure | Values |
|---|---|---|
| Push / Pull | `[relation]` | `gc` (getting close) or `gf` (getting far) — spatial relationship of the participant to Camera 3, positioned in front of the path |
| Sit / Stand | `na` | No task parameters apply; the tag is fixed as non-applicable |
| Walk | `[relation][view]` | `relation`: `gc`/`gf` as above. `view`: `cv` (close-up view, cameras repositioned 2 m from the path center for the second half of the walking trials) or `rv` (regular view, default camera positions) |
| Lift / Carry | `[size][direction][location][state]` | `size`: `s` (small), `m` (medium), `l` (large). `direction`: `r2l` (right-to-left) or `l2r` (left-to-right). `location`: `a` (adjacent shelves) or `d` (distant shelves). `state`: `f` (fixed cameras) or `m` (moving cameras) |

Immediately below each trial identifier, one or more `start_frame/end_frame` lines (1-based) mark each trial's extent. Lifting and carrying tasks involve multiple trials per recording, so their identifiers are followed by multiple frame-index lines; every other task consists of a single trial with just one line.

---

## Modalities

Raw multi-view video (1.24 TB, 5-camera 360° coverage — see [Experimental Setup](#experimental-setup) for the camera specs) is part of the original data collection but isn't distributed as its own downloadable component, since participants are identifiable in it; the 3 modalities below are.

### 1. Motion Capture (`.trc`)

3D motion capture data (304 GB total, `.trc` and Cortex-associated files). Available upon request — contact the first author ([apps.ehee@gmail.com](mailto:apps.ehee@gmail.com)).

- **System**: Cortex v7.02.1815 (Motion Analysis Corp.), 14 infrared cameras, 60 Hz
- **Markers**: 37 reflective markers (ISB placement; [Wu et al., 2002](https://doi.org/10.1016/S0021-9290(01)00222-6), [2005](https://doi.org/10.1016/j.jbiomech.2004.05.042))
- **Coordinate system**: Origin at force plate intersection; X = mediolateral, Y = vertical, Z = anterior-posterior (mm)

![Marker placement](figures/mocap_marker_placement.png)

Thirty-seven reflective markers were attached to anatomical landmarks following ISB recommendations. The coordinate origin is defined as the intersection of the four force plates on the ground.

| Index | Marker | Index | Marker |
|-------|--------|-------|--------|
| 1 | Forehead | 2/3 | Temple (R/L) |
| 4/5 | Acromion — shoulder points (R/L) | 6 | C7 — spinous process of the 7th cervical vertebra (base of neck) |
| 7 | Suprasternal notch (base of throat) | 8 | T8 — spinous process of the 8th thoracic vertebra (mid-back, below shoulder blades) |
| 9 | Xiphoid process (bottom tip of breastbone) | 10/11 | Lateral epicondyle — outer elbows (R/L) |
| 12/13 | Medial epicondyle — inner elbows (R/L) | 14/15 | Radial styloid — wrists, thumb side (R/L) |
| 16/17 | Ulnar styloid — wrists, pinky side (R/L) | 18/19 | ASIS — anterior superior iliac spine, front of hip bones (R/L) |
| 20/21 | PSIS — posterior superior iliac spine, lower back dimples (R/L) | 22/23 | Patella — kneecaps (R/L) |
| 24/25 | Lateral tibial condyle — outer upper shins (R/L) | 26/27 | Medial tibial condyle — inner upper shins (R/L) |
| 28/29 | Lateral malleolus — outer ankle bones (R/L) | 30/31 | Medial malleolus — inner ankle bones (R/L) |
| 32/33 | Big toe (R/L) | 34/35 | Calcaneus — heels (R/L) |
| 36/37 | Right-side identifiers | | |

Motion capture was recorded simultaneously with video at 60 Hz. For lifting tasks (Session 4), participants lifted three box sizes between two adjacent five-level shelves (small/medium) or four-level shelves (large).

![Lifting setup](figures/lifting_setup.png)

### 2. Vision-Based 3D Pose (`.txt`)

BlazePose 3D keypoint data, covering all 5 camera views (1.80 GB zipped). Download from [Google Drive](https://drive.google.com/file/d/1zpLqrGyzlRVKZg8QC4l3IDiTPQ7q8J5y/view?usp=sharing).

After downloading, unzip directly into `data/` so the structure looks like:

```
data/
├── raw_poses_3d_normalized.txt
├── raw_poses_3d_world.txt
├── pre_processed_poses_3d_normalized.txt
└── pre_processed_poses_3d_world.txt
```

- **Model**: Google BlazePose (22 keypoints)
- **Cameras**: 5 × GoPro Hero8 Black, 1920×1080, 60 Hz, 360° coverage — all 5 views are combined into each file; which camera a block of frames came from is encoded in that block's trial identifier (see [File Naming Convention](#file-naming-convention))
- **Per row**: 66 values = 22 keypoints × 3 (X, Y, Z)
- **Shape after loading**: `(n_frames, 22, 3)`
- **Coordinate system**: Origin at hip midpoint; X = mediolateral, Y = vertical, Z = anterior-posterior (m for `_world`, image-space for `_normalized` — see below)
- **`raw_` vs `pre_processed_`**: `raw_` is the direct BlazePose output; `pre_processed_` has a zero-phase 5th-order Butterworth low-pass filter applied at 3 Hz

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

**Normalized vs. World coordinates**

BlazePose, via [MediaPipe's PoseLandmarker](https://developers.google.com/edge/mediapipe/solutions/vision/pose_landmarker/python), outputs two parallel sets of landmarks per frame, and this dataset keeps both as separate files:

- **Normalized** (`pose_landmarks`; `*_normalized.txt`) — `x`/`y` are scaled to `[0, 1]` by image width/height, i.e. image-space, not metric. `z` is depth relative to the hip midpoint, on roughly the same scale as `x`.
- **World** (`pose_world_landmarks`; `*_world.txt`) — `x`/`y`/`z` are real-world coordinates in **meters**, independent of image size or camera distance.

Both use the same hip-midpoint origin and 22-keypoint topology above; only the units/scale differ. See the MediaPipe PoseLandmarker link above for the full details on how each is computed.

### 3. Metadata (`data/metadata.txt`)
- Trial identifiers encoding activity, camera, subject, and task parameters
- Start/end frame indices for each trial (1-based)

---

## To Do

- [ ] Re-run pose estimation with the heavy BlazePose model for more accurate pose data
- [ ] Release the cross-camera pose synchronization code

---

## Disclaimer

Both the motion capture and pose data have gone through quality checks, but some incorrect values may still remain — please use the data with appropriate discretion. The authors will continue identifying and fixing such issues, and will keep this dataset updated accordingly.

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
