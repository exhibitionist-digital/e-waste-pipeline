# 🚮 E-WASTE PIPELINE

<video src="https://cloudflare-ipfs.com/ipfs/QmenkhEUHDm1q9pZrSUY4aXgXSHg726hKT3jfJ3HGxQMWh"></video>

Modified img2img, tailored for transforming 3D renders with Stable Diffusion.

Keep it simple - written in a way thats easy to modify and hack for your own
purposes.

### How to use

- Clone repo, put source animation frames (png) in `./in`
- Rename `.env.example` to `.env` and add Hugging Face token
- Install reqs `pip install -r requirements.txt`
- Edit settings in `./waste.py`
- Run script with `python3 waste.py` and images will be output to `./out`

### Handy FFMPEG Scripts

Convert frames to video

```bash
ffmpeg -framerate 24 -pattern_type glob -i '*.png' -c:v libx264 -pix_fmt yuv420p out.mp4
```

Convert video to frames

```bash
ffmpeg -i input.mp4 -pix_fmt rgba output_%04d.png
```
