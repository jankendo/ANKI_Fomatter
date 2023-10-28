import os
import random
import shutil
import sqlite3
import zipfile
from pathlib import Path

import easygui
import langdetect

import json

APKG_EXTENSION = ".apkg"
JSON_EXTENSION = ".json"
OUTPUT_FOLDER = "./json"


def extract_fields(file_path, output_path, decknum):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall('output')

    db_path = 'output/collection.anki2'
    conn = sqlite3.connect(db_path)
    cursor = conn.execute('SELECT flds FROM notes')

    deck = {
        "id": str(decknum),
        "jpnName": "英検デッキ",
        "cards": []
    }

    cardnum = 0

    with open(output_path, 'w') as file:
        for row in cursor:
            data = row[0]
            if data:
                cardnum += 1
                fild = data.split("\x1f")
                jpn, eng = (fild[4], fild[5]) if detect_language(fild[4]) else (fild[5], fild[4])

                card = {
                    "id": str(cardnum),
                    "mp3Path": f"public/decks/deck1/audio/{cardnum}.mp3",
                    "genre": "none",
                    "word": fild[0],
                    "wordtrn": fild[1],
                    "sentence": eng,
                    "blank": convert_to_blank_sentence(eng),
                    "japanese": jpn,
                    "difficulty": random.randint(1, 1000),
                }
                deck['cards'].append(card)

        json.dump(deck, file, indent=4)

    conn.close()
    return output_path


def convert_to_blank_sentence(sentence):
    return "".join("_" if char.isalpha() else char for char in sentence)


def detect_language(text):
    return langdetect.detect(text) == 'ja'


def main():
    folder_path = easygui.diropenbox()

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    decknum = 0

    for entry in os.scandir(folder_path):
        if entry.name.endswith(APKG_EXTENSION):
            # outputフォルダが存在する場合はフォルダごと削除
            if os.path.exists('output'):
                shutil.rmtree('output')

            output_file = os.path.splitext(entry.name)[0] + JSON_EXTENSION
            output_path = Path(OUTPUT_FOLDER) / output_file

            # jsonファイルが存在する場合はスキップ
            extracted_path = extract_fields(entry.path, output_path, decknum)
            decknum += 1

            # jsonファイルを出力
            print(f"Converted {extracted_path}")

            shutil.rmtree('output')


if __name__ == "__main__":
    main()
