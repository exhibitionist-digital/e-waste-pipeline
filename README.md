# 🚮 E-WASTE PIPELINE

![e-waste](./example.gif)

Scripts for using img2img/depth2image, tailored for transforming 3D renders with
Stable Diffusion.

**Keep it simple** - written in a way thats easy to modify and hack for your own
purposes.

<table>
    <tr>
        <td>✅</td>
        <td>Positive / negative prompts</td>
    </tr>
    <tr>
        <td>✅</td>
        <td>Embeddings</td>
    </tr>
    <tr>
        <td>✅</td>
        <td>Dynamic prompt generator</td>
    </tr>
    <tr>
        <td>✅</td>
        <td>Compatible with SD 1.4/1.5/2.0/2.1</td>
    </tr>
    <tr>
        <td>✅</td>
        <td>Generate sequences of images</td>
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
        <td>No ui / code only</td>
    </tr>
</table>

### How to use

- Clone repo, put source animation frames (png) in `./in`
- Install reqs `pip install -r requirements.txt`
- Edit settings in `./waste.py`
- Run script with `python3 waste.py` and images will be output to `./out`

### Embeddings

Add `.pt` or `.bin` files into `./embeddings`, they will be added to the
pipeline on startup.

The `token` for each embedding will be printed to the console. It falls back to
filename if there is no token found in the embedding.

### Dynamic prompt generator

Use `prompt_gen` -- a simple, but powerful, function that allows you to pass in
lists of words/prompts and cycle through them at varying speeds and indices.

```python
bugType = ["shiny", "squashed", "giant", "monster", "cute"]
location = ["in the sky", "floating on water", "crawling on flesh"]

f"{prompt_gen(bugType, 6, 3)} bug {prompt_gen(location, 15, 3)}"
# shiny bug in the sky
f"{prompt_gen(bugType, 6, 22)} bug {prompt_gen(location, 15, 22)}"
# monster bug floating on water
f"{prompt_gen(bugType, 6, 41)} bug {prompt_gen(location, 15, 41)}"
# squashed bug crawling on flesh
```

...and so on -- you can also use these for strength/guide/seed/steps values if
you are silly.

```python
strengths = [0.8, 0.7, 0.6, 0.5]
steps = [40, 45, 50, 12]

strength = prompt_gen(strengths, 6, 41)
steps = prompt_gen(steps, 6, 41)
```

### Handy FFMPEG scripts

Convert frames to video

```bash
ffmpeg -framerate 8 -pattern_type glob -i '*.png' -c:v libx264 -pix_fmt yuv420p out.mp4
```

Convert video to frames

```bash
ffmpeg -i input.mp4 -pix_fmt rgba output_%04d.png
```
