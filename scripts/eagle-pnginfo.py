
# フォルダのパス
directory_path = r"O:\AI\sd.webui\webui\outputs\txt2img-images"
# directory_path = r"O:\202310"
# additional_tags_to_eagle="Steps,Sampler,CFG scale,Seed,Face restoration,Size,Model hash,Model,Hypernet,Hypernet strength,Variation seed,Variation seed strength,Seed resize from,Denoising strength,Conditional mask weight,Eta,Clip skip,ENSD"

ADD_TAG_TO_EAGLE="Model,Sampler,Hires upscaler"

import os
import sys
import gradio as gr
import zlib
from modules import  script_callbacks, shared
from scripts.eagleapi import api_application
from scripts.eagleapi import api_item
from scripts.eagleapi import api_util
from scripts.parser import Parser
from scripts.tag_generator import TagGenerator

from tqdm import tqdm  # tqdmライブラリを利用
from PIL import Image, PngImagePlugin

from typing import List


# png 内のデータを取得する
def parameters_text_from_png(input_image_path):
    # 画像を読み込む
    img = Image.open(input_image_path)

    # tEXtチャンクからテキストを抽出
    text_chunk = img.text.get("parameters", b"")
    # extracted_text = text_chunk.decode('utf-8')
    extracted_text = text_chunk

    return extracted_text
 
def main():    
    png_files = [file for file in os.listdir(directory_path) if file.lower().endswith(".png")]
    total_files = len(png_files)
    for root, dirs, files in os.walk(directory_path):
        folname = os.path.basename(root)
        # イーグルからフォルダIDを取得
        def _get_folderId(folder_name_or_id, allow_create_new_folder, server_url="http://localhost", port=41595):
            _ret = api_util.find_or_create_folder(folder_name_or_id, allow_create_new_folder, server_url, port)
            return _ret
        folderId = _get_folderId(folname, True)
        item=[]
        
        for file in tqdm(files, desc=f"Processing {root}", unit="file", position=0):
            if not file.lower().endswith(".png"):
                continue

            
            input_image_path = os.path.join(root, file)
            parameters_text=''
            tags = []
            # PNGのテキスト読み込み
            parameters_text = parameters_text_from_png(input_image_path)
            if parameters_text!=None  and parameters_text!="":
                format_string(parameters_text,tags)
            
            # ローカルを保存
            item.append(api_item.EAGLE_ITEM_PATH(
                filefullpath=input_image_path,
                filename=os.path.splitext(os.path.basename(input_image_path))[0],
                annotation=parameters_text,
                tags=tags
            ))
        
        else:
            # ディレクトリ単位で処理
            for r in item:
                ret = api_item.add_from_path(item=r,folderId=folderId)
            

def format_string(parameters_text,tags):
    
    # tag配列を射影します
    var1 = parameters_text.replace('\n', ',').split(',')
    var1 = [param.strip() for param in var1]
    var1 = [param for param in var1 if param != ""]
    var2 = [var.strip() + ": " for var in ADD_TAG_TO_EAGLE.split(',')]
    # 7. var1の中身を検索して、var2[n]+": "であるならば、その要素をVar3にセットします,順序も維持します
    var3 = [param for var in var2 for param in var1 if param.startswith(var)]
    # 元のtagsの中身を変更
    tags.clear()
    tags.extend(var3)
    # # その他の文字列を見つけやすいようにキャリッジリターンを入れます
    # parameters_text = parameters_text.replace('\nSteps: ', '\n\n\nSteps: ')
    # parameters_text = parameters_text.replace('\nNegative prompt: ', '\n\n\nNegative prompt: ')
    
main()
