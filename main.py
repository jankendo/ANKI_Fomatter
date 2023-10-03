import os
import csv
import tkinter.filedialog as filedialog
import zipfile
import sqlite3
import shutil


def extract_fields(file_path, output_path):
    # Zipファイルを解凍する
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall('output')

    db_path = 'output/collection.anki2'

    # データベースに接続し、notesテーブルからflds列を取得する
    conn = sqlite3.connect(db_path)
    cursor = conn.execute('SELECT flds FROM notes')

    # 出力ファイルを作成し、データをCSV形式で書き込む
    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        for row in cursor:
            data = row[0]
            if data:
                fields = data.split("\x1f")
                writer.writerow(fields)

    # データベースの接続を閉じる
    conn.close()
    return output_path


def main():
    # フォルダの選択ダイアログを表示する
    root = filedialog.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory()

    output_folder = "./csv"
    os.makedirs(output_folder, exist_ok=True)

    for file_path in os.listdir(folder_path):
        if file_path.endswith(".apkg"):
            # 初期化処理
            if os.path.exists('output'):
                shutil.rmtree('output')

            output_file = os.path.splitext(file_path)[0] + ".csv"
            output_path = os.path.join(output_folder, output_file)

            # 抽出・変換を実行する
            extracted_path = extract_fields(os.path.join(folder_path, file_path), output_path)

            # 処理完了メッセージを表示する
            print(f"抽出・変換完了: {extracted_path}")

            # 使用した一時フォルダを削除する
            shutil.rmtree('output')


if __name__ == "__main__":
    main()
