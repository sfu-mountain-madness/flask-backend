import TwitterHandler
from typing import Dict, List
import requests
import time
import shutil
import json
import random
from PIL import Image, ImageFont, ImageDraw

CAMERA_POOL: List[str] = [
  'http://ns-webcams.its.sfu.ca/public/images/udn-current.jpg',
  'http://ns-webcams.its.sfu.ca/public/images/aqn-current.jpg',
  'http://ns-webcams.its.sfu.ca/public/images/aqsw-current.jpg',
  'http://ns-webcams.its.sfu.ca/public/images/gaglardi-current.jpg',
  'http://ns-webcams.its.sfu.ca/public/images/towern-current.jpg',
  'http://ns-webcams.its.sfu.ca/public/images/towers-current.jpg'
]


def get_a_photo_from_camera() -> str:
  time_string = str(time.time()).split(".")[0]
  url = CAMERA_POOL[random.randrange(0, 6)]
  response = requests.get(url, stream=True)
  with open(f'./photos/{time_string}.jpg', 'wb') as f:
    shutil.copyfileobj(response.raw, f)
  return f'./photos/{time_string}.jpg'


def get_weather_from_sensor() -> Dict[str, float]:
  rv = requests.get('https://backend.haoxp.xyz/weather?limit=1').content.decode()
  rv_json = json.loads(rv)['weather'][0]
  return {"humidity": rv_json['humidity'], "temperature": rv_json['temp']}


def send_a_photo():
  filename = get_a_photo_from_camera()
  temp_hum = get_weather_from_sensor()
  TwitterHandler.post_with_images(
    filename,
    f"Mountain real-time status - temperature: {temp_hum['temperature']}°C, humidity: { temp_hum['humidity']}%"
  )

def add_text_to_photo(filename: str, text: str, 
                      location=(0, 0): Tuple[int, int], 
                      color=(0, 0, 0): Tuple[int, int, int],
                      fontSize=16: int):
  with Image.open("sample_in.jpg") as img:
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("./fonts/Verdana.ttf", fontSize)
    draw.text(location, text, color, font=font)
    img.save(filename)


if __name__ == '__main__':
  send_a_photo()
