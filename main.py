from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from models import User
import traceback

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///E:/Python/testTask_blogSite/db/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#db.init_app(app)




# Маршрут для регистрации
@app.route('/registration', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose another one.', 'danger')
        else:
            new_user = User(username=username)
            new_user.set_password(password)

            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful. You can now log in.', 'success')
                return redirect(url_for('authorisation'))
            except Exception as e:
                flash(f'Error during registration: {str(e)}', 'danger')
                traceback.print_exc()  # Добавляем вывод traceback в консоль
                db.session.rollback()

    return render_template('registration.html')

# Маршрут для авторизации
@app.route('/authorisation', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            flash('Login successful.', 'success')
            return redirect(url_for('index'))  # Перенаправление на главную страницу

            # Здесь можно добавить логику входа
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('authorisation.html')



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts')
def posts():
    return render_template('posts.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

if __name__ == '__main__':
    app.run(debug=True)
    