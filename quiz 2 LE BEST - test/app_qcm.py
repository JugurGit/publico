import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import json

#https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3

app = Flask(__name__)
app._static_folder = "C:/Users/jugur/Documents/projet Git/quiz 2 LE BEST/templates/static"

app.config['SECRET_KEY'] = 'test'

def get_db_connection():
    conn = sqlite3.connect('database_qcm.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM questions WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

def get_option(question_id):
    conn = get_db_connection()
    option = conn.execute('SELECT * FROM options WHERE question_id = ?',
                        (question_id,)).fetchall()
    conn.close()
    if post is None:
        abort(404)
    return option

def get_questions():
    connection = sqlite3.connect('database_qcm.db')
    connection.row_factory = sqlite3.Row  # This enables column access by name: row['column_name'] 
    cur = connection.cursor()

    cur.execute("SELECT * FROM questions")
    questions_rows = cur.fetchall()

    questions_list = []
    for question_row in questions_rows:
        cur.execute("SELECT option FROM options WHERE question_id=?", (question_row['id'],))
        options_rows = cur.fetchall()

        options_list = [option_row['option'] for option_row in options_rows]

        question_dict = {
            'numb': question_row['id'],
            'qcm': question_row['qcm'],
            'question': question_row['question'],
            'answer': question_row['answer'],
            'options': options_list
        }
        questions_list.append(question_dict)

    connection.close()

    js = "let questions = " + json.dumps(questions_list) + ";"
    with open('templates/static/questions.js', 'w') as f:
        f.write(js)

@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        get_questions() 
    return render_template('accueil_qcm.html')

@app.route('/admin')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM questions').fetchall()
    conn.close()
    return render_template('index_qcm.html', posts=posts)

@app.route('/admin/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    option = get_option(post_id)
    return render_template('post_qcm.html', post=post, option=option)

@app.route('/admin/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Question is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO questions (qcm, question, answer) VALUES (?, ?, ?)',
                          (0, title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create_qcm.html')

@app.route('/admin/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE questions SET question = ?, answer = ?'
                          ' WHERE id = ?',
                          (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit_qcm.html', post=post)

@app.route('/admin/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM questions WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['question']))
    return redirect(url_for('index'))

app.run(debug = False)
