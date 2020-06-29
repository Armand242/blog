from flask_wtf import FlaskForm
#nous importons les formulaires de wtf obliatoire a declarer lorsque nous faisons les formulaires
from flask_wtf.file import FileField, FileAllowed   #pour changer nos pictures  ,Fieldfile le type que ns vlons
# pour image picture et vaidate quel genre de file nous velons
from flask_login import current_user      # pour se rassurer que les modifiations seront faites chez le correct user
#surtout pour les validations lors des nos udpatess
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
#TextAreaField to ask un user to write in the fiel ici pour creer un nouveau un post
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,InputRequired
# nous mettons wtforms.validators et importons datarequired pour faire en sorte que l'utilisateur puisse 
#etre obliger de mettre les data, Length pour la taille , EqualTo pour dire que les valeurs doivent etre egales
#Donc Equalto(doit etre egale a valauer de notre password )
from flaskblog.models import User

# WTf pour utilser le formulaire WTT EST UNE LIBRARY IMPORTANET A TJRS IMPORTER 
#stringfield ce sont les cases pour entre les donnees
#passwordflied la ou nous entre le mot de passe
# submifield pour soummettre un form ou regsitration
#booelanfield pour garder utilsateur remmenber pir se rappler de lui
# datarequired pour obliger de rentrer le data ne pas aisser vide
# email car email estune des forme de wtforms pour verifer que email est valide
# equalto utilse pour verifier le motpasse=cequi est comfirmer 
#sutilse avec risoe pour afficher un message au cas ou utilsateur a inscris un terme deja pris par d'autre 

# we imort user in models to chekc if the user already exist in our app

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

# nous creeons a customs function ci_dessous 
#def validate_nous mettons un field name 
#nous devons importer User (qui est notre DB table )depuis notre database

# ici c'est pour les donnes entres puissee etre unique
# clssse username pour que cela puisse etre a un utilisateur donc validate_username 
# and we should import user from our models because we will use to check if the user already exist in our DB
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()   #nous verifions si luser existe deja dans notre DB
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')



class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

# mettre a jour notre compte 
# nous deons aussi importer udpaccform dans routes
 


 #to update our account informations 
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])    # chnager notre name
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')   # dois mettre upadte


# sassurer que les changements vont bien chez la personne 

#validation  pour verifier quenos informations mis a jour ne sont pas pareil a ceux que nous deja dns notre de base donnee
# pour cela nous devons aussi importer current user car cette function joue le role de current user aussi

    def validate_username(self, username):
        if username.data != current_user.username:      # si le nouvel utilsateur est different alors il peut le prendre 
            user = User.query.filter_by(username=username.data).first() # si cest diff alors le changement a lieu
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')




#for user to create a post we use flaskpostform which we will import into our routes
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])   
    #dont forget to import textareafield in our form.py to create a post 
    submit = SubmitField('Post')





#to rest email pour demander un nouvel email pour modiifer le mot de passe
#nous creeons une class requestform qui fait partie de flaskform 

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])    # demandons a util de mettre son email
    submit = SubmitField('Request Password Reset')  #ici il valide cela  en reqeust passord


    #si nous avons pas daccompte avec son email alors on le lui signifie pr cette methode 
    #noussverifons que email nesxiste pas if user is none donc lemail existe pas 

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


#pour renitialiser le mot de passe nous avons resetpassword dans flaskform 


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')






# pour contacter information page

class ContactForm(FlaskForm):
  name =  StringField("Name", validators=[DataRequired()])

  email =  StringField("Email",validators=[DataRequired(), Email()])

  subject =  StringField("Subject",validators=[DataRequired()])

  message = TextAreaField("Message",validators=[DataRequired()])

  submit = SubmitField("Send")




class AddCommentForm(FlaskForm):
   body = StringField("body", validators=[InputRequired()])

   submit = SubmitField("comment")

    











