from datetime import datetime
# car  il y aune partie de datetime dans otre BD
from flaskblog import db, login_manager,app
# car nous alons mettre ces infos dans ntre de donnnes  donc importede notre package flaksblog
# we import app for our secret key needed for rrest 
#nous importons notre app pour notre secretkey
from flask_login import UserMixin
# usermixin realoding user by id

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# we should import it for reset password
#its reset token process pour le mot de passe 





@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)


#reset token pour avoir le link du mail a renitialiser 
#get_rest_token methode acreer et nombre de secondes que ce lien vas expirer 


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)   #ici nous creeons un object pour renitialiser le mot de pase
        return s.dumps({'user_id': self.id}).decode('utf-8')
#return s dumps nous creens le token 

#methode qui verifie le token est staticmethod verify 

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']     # nous prenons le user id
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"





class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"





class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    body = db.Column(db.String(100), nullable=False)

    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Post('{self.body}', '{self.date_posted}')"

        










