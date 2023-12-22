"""EAGLE.exeにpngファイルだけを飛ばします。引数はフォルダです。サブフォルダも取り込みますがネストにはなりません。
PNGは ADD_TAG_TO_EAGLE で指定された ": "付きの項目のみtag化します。これ以上あると多くなりすぎるのでModel,Sampler,Hires upscalerで十分です。
promptとNegativepromptその他の情報はメモに突っ込んでます。
"""

# directory_path=""
ADD_TAG_TO_EAGLE = "Model,Sampler,Hires upscaler"

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from PIL import Image
from scripts.eagleapi import api_util
from scripts.eagleapi import api_item
import sys

def parameters_text_from_png(input_image_path):
    img = Image.open(input_image_path)
    text_chunk = img.text.get("parameters", b"")
    return text_chunk

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
def _get_folderId(folder_name_or_id, allow_create_new_folder, server_url="http://localhost", port=41595):
    _ret = api_util.find_or_create_folder(folder_name_or_id, allow_create_new_folder, server_url, port)
    return _ret

def process_file(input_image_path, folderId):
    parameters_text = parameters_text_from_png(input_image_path)
    if parameters_text and parameters_text.strip():
        tags = []
        format_string(parameters_text, tags)
        item = api_item.EAGLE_ITEM_PATH(
            filefullpath=input_image_path,
            filename=os.path.splitext(os.path.basename(input_image_path))[0],
            annotation=parameters_text,
            tags=tags
        )
        ret = api_item.add_from_path(item=item, folderId=folderId)

def main(directory_path):
    png_files = [file for file in os.listdir(directory_path) if file.lower().endswith(".png")]
    total_files = len(png_files)

    with ThreadPoolExecutor() as executor:
        futures = []
        for root, dirs, files in os.walk(directory_path):
            folname = os.path.basename(root)
            folderId = _get_folderId(folname, True)

            for file in tqdm(files, desc=f"Processing {root}", unit="file", position=0):
                if file.lower().endswith(".png"):
                    input_image_path = os.path.join(root, file)
                    futures.append(executor.submit(process_file, input_image_path, folderId))

        # ファイルごとの処理が終わるまで待機
        for future in as_completed(futures):
            future.result()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python your_script.py <directory_path>")
        sys.exit(1)
        
    print(sys.argv)
    for folder_path in sys.argv[1:]:
            main(folder_path)