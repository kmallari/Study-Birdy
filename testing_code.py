import os
import json
from read_text import ocr_space_url

json_data = json.loads(ocr_space_url('https://i.imgur.com/RPRkYjk.png'))
text_from_img = json_data['ParsedResults'][0]['ParsedText']

lines = text_from_img.split('\r')
official_line = []

for line in lines:
    details = []
    word = ''
    line = line.split('\t')
    for detail in line:
        if detail.startswith('\n'):
            detail = detail.replace('\n', '')
        if detail == '':
            continue
        details.append(detail)
    if details == []:
        continue
    official_line.append(details)

print(official_line)