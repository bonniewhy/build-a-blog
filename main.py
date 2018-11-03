from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:1234@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    content = db.Column(db.Text())

    def __init__(self, title, content):
        self.title = title
        self.content = content

@app.route('/', methods=['POST', 'GET'])
def index():
    blog = Blog.query.all()

    return render_template('index.html', title = "Build a Blog", blog = blog)

@app.route('/blog', methods=['POST', 'GET'])
def indv_post():

    return render_template('blog.html')

@app.route('/newpost', methods=['POST', 'GET'])
def create_new_post():
    blog_title = ""
    blog_content = ""
    title_error = ""
    content_error = ""

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_content = request.form['blog_content']

        if blog_title == "":
            title_error = "Please enter a title!"

        if blog_content == "":
            content_error = "Please enter a post!"

        else:
            new_post = Blog(blog_title, blog_content)
            db.session.add(new_post)
            db.session.commit()
            return redirect('/')

    return render_template('newpost.html', title = "Add a new post", blog_title = blog_title, blog_content = blog_content, title_error = title_error, content_error = content_error)

if __name__ == "__main__":
    app.run()