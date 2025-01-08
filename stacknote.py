import os
import json
import sqlite3
import re
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, filedialog, messagebox  # ttk,filedialog,messageboxをインポート
from datetime import date
from message_box import CustomMessageBox    # 作成したクラス
from message_box import CustomYesNoBox    # 作成したクラス
from message_box import CustomComboBox    # 作成したクラス
from message_box import CustomSearch    # 作成したクラス
from db_operation import DatabaseManager    # 作成したクラス

import sys
print(sys.executable)

######################################
## グローバル変数
######################################
# グローバル変数でDatabaseManagerインスタンスを管理
db_manager = DatabaseManager("stacknote.db")  # デフォルトのデータベース
# 設定ファイルのパス
SETTINGS_FILE = "settings.json"
# ソート順を管理
sort_reverse = False

######################################
## データベースの設定
######################################
# データベースを参照または生成
conn = sqlite3.connect('stacknote.db')
cur = conn.cursor()

# テーブルが存在するか確認
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='notes';")
if not cur.fetchone():
    # テーブルが存在しない場合のみ作成
    sql = """CREATE TABLE notes (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             stack TEXT NOT NULL,
             notebook TEXT NOT NULL,
             note TEXT NOT NULL,
             day TEXT NOT NULL,
             contents TEXT NOT NULL)"""
    cur.execute(sql)

# コミットして閉じる
conn.commit()
conn.close()


######################################
## CstomTkinterの設定
######################################
# デザイン設定
ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# トップレベルウインドウの生成
"""
csstomtkinterの場合、root = ctk.CTk()になる。
"""
root = ctk.CTk()
# トップレベルウインドウの設定
root.title('StackNote')
root.geometry('800x500')


######################################
## CstomTkinter/ttkウィジェットの設定
## ※Buttonウィジェットは引数で機能の関数を呼び出す為後半
######################################
textbox = ctk.CTkTextbox(
    root,
    width = 100,
    height = 100,
    border_width=3,
    border_color=('#505050'),  # ライトモードとダークモードで異なる色
    font=('meiryo', 14)
)

textbox.place(
    relx = 0.24,
    rely = 0.16,
    relwidth = 0.72,
    relheight = 0.81
)

# textboxに記入したテキストをstacknote.dbのnotesテーブルのcontentに保存
def get_note():
    conn = sqlite3.connect(db_manager.get_current_database())  # 切り替えたデータベースを参照
    cur = conn.cursor()

"""
ノートタイトル用のエントリー
"""
# ノートタイトル用のエントリーを作成
title_entry = ctk.CTkEntry(
    root,
    placeholder_text="ノートタイトルを入力",
    font=("Arial", 16))
title_entry.place(
    relx=0.24,
    rely=0.1,
    relwidth=0.72,
    relheight=0.05
)

# 初期値を設定
title_entry.insert(0, "")


# ハンドラ関数(各動作)
"""
CstomTkinter用にメッセージボックスを作成
Toplevelwindowクラスを呼び出し
"""
# 各種メッセージ用サイズでの呼び出し(サイズ省略で300x150になる)
if __name__ == "__main__":

    # ボタンを押すとメッセージボックスを表示
    def show_message(title, message):
        CustomMessageBox(root,
                         title,
                         message
                         # width="300",    # 省略するとデフォ値：300
                         # height="150"    # 省略するとデフォ値：150
                         )

# yes/no用
if __name__ == "__main__":

    # ボタンを押すとメッセージボックスを表示
    def ask_yes_no(title, message):
        return CustomYesNoBox.show(root,    # resultを返す
                       title,
                       message
                       # width="300",    # 省略するとデフォ値：320
                       # height="150"    # 省略するとデフォ値：150
                       )

# コンボボックス用
if __name__ == "__main__":

    # ボタンを押すとコンボボックスを表示
    def show_combo_box():
        """コンボボックスを表示して選択を取得"""
        # データベースからスタック名とノートブック名を取得
        # 「ノートの移動」用の関数使用
        stack_options = get_stacks()
        notebook_options = get_notebooks()

        # 2つのコンボボックスを表示して選択結果を取得
        result1, result2 = CustomComboBox.show(
            root,
            title="選択ダイアログ",
            message="以下の2つのオプションから選択してください:\n※内容に更新がある場合、上書き保存が必要です。",
            options1=stack_options,
            options2=notebook_options,
            width="330",    # デフォ値："310"
            height="210"   # デフォ値："210"
        )

        # 結果を表示（デバッグ用）
        print(f"選択したスタック: {result1}")
        print(f"選択したノートブック: {result2}")

        # 選択結果を返す
        return result1, result2


"""
treeview設定各種
"""
# treeviewのスクロールバーと階層列の設定
# Treeview用のスタイルを設定
style = ttk.Style()
style.configure("Custom.Treeview", font=("meiryo", 10))  # フォントとサイズを設定

# TreeviewのCustomTkinter用の親ウィジェットを追加
# CTkScrollableFrameを作成
treeview_frame = ctk.CTkFrame(root)
treeview_frame.place(
    relx=0.01,
    rely=0.17,
    relwidth=0.21,
    relheight=0.80
)

# Treeviewを作成
tree = ttk.Treeview(
    treeview_frame,
    show="tree headings",
    selectmode='extended',
    style="Custom.Treeview",
    height=10
)

# 階層列の設定
tree.column('#0', anchor='w', width=80)  # 階層列
# Treeviewの列設定
tree.column('#0', width=160, minwidth=160, stretch=True)  # 階層列
# 階層列の設定
tree.heading('#0', text='スタック / ノートブック / ノート',
                 anchor='w')  # 階層列

# Treeviewを配置
tree.grid(row=0, column=0, sticky="nsew")

# スクロールバーを作成
scrollbar = ctk.CTkScrollbar(treeview_frame,
                             orientation="vertical",
                              command=tree.yview)
scrollbar.grid(row=0, column=1, sticky="ns")

# Treeviewとスクロールバーを連携させる
tree.configure(yscrollcommand=scrollbar.set)

# フレーム内でTreeviewのサイズを調整
treeview_frame.grid_rowconfigure(0, weight=1)
treeview_frame.grid_columnconfigure(0, weight=1)


# Treeviewの階層列（#0）にソート機能を追加
def on_column_click(tree, column):
    global sort_reverse
    sort_reverse = not sort_reverse  # ソート順をトグル
    sort_treeview_recursive(tree, reverse=sort_reverse)

tree.heading('#0', text='スタック / ノートブック / ノート',
             command=lambda: on_column_click(tree, '#0'))

def sort_treeview_recursive(tree, parent="", reverse=False):
    """Treeviewの項目を再帰的に並べ替える"""
    # 親ノード直下の項目を取得
    children = [(tree.item(child, "text"), child) for child in tree.get_children(parent)]

    # テキストを基準に並べ替え
    children.sort(key=lambda t: t[0], reverse=reverse)

    # 並べ替え後に再配置
    for index, (_, child) in enumerate(children):
        tree.move(child, parent, index)

        # 子ノードも再帰的に並べ替え
        sort_treeview_recursive(tree, parent=child, reverse=reverse)


"""
選択中のデータベースを表示
"""
# 角丸のフレームを作成
# 選択中のデータベースの表示
# データベースのファイル名を表示するラベルを作成
database_label = ctk.CTkLabel(
    root,
    text="",
    font=("meiryo", 14),
    text_color="white",  # テキストの色
    fg_color="#4d4398",  # 背景色
    corner_radius=15,  # 角丸の半径
    anchor="w",  # 左詰め
    justify="left"  # テキストも左揃えに
)

# フレームを配置
database_label .place(
    relx=0.01,
    rely=0.082,
    relwidth=0.20,
    relheight=0.08
)

# 選択中のデータベースの表示
def update_database_label():
    """現在選択されているデータベースの名前をラベルに表示"""
    current_db = db_manager.get_current_database()
    # データベースファイル名を表示
    database_label.configure(
        text=f"現在のデータベース:\n{current_db.split('/')[-1]}",
        anchor="w"  # 左寄せに設定
    )

update_database_label()


######################################
## ウィジェットに紐づく機能(関数)
######################################
#ハンドラ関数を設定(各ボタン押した時の動作)
"""
データベースの切替
"""
def load_settings():
    """設定ファイルからデータベースパスを読み込む"""
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f).get("db_path", "")
    return ""

def save_settings(db_path):
    """データベースパスを設定ファイルに保存"""
    with open(SETTINGS_FILE, "w") as f:
        json.dump({"db_path": db_path}, f)

def db_switch():
    """データベースを切り替える"""
    global db_manager  # グローバル変数としてdb_managerを参照

    # ファイル選択ダイアログを開く
    initial_dir = load_settings() or "C:/"  # 設定ファイルから初期ディレクトリを取得、ない場合は C:/ を設定
    file_path = filedialog.askopenfilename(
        title="データベースファイルを選択してください",
        initialdir=initial_dir,
        filetypes=[("SQLiteデータベース", "*.db")]
    )

    if not file_path:
        messagebox.showinfo("キャンセル", "データベースの選択をキャンセルしました。")
        return

    # ファイル名が "stacknote" で始まるかを確認
    if not file_path.split("/")[-1].startswith("stack"):
        messagebox.showerror("エラー", "ファイル名が 'stack' で始まる必要があります。")
        return

    try:
        # データベースを切り替え
        db_manager.switch_database(file_path)
        # 選択したデータベースパスを保存
        save_settings(file_path)
        messagebox.showinfo("成功", f"データベースを '{file_path}' に切り替えました。")
        # Treeviewを更新するなどの処理
        clear_treeview(tree)
        load_treeview_data()
        # データベース名ラベルを更新
        update_database_label()

    except Exception as e:
        messagebox.showerror("エラー", f"データベースの切り替えに失敗しました。\n{e}")

# ボタンの設定
# 右クリックでdb_switchを起動するための関数
def on_right_click(event):
    """右クリックメニューを表示してデータベース切替"""
    db_switch()

# 右クリックイベントをバインド
database_label.bind("<Button-1>", on_right_click)

"""
新しいノート
"""
def show_new_note(show_confirmation=True):
    """Treeviewの選択を解除し、データボックスを空にして新しいノートを表示"""
    try:
        # 確認メッセージを表示するかどうかを制御
        if show_confirmation:
            # ユーザーに上書き確認を求める
            confirm = ask_yes_no("確認", f"新しいノートを表示しますか？\n入力中の内容はクリアされます")
            print(f"User confirmation: {confirm}")  # デバッグ用ログ
            if not confirm:
                return  # ユーザーが「いいえ」を選択した場合、処理を中断

        # デバッグ用：オブジェクトの状態を確認
        print(f"textbox exists: {textbox}")
        print(f"title_entry exists: {title_entry}")
        print(f"tree exists: {tree}")

        # データボックスを空にする
        textbox.delete("0.0", "end")  # テキストボックスの内容を削除
        title_entry.delete(0, tk.END)
        # Treeviewの選択を解除
        clear_treeview(tree)
        load_treeview_data()

        # ユーザーに通知
        print("新しいノートを表示しました。")  # デバッグ用
        if show_confirmation:
            show_message("新しいノート", "新しいノートの表示を行いました。")
    except Exception as e:
        print(f"エラー: {e}")  # デバッグ用ログ
        show_message("エラー", f"新しいノートの表示中にエラーが発生しました: {e}")



"""
スタック保存
"""
def stack_save_note():
    """Textboxの内容を新しいノートとして保存"""
    # Treeviewから現在選択されているスタックやノートブックを取得
    selected_item = tree.focus()

    # データベース接続
    conn = sqlite3.connect(db_manager.get_current_database())  # 切り替えたデータベースを参照
    cur = conn.cursor()
    # 'notes' テーブルからノート名を取得
    cur.execute("SELECT note FROM notes")
    rows = cur.fetchall()
    # ノート名のリストを作成
    note_names = [row[0] for row in rows]

    # 正規表現を使って "スタック" の数字部分を抽出
    stack_numbers = []
    for name in note_names:
        match = re.match(r"stack(\d+)", name)  # "スタック"に続く数字を取得
        if match:
            stack_numbers.append(int(match.group(1)))

    #タイトルを取得、空なら数字の最大値を取得
    if stack_numbers:
        max_stack_number = max(stack_numbers)
    else:
        max_stack_number = 0  # ノート(スタック○)が1つも存在しない場合

    stack =  "stack"
    notebook = "stack"

    # title_entryから新しいノート名を取得、空なら新しいノート名を作成
    new_stack_name = title_entry.get()  # title_entryから新しいノート名を取得
    if not new_stack_name:
        new_stack_name = f"stack{max_stack_number + 1}"

    # new_stack_name が "stack[数字]" の形式であるかを確認
    if re.match(r"^stack\d+$", new_stack_name):
        # "stack[数字]" の形式の場合、新しい番号で置き換える
        new_stack_name = f"stack{max_stack_number + 1}"

    # Textboxの内容を取得
    contents = textbox.get('1.0', 'end-1c')
    if not contents:
        show_message("警告", "内容が空です。何か入力してください。")
        return

    # 日付の取得
    day = str(date.today())

    # データベースに保存
    try:
        # 新規ノートを保存する
        sql = """INSERT INTO notes (stack, notebook, note, day, contents)
                 VALUES (?, ?, ?, ?, ?)"""
        cur.execute(sql, (stack, notebook, new_stack_name, day, contents))
        conn.commit()
        show_message("成功", "stackに保存されました。")

    except sqlite3.Error as e:
        show_message("エラー", f"データベースエラー: {e}")

    finally:
        conn.close()
        clear_treeview(tree)
        load_treeview_data()
        show_new_note(show_confirmation=False)  # メッセージなしで新しいノートを表示

"""
新規保存
"""
def save_new_note():
    """Textboxの内容を新しいノートとして保存"""
    # Treeviewから現在選択されているスタックやノートブックを取得
    selected_item = tree.focus()

    # メインウィンドウの位置を取得
    x = root.winfo_x()
    y = root.winfo_y()

    # Textboxの内容を取得
    contents = textbox.get('1.0', 'end-1c')

    # スタック名とノートブック名を手動で入力してもらう
    stack_dialog = ctk.CTkInputDialog(title="新規保存：スタック名",
                                      text="スタック名を入力してください\n（既存のスタックを選択、または新規作成）：")
    # ダイアログの位置をメインウィンドウと同じ位置に設定
    stack_dialog.geometry(f"+{x}+{y}")
    stack = stack_dialog.get_input()  # 入力結果を取得
    if not stack:
        show_message("警告", "スタック名を入力してください。")
        return

    notebook_dialog = ctk.CTkInputDialog(title="新規保存：ノートブック名",
                                         text="ノートブック名を入力してください\n（既存のノートブックを選択、または新規作成）：")
    # ダイアログの位置をメインウィンドウと同じ位置に設定
    notebook_dialog.geometry(f"+{x}+{y}")
    notebook = notebook_dialog.get_input()  # 入力結果を取得
    if not notebook:
        show_message("警告", "ノートブック名を入力してください。")
        return

    # ノート名を入力
    note_name = title_entry.get()  # title_entryから新しいノート名を取得
    if not note_name:
        note_dialog = ctk.CTkInputDialog(title="ノート名を入力",
                                        text="ノート名を入力してください：")
        # ダイアログの位置をメインウィンドウと同じ位置に設定
        note_dialog.geometry(f"+{x}+{y}")
        note_name = note_dialog.get_input()  # 入力結果を取得
        if not note_name:
            show_message("警告", "ノート名を入力してください。")
            return

    # 日付の取得
    day = str(date.today())

    # データベースに保存
    conn = sqlite3.connect(db_manager.get_current_database())  # 切り替えたデータベースを参照
    cur = conn.cursor()
    try:
        # 新規ノートを保存する
        sql = """INSERT INTO notes (stack, notebook, note, day, contents)
                 VALUES (?, ?, ?, ?, ?)"""
        cur.execute(sql, (stack, notebook, note_name, day, contents))
        conn.commit()
        show_message("成功", "新しいノートが保存されました。")

        # Treeviewを更新する処理
        # refresh_treeview()


    except sqlite3.Error as e:
        show_message("エラー", f"データベースエラー: {e}")

    finally:
        conn.close()
        clear_treeview(tree)
        load_treeview_data()
        show_new_note(show_confirmation=False)  # メッセージなしで新しいノートを表示

"""
上書き保存
"""
def save_existing_note(show_message_flag=True):
    """選択中のノートの内容を上書き保存"""
    # Treeviewから現在選択されているノートを取得
    selected_items = tree.selection()  # 複数選択された項目を取得
    if not selected_items:
        show_message("警告", "ノートが選択されていません。")
        return

    for item in selected_items:
        values = tree.item(item, "values")  # アイテムの値を取得

        # スタックやノートブックのアイテムかどうかを判定
        # スタックやノートブックはノート情報が不足している場合がある
        if len(values) < 1 or values[0] is None:  # id がない場合
            show_message("警告", "ノート情報が不足しています。")
            return  # 処理を中止

        elif isinstance(values, tuple) and len(values) == 1:
            show_message("警告", "ノート情報が不足しています。")
            return  # 処理を中止

        elif len(selected_items) > 1:
            show_message("警告", "複数のノートを選択しています。")
            return  # 処理を中止

    note_id = values[0]  # ノートのIDを取得

    # title_entryから新しいノート名を取得
    new_note = title_entry.get()

    if not new_note:
        if show_message_flag:
            show_message("警告", "ノート名を入力してください。")
        return

    note_text = new_note[:21] + "..." if len(new_note) > 21 else new_note

    if show_message_flag:
        confirm = ask_yes_no("上書確認", f"ノート「{note_text}」\nを上書きしますか？")
        if not confirm:
            return

    contents = textbox.get('1.0', 'end-1c').strip()
    day = str(date.today())

    conn = sqlite3.connect(db_manager.get_current_database())  # 切り替えたデータベースを参照
    cur = conn.cursor()
    try:
        sql = """
            UPDATE notes
            SET note = ?, day = ?, contents = ?
            WHERE id = ?
        """
        cur.execute(sql, (new_note, day, contents, note_id))  # IDは変更しない
        conn.commit()

        if show_message_flag:
            show_message("成功", "ノートが上書き保存されました。")

    except sqlite3.Error as e:
        if show_message_flag:
            show_message("エラー", f"データベースエラー: {e}")

    finally:
        conn.close()
        # Treeviewを更新
        clear_treeview(tree)
        load_treeview_data()
        select_treeview_item_by_id(note_id)


"""
削除:treeviewで選択した項目をデータベースから
"""
def delete_note():
    """選択したノートを削除する関数（確認メッセージ付き）"""
    # Treeviewから現在選択されているノートを取得
    selected_items = tree.selection()  # 複数選択された項目を取得
    if not selected_items:
        show_message("警告", "ノートが選択されていません。")
        return

    for item in selected_items:
        values = tree.item(item, "values")  # アイテムの値を取得

        # スタックやノートブックのアイテムかどうかを判定
        # スタックやノートブックはノート情報が不足している場合がある
        if len(values) < 1 or values[0] is None:  # id がない場合
            show_message("警告", "ノート情報が不足しています。")
            return  # 処理を中止

        elif isinstance(values, tuple) and len(values) == 1:
            show_message("警告", "ノート情報が不足しています。")
            return  # 処理を中止

    # 確認メッセージをループの外で表示
    confirm = ask_yes_no("削除確認", f"{len(selected_items)}件のノートを削除しますか？")
    if not confirm:
        return

    conn = sqlite3.connect(db_manager.get_current_database())
    cur = conn.cursor()

    try:
        for item in selected_items:
            # Treeviewの選択項目から値を取得
            values = tree.item(item, 'values')
            if len(values) < 1:  # IDが不足している場合
                continue

            note_id = values[0]  # ノートIDを取得

            # データベースから対応するレコードを削除
            cur.execute("DELETE FROM notes WHERE id = ?", (note_id,))

            # Treeviewから項目を削除
            tree.delete(item)

        conn.commit()  # 変更を保存
        show_message("成功", f"{len(selected_items)}件のノートを削除しました。")

    except sqlite3.Error as e:
        show_message("エラー", f"データベースエラー: {e}")

    finally:
        # データベース接続を閉じる
        conn.close()
        clear_treeview(tree)  # Treeviewのクリア
        load_treeview_data()  # データ再読み込み
        show_new_note(show_confirmation=False)  # メッセージなしで新しいノートを表示


"""
ノートの移動 (id使用版)
"""
def get_stacks():
    """データベースからすべてのスタック名を取得"""
    conn = sqlite3.connect(db_manager.get_current_database())  # 切り替えたデータベースを参照
    cur = conn.cursor()
    # 'notes' テーブルからスタック名を取得(DISTINCTで重複排除)
    cur.execute("SELECT DISTINCT stack FROM notes")
    stacks = [row[0] for row in cur.fetchall()]  # 結果をリストに変換
    conn.close()  # 正しい接続を閉じる
    return stacks

def get_notebooks():
    """データベースからすべてのノートブック名を取得"""
    conn = sqlite3.connect(db_manager.get_current_database())  # 切り替えたデータベースを参照
    cur = conn.cursor()
    # 'notes' テーブルからノートブック名を取得(DISTINCTで重複排除)
    cur.execute("SELECT DISTINCT notebook FROM notes")
    notebooks = [row[0] for row in cur.fetchall()]  # 結果をリストに変換
    conn.close()  # 正しい接続を閉じる
    return notebooks


def move_note():
    """選択したコンテンツを指定したスタックとノートブックに移動"""
    # Treeviewから現在選択されているノートを取得
    selected_items = tree.selection()  # 複数選択された項目を取得
    if not selected_items:
        show_message("警告", "編集するノートが選択されていません。")
        return

    for item in selected_items:
        values = tree.item(item, "values")  # アイテムの値を取得

        # スタックやノートブックのアイテムかどうかを判定
        # スタックやノートブックはノート情報が不足している場合がある
        if len(values) < 1 or values[0] is None:  # id がない場合
            show_message("警告", "ノート情報が不足しています。")
            return  # 処理を中止

        elif isinstance(values, tuple) and len(values) == 1:
            show_message("警告", "ノート情報が不足しています。")
            return  # 処理を中止

    # 移動先のスタックとノートブックを取得
    stack, notebook = show_combo_box()
    if not stack or not notebook:
        show_message("警告", "移動先が選択されていません。")
        return

    # データベース接続
    conn = sqlite3.connect(db_manager.get_current_database())  # 切り替えたデータベースを参照
    cur = conn.cursor()

    try:


        for item in selected_items:
            # Treeviewの選択項目から値を取得
            values = tree.item(item, 'values')
            if len(values) < 2:  # 必要な情報が不足している場合
                continue

            note_id = values[0]  # id を取得
            note = values[2]

            # ノート名が21文字を超える場合、表示しない
            note_text = ""  # 初期化

            if len(note) > 17:
                note_text = note[:17] + "..."  # 20文字に切り詰める
            else:
                note_text = note  # それ以外はそのまま

            # 現在のノート情報を取得
            cur.execute(
                "SELECT stack, notebook, note, contents FROM notes WHERE id = ?",
                (note_id,)
            )
            result = cur.fetchone()
            if not result:
                show_message("警告", f"ノートID {note_id} の情報が見つかりませんでした。")
                continue

            current_stack, current_notebook, current_note, current_contents = result

            # 現在と同じスタックとノートブックの場合はスキップ
            if current_stack == stack and current_notebook == notebook:
                show_message(
                    "警告",
                    f"ノート「{note_text}」\n現在と同じスタックとノートブックを選択しています。"
                )
                continue

            # 移動先が存在するか確認（省略可能：特定の組合せの存在確認をする場合）
            cur.execute(
                "SELECT COUNT(*) FROM notes WHERE stack = ? AND notebook = ?",
                (stack, notebook)
            )
            if cur.fetchone()[0] == 0:
                show_message(
                    "警告",
                    f"ノート「{note_text}」\n移動先の組合せは存在しません。"
                )
                continue

            # 日付の取得
            day = str(date.today())

            # 移動先に新しいノートを挿入
            insert_sql = """INSERT INTO notes (stack, notebook, note, day, contents)
                            VALUES (?, ?, ?, ?, ?)"""
            cur.execute(insert_sql, (stack, notebook, current_note, day, current_contents))

            # 元データを削除
            delete_sql = """DELETE FROM notes WHERE id = ?"""
            cur.execute(delete_sql, (note_id,))

            # Treeviewから項目を削除
            tree.delete(item)

        conn.commit()  # すべての操作を確定
        show_message("成功", f"{len(selected_items)}件のノートを移動しました。")

    except sqlite3.Error as e:
        # エラーメッセージを表示
        show_message("エラー", f"データベースエラー: {e}")

    finally:
        # データベース接続を閉じる
        conn.close()
        clear_treeview(tree)  # Treeviewのクリア
        load_treeview_data()  # データ再読み込み
        show_new_note(show_confirmation=False)  # メッセージなしで新しいノートを表示


"""
Treeviewを空にする関数(データベースには影響なし)
下記の関数使用時は以下の呼び出し
clear_treeview(tree)
"""
def clear_treeview(tree):
    """Treeviewの内容を全て削除して空にする"""
    for item in tree.get_children():
        tree.delete(item)


"""
treeviewをデータベース(現在選択中のもの)に繋げて表示
"""
def load_treeview_data():
    """Treeviewにデータベースの内容をロードする"""
    # Treeviewをクリア
    clear_treeview(tree)

    # 現在のデータベースからデータを取得
    query = """SELECT id, stack, notebook, note FROM notes"""
    try:
        rows = db_manager.fetch_all(query)
    except sqlite3.Error as e:
        messagebox.showerror("エラー", f"データ取得に失敗しました: {e}")
        return

    # 階層構造を作成
    stack_dict = {}  # スタックごとの親ノードを追跡
    notebook_dict = {}  # ノートブックごとの親ノードを追跡

    for note_id, stack, notebook, note in rows:
        # スタックが未登録なら追加
        if stack not in stack_dict:
            stack_id = tree.insert("", "end", text=stack, open=True)  # スタックノードを作成
            stack_dict[stack] = stack_id

        # ノートブックが未登録なら追加
        if (stack, notebook) not in notebook_dict:
            notebook_id = tree.insert(
                stack_dict[stack], "end", text=notebook, values=(notebook,), open=True
            )
            notebook_dict[(stack, notebook)] = notebook_id

        # ノートを追加（idを values に含める）
        tree.insert(
            notebook_dict[(stack, notebook)],
            "end",
            text=note,
            values=(note_id, notebook, note)
        )

# データのロード
load_treeview_data()

def initialize_database():
    """データベースの初期化"""
    query = """SELECT name FROM sqlite_master WHERE type='table' AND name='notes';"""
    try:
        result = db_manager.fetch_all(query)
        if not result:
            # テーブルが存在しない場合のみ作成
            create_table_query = """
            CREATE TABLE notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stack TEXT NOT NULL,
                notebook TEXT NOT NULL,
                note TEXT NOT NULL,
                day TEXT NOT NULL,
                contents TEXT NOT NULL
            )
            """
            db_manager.execute_query(create_table_query)
    except sqlite3.Error as e:
        messagebox.showerror("エラー", f"データベース初期化に失敗しました: {e}")



"""
treeviewの項目を選択すると、stacknoteの
contentsの内容をtextbox内に表示する
noteの内容をtitle_entry内に表示する
"""
def on_tree_note_select(event):
    selected_item = tree.focus()  # 選択された項目のIDを取得
    if not selected_item:  # 何も選択されていない場合は終了
        return

    # 選択された行の値を取得
    values = tree.item(selected_item, 'values')

    # valuesが空の場合（スタックやノートブックをクリックした場合）は処理をスキップ
    if not values or len(values) < 1:
        return  # 必要以上の警告を表示しない

    note_id = values[0]  # id を取得

    # データベースから note と contents を取得
    try:
        conn = sqlite3.connect(db_manager.get_current_database())  # 切り替えたデータベースを参照
        cur = conn.cursor()
        sql = """SELECT note, contents FROM notes WHERE id = ?"""
        cur.execute(sql, (note_id,))
        result = cur.fetchone()

        if result:
            note_from_db, content_from_db = result  # データベースから取得したノートと内容
            # ノートをタイトルエントリに設定
            title_entry.delete(0, tk.END)  # Entryをクリア
            title_entry.insert(0, note_from_db)  # ノートを表示

            # 内容を Textbox に設定
            textbox.delete('1.0', tk.END)  # Textbox をクリア
            textbox.insert('1.0', content_from_db)  # 内容を表示
        else:
            # データが見つからなかった場合はクリア
            title_entry.delete(0, tk.END)
            textbox.delete('1.0', tk.END)

    except sqlite3.Error as e:
        messagebox.showerror("データベースエラー", f"エラー: {str(e)}")
    finally:
        conn.close()

# Treeview の選択イベントにバインド
tree.bind("<<TreeviewSelect>>", on_tree_note_select)


"""
処理後にTreeviewで該当ノートの項目の選択を継続する
機能を付けたい関数に下記を記入
select_treeview_item_by_id(note_id)
"""
# 処理後にTreeviewで該当ノートの項目の選択を継続する　その1
def select_item_recursive(parent_item, note_id):
    """Treeview の親ノード以下を再帰的に探索して選択"""
    # 現在のノードの子ノードを取得
    for item in tree.get_children(parent_item):
        # ノードの値を取得
        item_values = tree.item(item, "values")
        if item_values and str(item_values[0]) == str(note_id):  # ID が一致する場合
            tree.selection_set(item)  # ノードを選択
            tree.focus(item)  # フォーカス
            tree.see(item)  # ノードをスクロールで表示
            return True  # 選択完了

        # 子ノードを再帰的に探索
        if select_item_recursive(item, note_id):
            return True

    return False

# 処理後にTreeviewで該当ノートの項目の選択を継続する　その2
def select_treeview_item_by_id(note_id):
    """note_id を基に Treeview の選択状態を復元"""
    # Treeview の全ての子ノードを取得
    for item in tree.get_children():
        # 子ノード（スタック）を再帰的に探索
        if select_item_recursive(item, note_id):
            break



######################################
## キー操作に紐づく機能
######################################
"""
検索機能の呼び出し(ctrl+F)
"""
# Control-f バインド
def open_search(event=None):
    CustomSearch(root, textbox)

root.bind("<Control-f>", open_search)


######################################
## Buttonウィジェット
######################################

# Buttonウィジェットの生成(CustomTkinter用)
Button_1 = ctk.CTkButton(
    root,
    text='新しいノート',
    text_color="white",  # テキストの色
    font=("meiryo", 14),  # フォント
    width=120,
    fg_color="green",  # 背景色
    corner_radius=10,  # 角丸
    command=show_new_note  # 関数をボタンに紐づけ
)

Button_2 = ctk.CTkButton(
    root,
    text='スタック保存',
    text_color = "white",  # テキストの色
    font = ("meiryo", 14),  # フォント
    width=120,
    fg_color = "green",  # 背景色
    corner_radius = 10,  # 角丸
    command=stack_save_note
)

Button_3 = ctk.CTkButton(
    root,
    text='新規保存',
    text_color = "white",  # テキストの色
    font = ("meiryo", 14),  # フォント
    width=120,
    fg_color = "green",  # 背景色
    corner_radius = 10,  # 角丸
    command=save_new_note
)

Button_4 = ctk.CTkButton(
    root,
    text='上書き保存',
    text_color = "white",  # テキストの色
    font = ("meiryo", 14),  # フォント
    width=120,
    fg_color = "green",  # 背景色
    corner_radius = 10,  # 角丸
    command=save_existing_note
)

Button_5 = ctk.CTkButton(
    root,
    text='ノートの移動',
    text_color = "white",  # テキストの色
    font = ("meiryo", 14),  # フォント
    width=120,
    fg_color = "green",  # 背景色
    corner_radius = 10, # 角丸
    command=move_note  # 移動ボタン
)

Button_6 = ctk.CTkButton(
    root,
    text='ノートの削除',
    text_color = "white",  # テキストの色
    font = ("meiryo", 14),  # フォント
    width=120,
    fg_color = "green",  # 背景色
    corner_radius = 10,  # 角丸
    command = delete_note  # 削除ボタン
)

# Buttonウィジェットの配置
Button_1.grid(column=0, row=0, padx=2, pady=10)
Button_2.grid(column=1, row=0, padx=2)
Button_3.grid(column=2, row=0, padx=2)
Button_4.grid(column=3, row=0, padx=2)
Button_5.grid(column=4, row=0, padx=2)
Button_6.grid(column=5, row=0, padx=2)

# メインループに入る
root.mainloop()

