# プロジェクト名
CustomTkinter-SQLite-Note-Taking-App


## 概要
文章をローカルで作成・整理しやすいシンプルなノートの作成


## 主な機能
1. **新しいノート**
   - 空のタイトルとノートを表示
   - 保存前の編集状態

2. **スタック保存**
   - ノートを新しい「スタック」として保存
   - 未入力時、自動で「stack1」「stack2」などの名前を付与

3. **新規保存**
   - 指定したスタックやノートブック名で保存
   - 既存のスタックに追加可能

4. **上書き保存**
   - 編集内容を既存ノートに保存

5. **ノートの移動**
   - 他のスタックやノートブックに移動（複数選択対応）

6. **ノートの削除**
   - 選択したノートを削除（複数選択対応）

7. **現在のデータベース**
   - 現在作業中のデータベースを表示
   - デフォルトでは「stacknote.db」がアプリケーションの実行ディレクトリに自動生成される
   - データベースのファイル名の変更は可能だが、ファイル名は「stack」で始める必要がある
   - クリックして、別のデータベースファイルを選択し切り替え可能

8. **ソート機能**
   - ツリービューのヘッダークリックで昇順・降順を切替可能

  ![](images\image1.jpg)


## プロジェクトの構造
- stacknote：メインアプリケーションコード
- message_box：メッセージ関連のモジュール
- db_operation：データベース関連のモジュール

アプリを実行する時は、全てのプロジェクトファイルが同じディレクトリ内である必要がある


## 必要条件
- OS：Windows 10/11（64ビット版推奨）
- Python：3.6以降推奨
- 必要なライブラリ: customtkinter


## セットアップ手順
1. **Pythonをインストール**
   - [公式サイト](https://www.python.org/)からPython 3.6以降をインストール

2. **ノートファイルのダウンロード**
   - リポジトリ全体をダウンロードする場合
     - (a), GitHub のリポジトリページにアクセス
     - (b), 右にある緑色の「コード」ボタンをクリック
     - (c), 「Download ZIP」をクリック
     - (d), ダウンロードしたフォルダを任意の場所に移動し解凍

3. **ターミナルでカレントディレクトリを指定**
   - ターミナル（コマンドプロンプト）で、アプリケーションのディレクトリに移動
   ```bash
   cd [ディレクトリの絶対パス]　
   ```
   例：
   ```bash
   cd C:\Users\[ユーザー名]\pythonproject\CustomTkinter-SQLite-Note-Taking-App-main　
   ```
   
4. **必要なライブラリをインストール**
   ```bash
   pip install customtkinter

5. **メインアプリケーションコードを実行**
   ```bash
   python stacknote.py
   ```
   
## 実行ファイル化手順(PyInstallerを使用)
1. **PyInstallerをインストール**
   - ターミナル(コマンドプロンプト)で、下記を入力して実行:
   ```bash
   pip install pyinstaller

2. **カレントディレクトリを指定**
   ```bash
   cd [ディレクトリの絶対パス]　
   ```
   
3. **実行ファイル化**
   - ファイルのアイコン無しで実行化の場合:
   ```bash
   pyinstaller --onefile stacknote.py
   ```
   - ファイルのアイコンを付けたい実行化の場合:
   ```bash
   pyinstaller --onefile --windowed --icon=stack_icon.ico stacknote.py
   ```
      - 上記いずれかを実行するとdistフォルダ内に実行ファイルが生成される


4. **依存ファイルを明示的に含める**
     - (a), 以下のコマンドを実行して .specファイル(stacknote.spec)を生成:
   ```bash
   pyinstaller --onefile --name stacknote stacknote.py
   ```
     - (b), .spec ファイルを編集
   ```bash
	  a = Analysis(
           ['stacknote.py'],
           pathex=['.'],
           binaries=[],
           datas=[('message_box.py', '.'), ('db_operation.py', '.')],  # 依存ファイル2つを指定
           ) 
	
	  # アイコンを付ける場合は追加
	  exe = EXE(
           ...
           icon='stack_icon.ico',  # アイコンを指定
           ...
           )
   ```

     - (c), .spec ファイルを使用して再ビルド
   ```bash
   pyinstaller stacknote.spec
   ```
   
5. **作成した実行ファイルについての備考**
     - distフォルダ内の「stacknote.exe」をクリックすると実行される
     - ショートカットを作成した場合、「staknote.db」(デフォルトのデータベース)は実行ファイルのフォルダに生成される
     - 一度データベースを選択すると、次回選択も同じフォルダを開く(データベース専用のフォルダを作ると楽)


## ライセンス
- MIT License

