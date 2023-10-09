import os
import re
import shutil
import sqlite3
import tkinter.filedialog as filedialog
import zipfile
import json


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
                    "wordtrn":fild[1],
                    "sentence": eng,
                    "blank": convert_to_blank_sentence(eng),
                    "japanese": jpn,
                    "difficulty": "980"
                }
                deck['cards'].append(card)

        json.dump(deck, file, indent=4)

    conn.close()
    return output_path


def convert_to_blank_sentence(sentence):
    return "".join("_" if char.isalpha() else char for char in sentence)


def detect_language(text):
    japanese_range = (ord(u"ぁ"), ord(u"ゟ"))
    return any(japanese_range[0] <= ord(char) <= japanese_range[1] for char in text)


def main():
    root = filedialog.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory()

    output_folder = "./json"
    os.makedirs(output_folder, exist_ok=True)

    decknum = 0

    for file_path in os.listdir(folder_path):
        if file_path.endswith(".apkg"):
            if os.path.exists('output'):
                shutil.rmtree('output')

            output_file = os.path.splitext(file_path)[0] + ".json"
            output_path = os.path.join(output_folder, output_file)

            extracted_path = extract_fields(os.path.join(folder_path, file_path), output_path, decknum)
            decknum += 1

            print(f"抽出・変換完了: {extracted_path}")

            shutil.rmtree('output')


if __name__ == "__main__":
    main()
