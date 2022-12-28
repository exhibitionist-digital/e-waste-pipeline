import os
import glob
from PIL import Image
import torch
from torch import autocast
from diffusers import StableDiffusionImg2ImgPipeline

# resolution settings
width = 1500
height = 1000

# edit settings here...
prompt = "beautiful horse"
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


def load_learned_embed_in_clip(
    learned_embeds_path, text_encoder, tokenizer, token=None
):
    loaded_learned_embeds = torch.load(learned_embeds_path, map_location="cpu")

    # separate token and the embeds
    trained_token = list(loaded_learned_embeds.keys())[0]
    embeds = loaded_learned_embeds[trained_token]

    # cast to dtype of text_encoder
    dtype = text_encoder.get_input_embeddings().weight.dtype

    # add the token in tokenizer
    token = token if token is not None else trained_token
    num_added_tokens = tokenizer.add_tokens(token)
    i = 1
    while num_added_tokens == 0:
        print(f"The tokenizer already contains the token {token}.")
        token = f"{token[:-1]}-{i}>"
        print(f"Attempting to add the token {token}.")
        num_added_tokens = tokenizer.add_tokens(token)
        i += 1

    # resize the token embeddings
    text_encoder.resize_token_embeddings(len(tokenizer))

    # get the id for the token and assign the embeds
    token_id = tokenizer.convert_tokens_to_ids(token)
    text_encoder.get_input_embeddings().weight.data[token_id] = embeds
    print("Added token: ", token)
    return token


for embedding in sorted(
    glob.glob("./embeddings/*.pt") + glob.glob("./embeddings/*.bin")
):
    name = embedding.split("/")
    name = name[len(name) - 1].split(".")[0]
    load_learned_embed_in_clip(
        embedding, img_pipe.text_encoder, img_pipe.tokenizer, name
    )


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


for frame in sorted(glob.glob("./in/*.png")):
    new_path = frame.replace("./in/", "./out/")
    image = Image.open(frame).convert("RGB")
    image = image.resize((width, height), Image.Resampling.LANCZOS)
    image = infer(image)
    image.save(new_path)
