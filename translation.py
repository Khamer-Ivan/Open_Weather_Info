from googletrans import Translator


def translator(text, lang_1, lang_2):
    try:
        translator = Translator()
        translation = translator.translate(text=text, src=lang_1, dest=lang_2)
        return translation.text
    except Exception as error:
        return error
