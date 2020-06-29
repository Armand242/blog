#toujours importer tout les forms que nous avons creer en form,tableau avec model
# et login tout doit figurer ici

import os
import secrets   # pour ne pas voir le nom de limage creer 
from PIL import Image
#its pillwow package installer avec pip pour que nos images puissent avoir une taille determineee




from flask import render_template, url_for, flash, redirect, request, abort  #pour demander obligatoirement une page apres un login
# url passer une page a une autre , flash afficher un message 
#redirect apres un regu=ister dirrge dans ue autre page 
#equest pour demander a ce que on puisse garder lutilsateur login avec un remenber me 
from flaskblog import app, db, bcrypt, mail
# nous importons db et bcrypt de notre app pour servir lors de la rgstration et login
from flaskblog.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                             PostForm, RequestResetForm, ResetPasswordForm,ContactForm,AddCommentForm)

# ce sont  nos deux formulaires que nous avons importe et updates pour nos modif
#Updtae account form obligatoires de declarer pour faires de changements dans notre pages 
from flaskblog.models import User, Post
# ce sont nous deux tableaux que nous abons importer 
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
#for user session need to be installed on pip
# currnt user after login the nextpage 
# faire sortir exit user logout
#login required pour oblier que cela soit obligatoire pour voir la page account
#turnory condition
#login user pour mettre le user login in 
#logout user cest pour quitter le login 
#loginrequired fais en sorte que cette function puissse etre demander pour interagir avec une fonction
#mail est utilser ici pour le reset password 



#posts = Post.query.all() # pour afficher nos posts sur notre homepg different de paginate
   #paginate  pour avoir des ages qui se suivent 


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)  #
    #npus prennons lespages , le type fera en sorte que la page puisse juste etre intger
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    #paginate for makinf page in order 
    #5ctes le nombre de ost qui sera afficher 
    return render_template('home.html', posts=posts)




@app.route("/about")
def about():
    return render_template('about.html', title='About')





@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
    	#lorsque users submit b=ces infos voic la patie du checking 

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # partie necessaire pour hidden le mot de passe
        #form.password cela veut dire que cest se password que nous voulons hashed pris depuis le formulaire
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        #nous creeons un nouveau user aprres avoir fait un hashed et notre pasword=hashed_password 
        #nous l'avons fait creer car cest une nouvele declaration
        db.session.add(user)
        db.session.commit()
        #une fois que les infos sont rentrer le processus permet envoyer la BD
        flash(" Your application has been created,Login Now ")
        #Grace a flasj ressort ce message  
        return redirect(url_for('login'))
        # redirige dans login apres un register created
    return render_template('register.html', title='Register', form=form)





@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  
        #nous verifions si lemail est egale a lemail dans notre data nous 
        if user and bcrypt.check_password_hash(user.password, form.password.data):    
            #   nous comparons le databse passsword enregistrer avec celui qui a ateait mis dans le 
            #formualire lors du login sils sont egales alors luser peut login  et dirriger dans hompage
            #user.password depuis le databse , form.password.data cequi a etait enregsitrer dans le formulaire
            # si cela existe a lors
            login_user(user, remember=form.remember.data)  # ici cela login un le user grace 
            # grace a la fonction login_user imorter en haut
            next_page = request.args.get('next')    # 
            return redirect(next_page) if next_page else redirect(url_for('home')) #apres login envoi a la hompage
            #si les condtions sont pas garanties alos nous mettons ce message
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)




@app.route("/logout")
def logout():
    logout_user()    
    return redirect(url_for('home'))


# for logout user we shall import logoutuser et logout from the top from.... lougt_user() 

# lorsque luser login alors il a acces a son acount 


# prendre la phto pour upload
def save_picture(form_picture):
    #random_hex pour ne plus afficher le nom de limage pris lors de upload et enregsitrer cela
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)  # return le nom de lextensions et lextensions lui meme

    #to get the filename we want to save the new filename !
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn) #here python knows where i wan to save
#ici sera sauvegarder dans notre static ,oublios pas dimporter os module
#
    output_size = (125, 125)    #imposer une taille de l'image  donc on refait la taille de l'image
    i = Image.open(form_picture)   # ensuite nous creeons limage 
    i.thumbnail(output_size)       
    i.save(picture_path)  # we save our picture to the data 

    return picture_fn



#account pages 

@app.route("/account", methods=['GET', 'POST'])  # get or post request
@login_required
#obligatoire que la personne puisse etre login a a linterieur 
def account():
    #nous devons importer dabord updateaccount pour faire cette demarche fromflasklogin....
    form = UpdateAccountForm()
    if form.validate_on_submit():   # si notre form est valide alors on peut faire des changements
        if form.picture.data:   # pour sil ya une photo upload
        #
            picture_file = save_picture(form.picture.data) # save our picture 
            current_user.image_file = picture_file
        current_user.username = form.username.data   # le nouvel user sera envoyer a nos base de donnnees
        current_user.email = form.email.data
        db.session.commit()  # ici nous confirmons notre changement
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))   # apres cela sa nous remets sur notre page account et on peut revoir sa
    elif request.method == 'GET':  # Get alors on peut populate sur nos data directement dans la Db comme le chn es drct
        #Get nous prenonsles informations depuis notre base de donnnees 
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file) #image of our account 
    #where users will put the imagefile 
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

    # imge_file=image-file we past that image in our database




    # for new post we create a post routes which is bellow  
    # we require user to login
    # we import form that will help us to create post
    #get ,post car cest une reqiete nous prennons et postons


@app.route("/post/new", methods=['GET', 'POST'])
@login_required  # user must be login to create a pot 
def new_post():
    #orm=postform we call the postform formulaire on this part 
    form = PostForm()
    if form.validate_on_submit():   #we are adding on the databse  , 
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        #author=currentuser it will give the name diretly
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')



# ony the right user could update the post 

#to get a post from his id 
#sachant que lid est donner automatiquement pa la base de donnnee donc ic nous utilisons jusste cette functio
#nous prennons notre id depuis la base de donnnee


@app.route("/post/<int:post_id>" , methods=["GET", "POST"])
def post(post_id):
    form=AddCommentForm()
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post,form=form)









@app.route("/post/<int:post_id>/comment", methods=["GET", "POST"])
@login_required
def comment_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = AddCommentForm()
    if request.method == 'POST': # this only gets executed when the form is submitted and not when the page loads
        if form.validate_on_submit():
            comment = Comment(body=form.body.data, article=post.id)
            db.session.add(comment)
            db.session.commit()
            flash("Your comment has been added to the post", "success")
            return redirect(url_for("post", post_id=post.id))
    return render_template("post.html", title="Comment Post", 
form=form, post_id=post_id)





@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:    #if the authoris diffferent than user we get error 
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
        #lorsque cela est fait alors on populate a partir de cette demarche 
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')




@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))





#paginations : lorsque nous avons plusisuers postes et que nous voulons pas tous les voir sur notre pages alors
# pour le faires suivres vers d'autres pages nous faisons de la pagination pour ermettrede nous rediriger 
#vers d'autres pages 




@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)





# pour envoyer lemil 

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)





#renitialiser le mot de passe  a partir du mail 

@app.route("/reset_password", methods=['GET', 'POST'])
#car nous aurons une template resetrequest
def reset_request():
    #lutilsateur doit etre login pour renitialiser le mot de passe  a partir de leur emaail
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        #form=requestform car nous renitialisons avec la methode requestform
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)





#pour renitialser le mot de passe pratiquement le emem masi ici nous avons un token

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):  # nous appelons pour renitilaser mot de passe 
#user doit etre login
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)  #nous verifons le token 
    if user is None:
        flash('That is an invalid or expired token', 'warning') #lorsque le nombre de second a dpasser 
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    #si cela a etait valider
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)



@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.errorhandler(403)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('403.html'), 403


@app.errorhandler(500)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('500.html'), 500


@app.route("/donations")
def donations():
    return render_template('donations.html', title='donations')




@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()
 
  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
      msg = Message(form.subject.data, sender='contact@example.com', recipients=['your_email@example.com'])
      msg.body = """
      From: %s &lt;%s&gt;
      %s
      """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)
 
      return render_template('contact.html', success=True)
 
  elif request.method == 'GET':
    return render_template('contact.html', form=form)






#@app.route("/post/<int:post_id>/comment", methods=["GET", "POST"])
#@login_required
#def post(post_id):
   # post = Post.query.get_or_404(post_id)
   # form = AddCommentForm()
    #if request.method == 'POST': # this only gets executed when the form is submitted and not when the page loads
       # if form.validate_on_submit():
          #  comment = Comment(body=form.body.data, article=post.id)
          #  db.session.add(comment)
           # db.session.commit()
           # flash("Your comment has been added to the post", "success")
           # return redirect(url_for("post", post_id=post.id))
           # return render_template('post.html', title=post.title, post=post,form=form)









#we shall reset token similar to our request template







