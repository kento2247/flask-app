import base64
import hashlib
import sqlite3
from datetime import timedelta

from flask import Flask, flash, g, redirect, render_template, request, session, url_for

DATABASE = "sample.db"  # データベースファイルの名前を指定
app = Flask(__name__, static_folder="./static")
app.config["SECRET_KEY"] = "72224660711"  # port保護のためのキー


@app.before_request
def before_request():  # リクエストのたびにセッションの寿命を更新する
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=15)
    session.modified = True


def get_db():  # DATABASEへ接続する
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


def db_insert(table, data_obj):  # data={key:value}
    conn = get_db()
    cur = conn.cursor()
    query_str = f"INSERT INTO {table} ("
    values_str = ""
    values = []
    keys = data_obj.keys()
    for i in keys:
        query_str += i + ", "
        values_str += "?" + ", "
        values.append(data_obj[i])
    query_str = query_str[:-2]
    values_str = values_str[:-2]
    query_str += f") VALUES ({values_str})"
    try:
        cur.execute(query_str, values)
        conn.commit()  ## 更新はcommitが必要
        return True
    except sqlite3.Error as e:
        print("sqlite3.Error occurred:", e.args[0])
        conn.commit()  ## 更新はcommitが必要
        return False


def db_delete(table, where):
    conn = get_db()
    cur = conn.cursor()
    query_str = f"DELETE from {table} where {where}"
    try:
        cur.execute(query_str)
        conn.commit()  ## 更新はcommitが必要
        return True
    except sqlite3.Error as e:
        print("sqlite3.Error occurred:", e.args[0])
        conn.commit()  ## 更新はcommitが必要
        return False


def db_get_json(table, query):
    return_json = []
    conn = get_db()
    cur = conn.cursor()
    query_str = query
    if query == "":
        query_str = "SELECT * FROM " + table
    try:
        records = cur.execute(query_str)
    except sqlite3.Error as e:
        print("doing query is: " + query)
        print("sqlite3.Error occurred:", e.args[0])
        return {}
    keys = []
    for num, record in enumerate(records):
        if num == 0:
            keys = record.keys()
        temp_obj = {}
        for index, val in enumerate(record):
            temp_obj[keys[index]] = val
        return_json.append(temp_obj)
    return return_json


def db_update(table, value, where):
    conn = get_db()
    cur = conn.cursor()
    query_str = f"UPDATE {table} SET {value} WHERE {where}"
    try:
        cur.execute(query_str)
        conn.commit()  ## 更新はcommitが必要
        return True
    except sqlite3.Error as e:
        print("sqlite3.Error occurred:", e.args[0])
        conn.commit()  ## 更新はcommitが必要
        return False


@app.teardown_appcontext
def close_connection(exception):  # アプリ終了時にデータベース接続を閉じる
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


@app.route("/")
def home():
    result = db_get_json(
        "", f'SELECT * FROM USERS u WHERE u.username="{"admin"}"'
    )  # adminユーザーが登録されているか確認する
    if result == []:  # adminユーザーが登録されていない場合、登録する
        h = hashlib.md5("admin".encode())  # パスワードは平文ではなくハッシュ値で暗号化する
        data_obj = {"username": "admin", "password": h.hexdigest()}
        db_insert("USERS", data_obj)  # データベースにadminユーザーを登録する

    if "user_id" not in session:  # セッションにuser_idがない場合、未ログインなのでusernameを渡さずにHTMLをレンダリング
        return render_template("home.html")
    result = db_get_json(
        "", f'SELECT * FROM USERS u WHERE u.username="{session["user_id"]}"'
    )  # adminユーザーが登録されているか確認する
    print(result)
    return render_template("home.html", username=result[0]["username"])


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("home"))
    error = None
    # POSTはこの関数の一番下のlogin.htmlから呼ばれ、その中のフォームを送信する。フォームの内容に基づき、ユーザ情報を照合する
    if request.method == "POST":
        # フォームの内容を取得する
        username = request.form["username"]
        password = request.form["password"]
        # パスワードは平文ではなくハッシュ値で照合する
        h = hashlib.md5(password.encode())
        conn = get_db()
        cur = conn.cursor()
        user = cur.execute(
            "SELECT * FROM USERS WHERE username = ? AND password = ?",
            (username, h.hexdigest()),
        ).fetchone()
        if user is None:
            # ユーザ認証されなかった場合、エラーメッセージをレンダリングする。メッセージはこのように引数で渡すこともできるし、else以下のようにflashを使用することもできる。
            error = "Invalid username or password"
        else:
            # ユーザ認証された場合、セッションに記録する
            session["user_id"] = username
            # flashメッセージを設定する
            flash("Logged in")
            return redirect(url_for("home"))
    return render_template("login.html", error=error)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    request_valid = True
    if request.method == "POST":  # フォームの内容を取得し、バリデーションを行う。エラーがあればflashメッセージで通知する
        username = request.form["username"]
        password = request.form["password"]
        confirm = request.form["confirm"]
        if not username:
            flash("ユーザー名を入力してください")
            request_valid = False
        if not password:
            flash("パスワードを入力してください")
            request_valid = False
        if password != confirm:
            flash("確認用のパスワードが一致しません")
            request_valid = False
        result = db_get_json("", f'SELECT * FROM USERS u WHERE u.username="{username}"')
        if result != []:  # 既に同じユーザー名が登録されている場合、エラーメッセージを表示する
            flash("This username is already taken")
            request_valid = False
        if request_valid:  # 新しいユーザーを作成する
            h = hashlib.md5(password.encode())  # パスワードは平文ではなくハッシュ値で暗号化する
            data_obj = {"username": username, "password": h.hexdigest()}
            db_insert("USERS", data_obj)  # データベースにユーザー情報を追加する
            return redirect(url_for("login"))  # ログインページにリダイレクトする
    return render_template("signup.html")


@app.route("/logout")
def logout():
    if session.pop("user_id", None):
        flash("ログアウトしました")
    return redirect(url_for("home"))  # ログアウト後はホームにリダイレクトする


@app.route("/game", methods=["GET", "POST"])
def game():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        # ゲーム処理
        return render_template("game.html", form={})
    else:  # GET
        return render_template("game.html", form={})


@app.route("/vote", methods=["GET", "POST"])
def vote():
    if "user_id" not in session:
        return redirect(url_for("login"))

    labels = ""
    values = ""
    result = db_get_json("VOTES", "")
    vote_values = {}
    for i in result:
        title = i["title"]
        num = int(i["num"])
        labels += f"{title},"
        values += f"{num},"
        vote_values[title] = num
    labels = labels[:-1]  # 最後のカンマを削除
    values = values[:-1]  # 最後のカンマを削除
    graph_data = {
        "chart_labels": labels,
        "chart_data": values,
        "chart_title": "OS集計",
        "chart_target": "",
    }

    if request.method == "POST":
        selected = request.form["vote"]
        if selected == "Mac OS":
            print("mac os")
        elif selected == "Windows":
            print("windows")
        elif selected == "Linux":
            print("linux")
        flash(f"投票しました\n{selected}: {vote_values[selected]}→{vote_values[selected]+1}")
        db_update("VOTES", f"num={vote_values[selected]+1}", f"title='{selected}'")

        return redirect(url_for("vote"))
    else:  # GET
        return render_template("vote.html", form={}, graph_data=graph_data)


if __name__ == "__main__":
    app.run(debug=True)
