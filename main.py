from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image, ImageDraw, ImageFont
import uuid, os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

def generate_reply(prompt: str) -> str:
    return f"مرحباً، كتبت: {prompt}"

def generate_image(prompt: str) -> str:
    img = Image.new('RGB', (600, 300), (240, 240, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    draw.text((20, 140), prompt, fill=(0,0,0), font=font)
    os.makedirs('static', exist_ok=True)
    filepath = f"static/{uuid.uuid4().hex}.png"
    img.save(filepath)
    return filepath

@app.post("/chat")
async def chat(req: PromptRequest):
    reply = generate_reply(req.prompt)
    img_path = generate_image(req.prompt)
    return {"reply": reply, "image_url": img_path}
