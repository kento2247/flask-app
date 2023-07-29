# flask-app

1. [git](https://git-for-windows.github.io/)をインストールする

2. 以下を実行（プログラムをコピー: 初回のみ）

   `git clone https://github.com/kento2247/flask-app.git`

3. [VScode](https://code.visualstudio.com/)がインストールされていなければ、インストールする

4. python がインストールされているかを以下のコマンドで確認

   `python -V`

   **もし Python 3.\_*.*と表示されなければ**

   - Pyhonをインストールする
     
     Windows app storeから最新のPythonをインストール

   - 再び以下のコマンドを実行して、インストールされているか確認

   `python -V`

5. Flask をインストールする

   `pip install flask`

   - ちゃんとインストールできてるかを確認
     ```pip list```

7. sqlite3をインストールする
   - [sqlite3.zip](https://github.com/kento2247/flask-app/files/12208010/sqlite3.zip)をダウンロード
   - Cドライブ直下やルートディレクトリなど、普段使わないところに解凍したsqlite3フォルダを置く
   - sqlite3フォルダを右クリックして、「パスをコピー」を押す
   - 「設定」→「検索」→「環境変数」→「ユーザー環境変数 / PATH」→「編集」→「追加」
   - 2個前でコピーしたパスをペーストして保存
