from flask import render_template, Flask,redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy as _BaseSQLAlchemy
from sqlalchemy import desc

app=Flask(__name__)

app.config['SQLALCHMEY_DATABASE_URI'] ="postgresql://cloudgame_owner:3QWMEHbAr0eO@ep-jolly-sun-a5l8s2ys.us-east-2.aws.neon.tech/cloudgame?sslmode=require"

#class for database operation


class SQLAlchemy(_BaseSQLAlchemy):
    def apply_pool_defaults(self, app, options):
        super(SQLAlchemy, self).apply_pool_defaults(self, app, options)
        options["pool_pre_ping"] = True

# run database

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(120), nullable=False)
    fullname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(20),nullable=True)
    points = db.Column(db.Integer,default=50)
    upvotes = db.Column(db.Integer,default=0)
    Badge = db.Column(db.String(20),default="Rookie")



class Post(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    Description = db.Column(db.String(240),nullable=False)
    img_url= db.Column(db.String(120), nullable=False


with app.app_context():
    db.create_all()


app.secret_key="superhighsecretlock"

@app.route('/',methods=['POST','GET'])
def index():
    return render_template("index.html")


@app.route('/login',methods=['POST','GET'])
def login():
    msg=''
    if request.method=='POST':
        uname = request.form["uname"]
        pwd = request.form["pswd"]
        auth = User.query.filter_by(fullname=uname,password=pwd).all()
        if auth:
            session['uname']=uname
            session['pwd']=pwd
            return redirect(url_for('home'))
        else:
            msg="Invalid Username/Password"
    return render_template("login.html",message=msg)
