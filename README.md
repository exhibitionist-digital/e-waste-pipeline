# 🚮 E-WASTE PIPELINE

![e-waste](./example.gif)

Scripts for using img2img/depth2image, tailored for transforming 3D renders with Stable Diffusion.

__Keep it simple__ - written in a way thats easy to modify and hack for your own
purposes.

<table>
    <tr>
        <td>✅</td>
        <td>Positive / negative prompts</td>
    </tr>
    <tr>
        <td>✅</td>
        <td>Compatible with SD 1.4/1.5/2.0/2.1</td>
    </tr>
    <tr>
        <td>✅</td>
        <td>Optimised for high(er) res </td>
    </tr>
    <tr>
        <td>✅</td>
        <td>img2img or depth2img</td>
    </tr>
    <tr>
        <td>❌</td>
        <td>No safety check</td>
    </tr>
    <tr>
        <td>❌</td>
        <td>No ui / cli only</td>
    </tr>
</table>

### How to use

- Clone repo, put source animation frames (png) in `./in`
- Rename `.env.example` to `.env` and add Hugging Face token
- Install reqs `pip install -r requirements.txt`
- Edit settings in `./waste.py`
- Run script with `python3 waste.py` and images will be output to `./out`

### Handy FFMPEG Scripts

Convert frames to video

```bash
ffmpeg -framerate 8 -pattern_type glob -i '*.png' -c:v libx264 -pix_fmt yuv420p out.mp4
```

Convert video to frames

```bash
ffmpeg -i input.mp4 -pix_fmt rgba output_%04d.png
```
