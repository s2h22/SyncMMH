"""
Converts each *_multiview.mp4 in visualization/ to a *_multiview.gif alongside
it, so the clips play inline in README.md (GitHub's markdown renderer
autoplays GIFs via plain ![]() syntax but does not render <video> tags or
autoplay linked mp4s in a committed README).

Downscales width and drops frames to keep file size reasonable for a README.

Usage:
  python mp4_to_gif.py
"""

import glob
import os

import cv2
from PIL import Image

GIF_WIDTH = 900
GIF_FPS = 24  # higher than before (was 12) so motion doesn't look choppy

for mp4_path in sorted(glob.glob("../visualization/*_multiview.mp4")):
    gif_path = mp4_path[:-4] + ".gif"
    print(mp4_path, "->", gif_path)

    cap = cv2.VideoCapture(mp4_path)
    src_fps = cap.get(cv2.CAP_PROP_FPS)
    step = max(1, round(src_fps / GIF_FPS))

    raw_frames = []
    i = 0
    while True:
        res, frame = cap.read()
        if not res:
            break
        if i % step == 0:
            h, w = frame.shape[:2]
            scale = GIF_WIDTH / w
            frame = cv2.resize(frame, (GIF_WIDTH, round(h * scale)), interpolation=cv2.INTER_AREA)
            raw_frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        i += 1
    cap.release()

    # Quantize every frame against ONE shared palette (built from the middle
    # frame) instead of each frame picking its own -- otherwise the palette
    # shifts slightly frame to frame and reads as flicker. Dithering is off:
    # this content is flat black background + solid-colored lines/circles,
    # not photographic gradients, so dithering just adds per-frame noise
    # that shimmers between frames instead of hiding banding.
    palette_img = Image.fromarray(raw_frames[len(raw_frames) // 2]).quantize(colors=255, method=Image.MEDIANCUT)
    frames = [Image.fromarray(f).quantize(palette=palette_img, dither=Image.NONE) for f in raw_frames]

    duration_ms = round(1000 / (src_fps / step))
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=duration_ms, loop=0, optimize=True)
    print("  %d frames, %.1f MB" % (len(frames), os.path.getsize(gif_path) / 1e6))
