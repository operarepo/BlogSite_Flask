from flask import Flask, render_template, request, flash, redirect, url_for
from sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import traceback


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////db/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('posts', lazy=True))

    # Добавление нового поста
    @classmethod
    def add_post(cls, title, content, user_id):
        post = cls(title=title, content=content, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return post

    # Получение поста по его ID
    @classmethod
    def get_post(cls, post_id):
        return cls.query.get(post_id)


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
                return redirect(url_for('index'))
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
    app.secret_key = 'your_secret_key'
    app.run(debug=True)
    
