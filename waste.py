import os
import glob
from PIL import Image
import torch
from torch import autocast
from diffusers import StableDiffusionImg2ImgPipeline

# resolution settings
width = 1472
height = 960

# edit settings here...
prompt = "beautiful horse, Kipaki-100"
negative_prompt = "trees"
guide = 15
steps = 48
seed = 12355
strength = 0.666

# make output dir
try:
    os.mkdir("./out/")
except:
    pass

# disable safety
def dummy(images, **kwargs):
    return images, False


# setup torch pipeline
torch.cuda.empty_cache()
img_pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "stabilityai/stable-diffusion-2-1"
)
img_pipe.safety_checker = dummy

# vram slicing on (good for HD)
img_pipe.to("cuda").enable_attention_slicing()


def infer(source_image):
    generator = torch.Generator("cpu").manual_seed(seed)
    images = img_pipe(
        prompt,
        image=source_image,
        strength=strength,
        guidance_scale=guide,
        num_inference_steps=steps,
        negative_prompt=negative_prompt,
    )
    return images[0][0]


# dynamic prompt generator
# cycle through word/prompt arrays at varying speed and indices
def prompt_gen(array, speed, index):
    built = []
    for prompt in array:
        built += [prompt] * speed
    return built[index % len(built)]


for frame in sorted(glob.glob("./in/*.png")):
    new_path = frame.replace("./in/", "./out/")
    image = Image.open(frame).convert("RGB")
    image = image.resize((width, height), Image.Resampling.LANCZOS)
    image = infer(image)
    image.save(new_path)
