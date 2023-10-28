import csv
import os
import random
import re
from pathlib import Path

import easygui
import langdetect

import json

JSON_EXTENSION = ".json"
OUTPUT_FOLDER = "./json"


def extract_fields(output_path, decknum):
    deck = {
        "id": str(decknum),
        "jpnName": "TSLデッキ",
        "cards": []
    }

    cardnum = 0
    uq = 0

    tslwords = append_word()
    tslsentens = append_sentence()

    with open(output_path, 'w') as file:
        for word in tslwords:
            Check, index = word_in_2d_array(word, tslsentens)
            if Check:
                sentence = tslsentens[index][6]
                wordtrn = tslsentens[index][4]
                jpn = tslsentens[index][7]
            else:
                uq += 1
                sentence = "None"
                wordtrn = "None"
                jpn = "None"

            cardnum += 1

            card = {
                "id": str(cardnum),
                "mp3Path": f"Voices/deck1/voice/{cardnum}.mp3",
                "genre": "none",
                "word": word,
                "wordtrn": wordtrn,
                "sentence": sentence,
                "blank": convert_to_blank_sentence(sentence),
                "japanese": jpn,
                "difficulty": random.randint(1, 1000),
            }
            deck['cards'].append(card)

        json.dump(deck, file, indent=4)
    print(f"Unique: {uq}")
    return output_path


def word_in_2d_array(word, array_2d):
    for index, row in enumerate(array_2d):
        if row[3] == word:
            return True, index
    return False, -1


def append_word():
    # ファイル名を指定
    file_name = "TSL_1.2_alphabetized_description.txt"

    # 条件に合致する行だけを格納するリストを作成
    selected_lines = []

    # ファイルを開いて条件に合致する行を抽出
    with open(file_name, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()  # 行末の改行文字を削除
            if re.match(r'^\d+\.\s+[a-zA-Z]+', line):  # 条件に合致する行を正規表現でチェック
                selected_lines.append(line.split(" ")[2])
    return selected_lines


def append_sentence():
    file_path = "TOEICTSLver2.csv"
    data_array = []

    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            csv_reader = csv.reader(file)

            # 2行目から読み取りを開始
            next(csv_reader)  # 1行目をスキップ

            # ファイルの残りの行を読み取り、データをリストに追加
            for row in csv_reader:
                data_array.append(row)
    except FileNotFoundError:
        print(f"ファイル '{file_path}' が見つかりません。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

    return data_array


def convert_to_blank_sentence(sentence):
    return "".join("_" if char.isalpha() else char for char in sentence)


def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    output_path = OUTPUT_FOLDER + "/TSL.json"
    decknum = 1

    # jsonファイルが存在する場合はスキップ
    extracted_path = extract_fields(output_path, decknum)

    # jsonファイルを出力
    print(f"Converted {extracted_path}")


if __name__ == "__main__":
    main()
