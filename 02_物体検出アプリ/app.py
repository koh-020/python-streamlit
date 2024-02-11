from io import StringIO
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image, ImageDraw, ImageFont
import sys
import time
import json
import streamlit as st






filepath = "sample01.jpg"
# JSONからキーとエンドポイントを取得
with open('secret.json') as f:
    secret = json.load(f)
KEY = secret['KEY']
ENDPOINT = secret['ENDPOINT']

# API情報を設定
computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(KEY))

# タグ情報取得
def get_tags(filepath):
    # Open local image file
    file_image = open(filepath, "rb")
    # Call API local image
    tags_result = computervision_client.tag_image_in_stream(file_image)

    # Print results with confidence score
    print("Tags in the local image: ")
    if (len(tags_result.tags) == 0):
        print("No tags detected.")
    else:
        tags = tags_result.tags
        tags_name = []
        for tag in tags:
            tags_name.append(tag.name)
            
            # print("'{}' with confidence {:.2f}%".format(tag.name, tag.confidence * 100))
    return tags_name


# 物体検出
def detect_objects(filepath):
    local_image_objects = open(filepath, "rb")
    # Call API with local image
    detect_objects_results_local = computervision_client.detect_objects_in_stream(local_image_objects)
    objects = detect_objects_results_local.objects

    return objects

# 検出物描画
def draw_object(object, draw):
    # 検出物の枠を表示
    rect = object.rectangle
    left = rect.x
    top = rect.y
    right = left + rect.w
    bottom = top + rect.h
    object_coordinates = ((left, top), (right, bottom))
    draw.rectangle(object_coordinates, outline='green', width=5)
    # 検出物の名前を表示
    font = ImageFont.truetype(font="./Poppins-Regular.ttf", size=50)
    caption = object.object_property
    text_left, text_top, text_right, text_bottom = draw.textbbox((left, top), caption, font=font)
    # text_right = left + text_w
    # text_bottom = top + text_h
    text_mergin = 5
    textarea_mergin = text_mergin * 2
    text_coordinates = ((left, top), (text_right + textarea_mergin, text_bottom + textarea_mergin))
    draw.rectangle(text_coordinates, fill='green')
    draw.text((left + text_mergin, top + text_mergin), caption, fill="white", font=font)




# streamlitでページ作成
st.title("物体検出")

# ファイルアップロード
upload_file = st.file_uploader("Chose a file",type=['jpg', 'png'])
if upload_file is not None:
    image = Image.open(upload_file)
    
    # メソッドを使うためのパスの設定
    img_path = f'img/{upload_file.name}'
    # パスに画像を保存
    image.save(img_path)

    # 描画
    draw = ImageDraw.Draw(image)
    # 物体検出
    objects = detect_objects(img_path)
    for object in objects:
        # 検出物を表示
        draw_object(object, draw)
        


    # 画像を表示
    st.image(image)


    # 認識されたタグ情報を表示
    st.markdown("**認識されたタグ**")

    img_tags = get_tags(img_path)
    tags_name = ", ".join(img_tags)
    st.markdown(f'>{tags_name}')