from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import yaml

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ('mysql://root:@localhost/MP_database.sql')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
db = yaml.load(open('database.yaml'))
app.config('MYSQL_HOST')
app.config('MYSQL_USER')
app.config('MYSQL_PASSWORD')
app.config('MYSQL_DB')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User  {self.username}>'

@app.route('/add_user', methods=['POST'])
def add_user():
    new_user = User(username='newuser', email='email@example.com')
    db.session.add(new_user)
    db.session.commit()
    return f'User  {new_user.username} added!'

@app.route('/users')
def get_users():
    users = User.query.all()
    return '<br>'.join([f'ID: {user.id}, Username: {user.username}, Email: {user.email}' for user in users])

@app.route('/update_user/<int:user_id>', methods=['POST'])
def update_user(user_id):
    user = User.query.get(user_id)
    if user:
        user.username = 'updateduser'
        db.session.commit()
        return f'User  {user_id} updated!'
    return 'User  not found!'

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return f'User  {user_id} deleted!'
    return 'User  not found!'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
    db.create_all()