from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__, template_folder="../templates")


def get_db():
    conn = sqlite3.connect('/tmp/database.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL
    )
    ''')

    conn.commit()
    return conn


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':

        user_input = request.form.get('content')

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            'INSERT INTO submissions (content) VALUES (?)',
            (user_input,)
        )

        conn.commit()
        conn.close()

        return "Saved Successfully!"

    return render_template("index.html")


@app.route('/results')
def results():

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM submissions')
    data = cursor.fetchall()

    conn.close()

    return "<h1>Submissions</h1>" + "".join(
        [f"<p>{row[1]}</p>" for row in data]
    )


app = app
