import TwitterHandler
from typing import Dict, List
import requests
import time
import shutil
import json
import random
import image_editor
from config import GOOGLE_API_KEY

CAMERA_POOL: List[str] = [
  'http://ns-webcams.its.sfu.ca/public/images/udn-current.jpg',
  'http://ns-webcams.its.sfu.ca/public/images/aqn-current.jpg',
  'http://ns-webcams.its.sfu.ca/public/images/aqsw-current.jpg',
  'http://ns-webcams.its.sfu.ca/public/images/gaglardi-current.jpg',
  'http://ns-webcams.its.sfu.ca/public/images/towern-current.jpg',
  'http://ns-webcams.its.sfu.ca/public/images/towers-current.jpg'
]
GOOGLE_API_ENDPOINT = f'https://vision.googleapis.com/v1/images:annotate?key={GOOGLE_API_KEY}'


def assemble_image_request(image_uri) -> dict:
  return {
    'requests': [{
      'image': {
        'source': {
          'imageUri': image_uri
        }
      },
      'features': [
        {
          'type': 'LABEL_DETECTION',
          'maxResults': 10
        }
      ]
    }]
  }


def clean_data(photo_annotation: list) -> List[Dict[str, float]]:
  score_list = [x['score'] for x in photo_annotation]
  max_score = max(score_list)
  min_score = min(score_list)
  distance = max_score - min_score
  selected_values = [{'label': x['description'], 'score': (x['score'] - min_score) / distance} for x in
                     photo_annotation]
  return selected_values


def image_annotation_text(image_uri: str):
  image_request_json = assemble_image_request(image_uri)
  response = requests.post(GOOGLE_API_ENDPOINT, json=image_request_json).content.decode('utf-8')
  return json.loads(response)['responses'][0]['labelAnnotations']


def save_a_photo_to_disk(image_uri: str, file_name: str):
  response = requests.get(image_uri, stream=True)
  with open(f'./photos/{file_name}.jpg', 'wb') as f:
    shutil.copyfileobj(response.raw, f)


def get_a_photo_from_camera() -> str:
  time_string = str(time.time()).split(".")[0]
  image_url = CAMERA_POOL[random.randrange(0, 6)]
  save_a_photo_to_disk(image_url, time_string)
  photo_annotation = image_annotation_text(image_url)
  cleaned_annotation = clean_data(photo_annotation)
  
  return f'./photos/{time_string}.jpg', cleaned_annotation


def get_weather_from_sensor() -> Dict[str, float]:
  rv = requests.get('https://backend.haoxp.xyz/weather?limit=1').content.decode()
  rv_json = json.loads(rv)['weather'][0]
  return {"humidity": rv_json['humidity'], "temperature": rv_json['temp']}


def edit_photo(filename: str, labels: List[Dict[str, object]], weather: Dict[str, float]):
  font_size = 24
  column_sep = font_size
  row_sep = font_size
  
  text_area_width = 2 * max([len(x['label']) for x in labels]) * font_size + 3 * column_sep
  row_num = (len(labels) + 1) // 2
  text_area_height = (row_num + 1) * row_sep + row_num * font_size
  
  # print(text_area_width, text_area_height)
  
  image_editor.add_rectangle_to_photo(filename, (-text_area_width, 0))
  image_editor.add_labels_to_photo(filename, labels, font_size, column_sep, row_sep)
  image_editor.add_weather_to_photo(filename, weather, (-text_area_width + column_sep, text_area_height))


def send_a_photo():
  filename, cleaned_annotation = get_a_photo_from_camera()
  temp_hum = get_weather_from_sensor()
  edit_photo(filename, cleaned_annotation, temp_hum)
  TwitterHandler.post_with_images(
    filename,
    f"Mountain real-time status - temperature: {temp_hum['temperature']}°C, humidity: { temp_hum['humidity']}%"
  )


if __name__ == '__main__':
  send_a_photo()
