from PIL import Image
from pathlib import Path

FIG = Path("results/figures")
names = ["calibration_sessions.png", "calibration_energy.png", "calibration_duration.png"]
imgs = [Image.open(FIG / n) for n in names]

# scale all to the same height
h = min(im.height for im in imgs)
imgs = [im.resize((int(im.width * h / im.height), h), Image.LANCZOS) for im in imgs]

gap = 20
W = sum(im.width for im in imgs) + gap * (len(imgs) - 1)
canvas = Image.new("RGB", (W, h), "white")

x = 0
for im in imgs:
    canvas.paste(im, (x, 0))
    x += im.width + gap

out = FIG / "calibration_3panel.png"
canvas.save(out, dpi=(220, 220))
print(f"saved {out}  ({canvas.width}x{canvas.height})")