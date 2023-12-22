from googletrans import Translator

def translate_text(text, dest_language='ja'):
    translator = Translator()
    translation = translator.translate(text, dest=dest_language)
    return translation.text

# 翻訳したいテキスト
original_text = "Hello, how are you?"

# 翻訳
translated_text = translate_text(original_text)

# 結果の表示
print(f"Original Text: {original_text}")
print(f"Translated Text: {translated_text}")