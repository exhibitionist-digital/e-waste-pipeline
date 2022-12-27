# 🚮 E-WASTE PIPELINE

Modified img2img, tailored for transforming 3D renders with Stable Diffusion.

### How to use

- Clone repo, put source animation frames (png) in `./in`
- Rename `.env.example` to `.env` and add Hugging Face token
- Install reqs `pip install -r requirements.txt`
- Edit settings in `./waste.py`
- Run script with `python3 waste.py` and images will be output to `./out`

### Handy FFMPEG Scripts

Convert frames to video

```bash
ffmpeg -framerate 24 -pattern_type glob -i '*.png' c:v libx264 -pix_fmt yuv420p out.mp4
```

Convert video to frames

```bash
ffmpeg -i input.mp4 -pix_fmt rgba output_%04d.png
```