from PIL import Image, ImageFont, ImageDraw
from typing import Tuple, Dict, List

def color_interpolation(score: float, color_endpoints=((255, 127, 127), (127, 255, 127))):
  color_group_by_channel = [ [] for i in range(0, 3)]
  for i in range(0, 3):
    color_group_by_channel[i].append(color_endpoints[0][i])
  for i in range(0, 3):
    color_group_by_channel[i].append(color_endpoints[1][i])
  return tuple(map(lambda x: int((x[0]-x[1])*score + x[1]), color_group_by_channel))

def raw_location_to_absolute(location: Tuple[int, int], width: int, height: int):
  tmp = []
  if location[0] < 0:
    tmp.append(location[0] + width)
  else:
    tmp.append(location[0])
  if location[1] < 0:
    tmp.append(location[1] + height)
  else:
    tmp.append(location[1])

  return tuple(tmp)

def add_rectangle_to_photo(filename: str, raw_left_top: Tuple[int, int], 
                           raw_right_bottom=None, color=(255, 255, 255, 100)):
  with Image.open(filename) as img:
    width, height = img.size

    left_top = raw_location_to_absolute(raw_left_top, width, height)
    if raw_right_bottom == None:
      right_bottom = (width, height)
    else:
      right_bottom = raw_location_to_absolute(raw_right_bottom, width, height)

    add_rectangle_to_img(img, left_top, right_bottom, color)
    img.save(filename)

def add_weather_to_photo(filename: str, weather_info: Dict[str, float], raw_location: Tuple[int, int], 
                        font_size=32, color=(232, 65, 24)):
  with Image.open(filename) as img:
    width, height = img.size
    location_x, location_y = raw_location_to_absolute(raw_location, width, height)

    for k, v in weather_info.items():
      str_to_write = k + ' ' + str(v)
      if k == 'humidity':
        str_to_write += '%'
      elif k == 'temperature':
        str_to_write += '°'
      add_text_to_img(img, str_to_write , location=(location_x, location_y), color=color, font_size=font_size)
      location_y += font_size

    img.save(filename)

def add_labels_to_photo(filename: str, labels: List[Dict[str, object]], 
                        font_size:int, column_sep: int, row_sep: int):
  row_num = (len(labels) + 1) // 2
  max_word_width = max([len(x['label']) for x in labels]) * font_size * 0.8

  with Image.open(filename) as img:
    location_y = 0
    location_x = img.size[0] * 0.1

    i = 0
    content_left = location_x + column_sep
    location_x += column_sep
    location_y += row_sep 
    while i < len(labels):
      add_text_to_img(img, labels[i]['label'], 
                    location=(location_x, location_y), 
                    color=color_interpolation(labels[i]['score']), 
                    font_size=font_size)
      i += 1
      location_x += max_word_width
      location_x += column_sep
      if not i < len(labels):
        break
      add_text_to_img(img, labels[i]['label'], 
                    location=(location_x, location_y), 
                    color=color_interpolation(labels[i]['score']), 
                    font_size=font_size)
      i += 1
      location_x = content_left
      location_y += font_size
      location_y += row_sep
    img.save(filename)


def add_text_to_img(image: object, text: str,
                    location=(0, 0), color=(0, 0, 0), font_size=16):
  draw = ImageDraw.Draw(image)
  font = ImageFont.truetype("./fonts/Verdana.ttf", font_size)
  draw.text(location, text, color, font=font)
  del draw

def add_rectangle_to_img(image: object, left_top: Tuple[int, int], 
                         right_bottom: Tuple[int, int], color: Tuple[int, int, int, int]):
  draw = ImageDraw.Draw(image, 'RGBA')
  draw.rectangle((left_top, right_bottom), color)
  del draw

if __name__ =='__main__':
  
  add_labels_to_photo(filename, labels)
