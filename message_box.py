import customtkinter as ctk
from tkinter import messagebox

# メッセージ表示
class CustomMessageBox:
    _instance = None  # クラスレベルで唯一のインスタンスを管理

    def __init__(self, root, title="Message", message="", width="300", height="150"):
        """
        カスタムメッセージボックスを作成
        :param root: 親ウィジェット
        :param title: ダイアログのタイトル
        :param message: ダイアログ内のメッセージ
        """
        if CustomMessageBox._instance is not None and CustomMessageBox._instance.winfo_exists():
            return  # 既にダイアログが存在する場合は何もしない

        # メインウィンドウの位置を取得
        x = root.winfo_x()
        y = root.winfo_y()

        # ダイアログウィンドウの作成
        CustomMessageBox._instance = ctk.CTkToplevel(root)
        self.dialog = CustomMessageBox._instance  # ローカルインスタンス
        self.dialog.title(title)
        # サイズを引数として渡す
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")
        self.dialog.resizable(False, False)  # サイズ変更を無効化
        self.dialog.wm_attributes('-topmost', 1)  # 前面に表示

        # メッセージラベル
        label = ctk.CTkLabel(self.dialog, text=message)
        label.pack(pady=20)

        # 閉じるボタン
        close_button = ctk.CTkButton(self.dialog, text="閉じる", command=self.close)
        close_button.pack(pady=10)

    def close(self):
        """ダイアログを閉じる"""
        if CustomMessageBox._instance is not None:
            CustomMessageBox._instance.destroy()
            CustomMessageBox._instance = None  # グローバルインスタンスをリセット


# yes/no表示
class CustomYesNoBox:
    _instance = None  # クラスレベルで唯一のインスタンスを管理

    def __init__(self, root, title="Message", message="", width="320", height="150"):
        """
        カスタムメッセージボックスを作成
        :param root: 親ウィジェット
        :param title: ダイアログのタイトル
        :param message: ダイアログ内のメッセージ
        """
        if CustomYesNoBox._instance is not None and CustomYesNoBox._instance.dialog.winfo_exists():
            return  # 既にダイアログが存在する場合は何もしない

        # メインウィンドウの位置を取得
        x = root.winfo_x()
        y = root.winfo_y()

        # ダイアログウィンドウの作成
        CustomYesNoBox._instance = self
        self.result = None  # 結果を保存する変数
        self.dialog = ctk.CTkToplevel(root)
        self.dialog.title(title)
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")
        self.dialog.resizable(False, False)  # サイズ変更を無効化
        self.dialog.wm_attributes('-topmost', 1)  # 前面に表示

        # 結果の初期化
        self.result = None

        # メッセージラベル
        label = ctk.CTkLabel(self.dialog, text=message)
        label.grid(row=0, column=0, columnspan=2, pady=20)

        # ボタンの定義
        yes_button = ctk.CTkButton(self.dialog, text="はい", command=self.on_yes)
        yes_button.grid(row=1, column=0, padx=10, pady=10)

        no_button = ctk.CTkButton(self.dialog, text="いいえ", command=self.on_no)
        no_button.grid(row=1, column=1, padx=10, pady=10)

        # ダイアログが閉じるまで待機
        self.dialog.wait_window(self.dialog)

    def on_yes(self):
        """「はい」が押されたときの処理"""
        self.result = True
        self.close()

    def on_no(self):
        """「いいえ」が押されたときの処理"""
        self.result = False
        self.close()

    def close(self):
        """ダイアログを閉じる"""
        if CustomYesNoBox._instance is not None:
            CustomYesNoBox._instance.dialog.destroy()
            CustomYesNoBox._instance = None

    @staticmethod
    def show(root, title="Message", message="", width="320", height="150"):
        """
        ダイアログを表示し、結果を返す
        """
        box = CustomYesNoBox(root, title, message, width, height)
        return box.result


# コンボボックス用(2個使用)
class CustomComboBox:
    _instance = None  # クラスレベルで唯一のインスタンスを管理

    def __init__(self, root, title="Message", message="", options1=None, options2=None, width="310", height="210"):
        """
        カスタムコンボボックスを作成
        :param root: 親ウィジェット
        :param title: ダイアログのタイトル
        :param message: ダイアログ内のメッセージ
        :param options1: 1つ目のコンボボックスの選択肢
        :param options2: 2つ目のコンボボックスの選択肢
        """
        if CustomComboBox._instance is not None and CustomComboBox._instance.dialog.winfo_exists():
            return  # 既にダイアログが存在する場合は何もしない

        # メインウィンドウの位置を取得
        x = root.winfo_x()
        y = root.winfo_y()

        # ダイアログウィンドウの作成
        CustomComboBox._instance = self
        self.result1 = None  # 1つ目のコンボボックスの結果
        self.result2 = None  # 2つ目のコンボボックスの結果
        self.dialog = ctk.CTkToplevel(root)
        self.dialog.title(title)
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")
        self.dialog.resizable(False, False)  # サイズ変更を無効化
        self.dialog.wm_attributes('-topmost', 1)  # 前面に表示

        # メッセージラベル
        label = ctk.CTkLabel(self.dialog, text=message)
        label.grid(row=0, column=0, columnspan=2, padx=30, pady=20)

        # 1つ目のコンボボックス
        label1 = ctk.CTkLabel(self.dialog, text="スタック:")
        label1.grid(row=1, column=0, padx=10, pady=5)
        self.combo_box1 = ctk.CTkComboBox(self.dialog, values=options1 or [])
        self.combo_box1.grid(row=1, column=1, padx=0, pady=5, sticky="w")

        # 2つ目のコンボボックス
        label2 = ctk.CTkLabel(self.dialog, text="ノートブック:")
        label2.grid(row=2, column=0, padx=10, pady=5)
        self.combo_box2 = ctk.CTkComboBox(self.dialog, values=options2 or [])
        self.combo_box2.grid(row=2, column=1, padx=0, pady=5, sticky="w")

        # OKボタン
        ok_button = ctk.CTkButton(self.dialog, text="OK", command=self.on_ok)
        ok_button.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

        # ダイアログが閉じるまで待機
        self.dialog.wait_window(self.dialog)

    def on_ok(self):
        """OKボタンが押されたときの処理"""
        self.result1 = self.combo_box1.get()
        self.result2 = self.combo_box2.get()
        self.close()

    def close(self):
        """ダイアログを閉じる"""
        if CustomComboBox._instance is not None:
            CustomComboBox._instance.dialog.destroy()
            CustomComboBox._instance = None

    @staticmethod
    def show(root, title="Message", message="", options1=None, options2=None, width="320", height="200"):
        """
        ダイアログを表示し、2つの選択結果を返す
        """
        box = CustomComboBox(root, title, message, options1, options2, width, height)
        return box.result1, box.result2


# 検索画面
class CustomSearch:
    _instance = None  # クラスレベルで唯一のインスタンスを管理

    def __init__(self, root, textbox, title="検索", width="300", height="150"):
        """
        カスタム検索ウィンドウを作成
        :param root: 親ウィジェット
        :param textbox: 検索対象のTextboxウィジェット
        :param title: ダイアログのタイトル
        :param width: ダイアログの幅
        :param height: ダイアログの高さ
        """
        if CustomSearch._instance is not None and CustomSearch._instance.winfo_exists():
            return  # 既にダイアログが存在する場合は何もしない

        # メインウィンドウの位置を取得
        x = root.winfo_x()
        y = root.winfo_y()

        # ダイアログウィンドウの作成
        CustomSearch._instance = ctk.CTkToplevel(root)
        self.dialog = CustomSearch._instance  # ローカルインスタンス
        self.dialog.title(title)
        # サイズを引数として渡す
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")
        self.dialog.resizable(False, False)  # サイズ変更を無効化
        self.dialog.wm_attributes('-topmost', 1)  # 前面に表示

        # ラベル
        search_label = ctk.CTkLabel(self.dialog, text="検索:")
        search_label.grid(row=0, column=0, padx=5, pady=10)

        # 検索エントリ
        self.search_entry = ctk.CTkEntry(self.dialog, width=280)
        self.search_entry.grid(row=1, column=0, padx=10, pady=10)

        # 検索ボタン
        search_button = ctk.CTkButton(self.dialog, text="検索", command=lambda: self.perform_search(textbox))
        search_button.grid(row=2, column=0, padx=0, pady=10)

        # エンターキーで検索を実行
        self.search_entry.bind("<Return>", lambda event: self.perform_search(textbox))

        # ダイアログを閉じた時にハイライトをクリアする処理
        self.dialog.protocol("WM_DELETE_WINDOW", lambda: self.on_close(textbox))

    def perform_search(self, textbox):
        """検索処理を実行"""
        query = self.search_entry.get()
        if query:
            """検索文字列をハイライト"""
            textbox.tag_remove("highlight", "1.0", "end")  # 以前のハイライトをクリア

            if not query:
                return

            start_index = "1.0"  # 検索開始位置
            while True:
                # 検索実行
                start_index = textbox.search(query, start_index, stopindex="end")
                if not start_index:  # 一致しなければ終了
                    break

                # ハイライト設定
                end_index = f"{start_index}+{len(query)}c"
                textbox.tag_add("highlight", start_index, end_index)
                start_index = end_index  # 次の位置に進む

            # ハイライトスタイルを設定
            textbox.tag_config("highlight", background="yellow", foreground="black")
        else:
            CustomMessageBox(self.dialog,
                             title="警告",
                             message="検索キーワードを入力してください！"
                             )

    def on_close(self, textbox):
        """ダイアログを閉じたときにハイライトをクリア"""
        textbox.tag_remove("highlight", "1.0", "end")  # ハイライトをクリア
        self.dialog.destroy()  # ダイアログを閉じる




######################################
## 現状使用ないクラス
######################################
# コンボボックス表示1個だけ
class CustomComboBoxOne:
    _instance = None  # クラスレベルで唯一のインスタンスを管理

    def __init__(self, root, title="Combo Box", message="", options=None, width="400", height="300"):
        """
        カスタムコンボボックスウィンドウを作成
        :param root: 親ウィジェット
        :param title: ダイアログのタイトル
        :param message: ラベルメッセージ
        :param options: コンボボックスに表示する選択肢
        """
        if CustomComboBox._instance is not None and CustomComboBox._instance.dialog.winfo_exists():
            return  # 既にダイアログが存在する場合は何もしない

        # メインウィンドウの位置を取得
        x = root.winfo_x()
        y = root.winfo_y()

        # デフォルトの選択肢
        if options is None:
            options = ["Option 1", "Option 2", "Option 3"]

        # ダイアログウィンドウの作成
        CustomComboBox._instance = self
        self.result = None  # 選択結果を保存
        self.dialog = ctk.CTkToplevel(root)
        self.dialog.title(title)
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")
        self.dialog.wm_attributes('-topmost', 1)  # 前面に表示

        # ラベル
        label = ctk.CTkLabel(self.dialog, text=message)
        label.grid(row=0, column=0, columnspan=2, pady=10)

        # コンボボックス
        self.combo_box = ctk.CTkComboBox(self.dialog, values=options)
        self.combo_box.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # OKボタン
        ok_button = ctk.CTkButton(self.dialog, text="OK", command=self.on_ok)
        ok_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.dialog.wait_window(self.dialog)  # ダイアログが閉じるまで待機

    def on_ok(self):
        """OKボタンが押されたときの処理"""
        self.result = self.combo_box.get()  # コンボボックスで選択された値を取得
        self.close()

    def close(self):
        """ダイアログを閉じる"""
        if CustomComboBox._instance is not None:
            CustomComboBox._instance.dialog.destroy()
            CustomComboBox._instance = None

    @staticmethod
    def show(root, title="Combo Box", message="", options=None, width="320", height="150"):
        """
        ダイアログを表示し、選択された値を返す
        """
        box = CustomComboBox(root, title, message, options, width, height)
        return box.result
