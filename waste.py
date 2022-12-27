import os
import glob
from dotenv import load_dotenv
from PIL import Image
import torch
from torch import autocast
from diffusers import StableDiffusionImg2ImgPipeline

# resolution settings
width = 1500
height = 1000

# edit settings here...
prompt = "beautiful horse"
# n_prompt = "trees"
guide = 15
steps = 48
seed = 12355
strength = 0.666

# get huggingface token
load_dotenv()
HUGGING_FACE = os.getenv("HUGGING_FACE")

# make output dir
try:
    os.mkdir("./out/")
except OSError as error:
    print("./out already exists")

# disable safety
def dummy(images, **kwargs):
    return images, False


# setup torch pipeline
device = "cuda"
torch.cuda.empty_cache()
img_pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "stabilityai/stable-diffusion-2", use_auth_token=HUGGING_FACE
)
img_pipe.safety_checker = dummy

# vram slicing on (good for HD)
img_pipe.to(device).enable_attention_slicing()


def infer(source_image):
    generator = torch.Generator("cpu").manual_seed(seed)
    images = img_pipe(
        prompt,
        image=source_image,
        strength=strength,
        guidance_scale=guide,
        num_inference_steps=steps,
    )
    return images[0][0]


for frame in sorted(glob.glob("./in/*.png")):
    new_path = frame.replace("./in/", "./out/")
    image = Image.open(frame).convert("RGB")
    image = image.resize((width, height), Image.Resampling.LANCZOS)
    image = infer(image)
    image.save(new_path)
