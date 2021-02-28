from flask import Flask, render_template, request, flash, redirect # to cconnect template with url
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, UserMixin, logout_user
from datetime import datetime
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SECRET_KEY'] = 'super secret key'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    fname = db.Column(db.String(120), nullable=False)
    lname = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120),nullable=False)
    def __repr__(self):
        return '<User %r>' % self.username

class Blog(db.Model):
    blog_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content=db.Column(db.Text(), nullable=False)
    pub_date=db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return '<Blog %r>' % self.title

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/main') #blank URL
def main():
    return render_template("main.html")


@app.route('/') #blank URL
def index():
    data = Blog.query.all()
    return render_template("index.html", data=data)

@app.route('/login', methods=['GET','POST']) #error-__init__() got an unexpected keyword argument 'method'(s is missing)
def login():
    if request.method=='POST':
        uname= request.form.get('uname')
        password= request.form.get('password')
        user = User.query.filter_by(username=uname).first()
        if user and password ==user.password:
            login_user(user)
            return redirect('/')
        else:
            flash('Invalid Credentials', 'danger')
            return redirect('/login')


    return render_template("login.html")

@app.route('/register', methods=['GET','POST']) 
def register():
    if request.method=='POST':
        email= request.form.get('email')
        password= request.form.get('password')
        fname= request.form.get('fname')
        lname= request.form.get('lname')
        uname= request.form.get('uname')
        user = User.query.filter_by(username=uname).first()
        
        if user and password ==user.password:
            flash('Already Exist', 'success')
            return redirect('/login')
        else:
            user = User(username=uname, email=email, fname=fname, lname=lname, password=password)
            print("Code is in else condition")
            db.session.add(user)
            db.session.commit()
            flash('user has been registered successfully', 'success')
            return redirect('/login')


    return render_template("register.html") 
     #error- "GET /register HTTP/1.1" 200 -
    #resolved- try different browser

@app.route('/logout') #blank URL
def logout():
    logout_user()
    return redirect('/')

@app.route('/blogpost', methods=['GET','POST']) #blank URL
def blogpost():
    if request.method=='POST':
        title = request.form.get('title')
        content= request.form.get('content')
        blog = Blog(title=title,content=content)
        db.session.add(blog)
        db.session.commit()
        flash("Your post has been submitted successfully", 'success')
        return redirect ('/')

    return render_template('blog.html')
@app.route("/blog_detail/<int:id>", methods=['GET','POST']) #blank URL
def blogdetail(id):
    blog = Blog.query.get(id)
    return render_template('blog_detail.html', blog=blog)

@app.route("/delete/<int:id>", methods=['GET','POST']) #blank URL
def delete_post(id):
    blog = Blog.query.get(id)
    db.session.delete(blog)
    db.session.commit()
    flash("Post has been deleted, Success")
    return redirect('/')

@app.route("/edit/<int:id>", methods=['GET','POST']) #blank URL
def edit_post(id):
    blog = Blog.query.get(id)
    if request.method=='POST':
        blog.title=request.form.get('title')
        blog.content=request.form.get('content')
        db.session.commit()
        flash("Post has been updated, Success")
        return redirect('/')
    return render_template('edit.html',blog=blog)


   

if __name__ == "__main__":
    app.run(debug=True)