from flask import  render_template, url_for, flash, redirect,request
from gtaches.models import User,Category,Taches
from gtaches.forms import LoginForm,RegistrationForm,UpdateProfileForm
from gtaches import app,db,bcrypt
from flask_login import login_user,login_required,logout_user,current_user
import secrets
import os 
#from PIL import Image

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/user_pics", picture_name)
    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_name

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',title="home")

@app.route("/about")
def about():
    return render_template('about.html', title="About")

@app.route("/register", methods=["GET", "POST"])
def register():
    #if user login
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    #validate 
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            fname=form.fname.data,
            lname=form.lname.data,
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
        )
        db.session.add(user)
        db.session.commit()
        flash(f"Account created successfully for {form.username.data}", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            flash("You have been logged in!", "success")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check credentials", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    profile_form = UpdateProfileForm()
    if profile_form.validate_on_submit():
        if profile_form.picture.data:
            picture_file = save_picture(profile_form.picture.data)
            current_user.image_file = picture_file
        current_user.username = profile_form.username.data
        current_user.email = profile_form.email.data
        current_user.bio = profile_form.bio.data
        db.session.commit()
        flash("Your profile has been updated", "success")
        return redirect(url_for("dashboard"))
    elif request.method == "GET":
        profile_form.username.data = current_user.username
        profile_form.email.data = current_user.email
        profile_form.bio.data = current_user.bio
    image_file = url_for("static", filename=f"user_pics/{current_user.image_file}")
    return render_template(
        "dashboard.html",
        title="Dashboard",
        profile_form=profile_form,
        image_file=image_file,
    )