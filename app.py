from flask import Flask,request,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pyshorteners
import os


short_url=""
orig_url=""

app=Flask(__name__)


############# SQLAlchemy Configuration ###############

basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqllite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)  
Migrate(app,db)
######################################################

################## Create a Model ####################

class Data(db.Model):
    __tablename__='URL_Shortener'
    id=db.Column(db.Integer,primary_key=True)
    orig_url=db.Column(db.String(100))
    short_url = db.Column(db.String(100))
    
    def __init__(self,orig_url,short_url):
        self.orig_url=orig_url
        self.short_url=short_url

        
    
        
@app.before_first_request
def create_tables():
    db.create_all()
    
######################################################

@app.route('/',methods=["GET","POST"])
def home():
    global short_url,orig_url
    if request.method=='POST':
        orig_url=request.form.get('name')
        s_config=pyshorteners.Shortener()
        short_url=s_config.tinyurl.short(orig_url)
        val=Data(orig_url,short_url)
        db.session.add(val)
        db.session.commit()
        
    return render_template('index.html',short_url=short_url)

@app.route('/history')
def history():
    alllinks=Data.query.all()
    return render_template('history.html',alllinks=alllinks)


######################################################
if __name__=="__main__":
    app.run(debug=True)
    