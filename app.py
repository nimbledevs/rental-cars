# import the Flask library
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import bcrypt
app = Flask(__name__) 
app.debug = True

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "helo this is my secret key"
db=SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
    def __init__(self,email,password,name):
        self.username = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
with app.app_context():
    db.create_all()

#  Home page route 

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        user = User(email, password, username)
        db.session.add(user)
        db.session.commit()
        return render_template('login.html')
    return render_template('register.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            print(user)
            return render_template('home.html',{user:user
                                                })
        else:
            return render_template('login.html', error='Invalid email or password, Please try again')
    return render_template('login.html')
 
# Start with flask web app with debug as

if __name__ == "__main__":
    app.run(debug=True)
