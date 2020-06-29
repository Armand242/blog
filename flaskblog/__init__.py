import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail



app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)   # initialisation a reproduire aussis sur cmd 
#ensuite nous faisons bycrpt.generate_password_has()  cel apermet anotre password de ne pas etre vu meme pas ceux qui ont acces a notre db
#pour verifier que les passwords se valent nous utilisopns chcek password acr bycrypt nous donnent differents bytes
#bycrypt.check_password_hash(hashed_pw, 'password')
login_manager = LoginManager(app)   # to use login mnager in our app create t in our app
login_manager.login_view = 'login'
# ceal montrer la page de luser et display son account de login
login_manager.login_message_category = 'info'
#after we login ,its redirectus back to the page we want to go vith ce qui en desous 
login_manager.login_view='login'   # obliger un login pour voir account page




app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'webworkarmand@gmail.com'
app.config["MAIL_PASSWORD"] = 'rmqdbnnlwhbzsrlz'

mail = Mail(app)

from flaskblog import routes