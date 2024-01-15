from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import traceback
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///E:/Python/testTask_blogSite/db/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)  # Изменил на user_name
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

    @classmethod
    def add_post(cls, title, content, user_id):
        post = cls(title=title, content=content, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return post

def generate_unique_id():
    return random.randint(1, 10000)

def get_current_user_id():
    while True:
        new_id = generate_unique_id()
        existing_user = User.query.filter_by(id=new_id).first()
        if not existing_user:
            return new_id

@app.route('/createpost', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user_id = get_current_user_id()

        try:
            Post.add_post(title, content, user_id)
            flash('Post created successfully.', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error creating post: {str(e)}', 'danger')
            traceback.print_exc()

    return render_template('createpost.html')

@app.route('/registration', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(user_name=user_name).first()
        if existing_user:
            flash('Username already exists. Please choose another one.', 'danger')
        else:
            new_user = User(user_name=user_name)
            new_user.set_password(password)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful. You can now log in.', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                flash(f'Error during registration: {str(e)}', 'danger')
                traceback.print_exc()
                db.session.rollback()

    return render_template('registration.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
@app.route('/authorisation', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['username']  # Изменил на user_name
        password = request.form['password']
        user = User.query.filter_by(user_name=user_name).first()  # Изменил на user_name
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful.', 'success')
            return redirect(url_for('index'))
        else:
            print("invalid pass")
            flash('Invalid user_name or password. Please try again.', 'danger')
    return render_template('authorisation.html', current_user=current_user)

@app.route('/')
def index():
    return render_template('authorisation.html')

@app.route('/posts')
def posts():
    return render_template('posts.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

if __name__ == '__main__':
    app.secret_key = 'your_secret_key'
    app.run(debug=True)
