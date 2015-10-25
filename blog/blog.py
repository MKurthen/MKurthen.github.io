import sys
from flask import Flask, render_template
from flask_flatpages import FlatPages, pygments_style_defs
from flask_frozen import Freezer
from IPython.core.debugger import Tracer

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'content'
POST_DIR = 'posts'
#FREEZER_DESTINATION = '..'
FREEZER_DESTINATION_IGNORE = ['blog']

app = Flask(__name__)
freezer = Freezer(app)
flatpages = FlatPages(app)
app.config.from_object(__name__)

@app.route("/posts/")
def posts():
    posts = [p for p in flatpages if p.path.startswith(POST_DIR)]
    with open('log', 'a') as f:
        f.write(str(posts) + '\n' )
    posts.sort(key=lambda item:item['date'], reverse=False)
    return render_template('posts.html', posts=posts)

@app.route('/posts/<name>/')
def post(name):
    path = '{}/{}'.format(POST_DIR, name)
    #Tracer()()
    #path = path.strip('.md')
    freezer = Freezer(app)
    with open('log', 'a') as f:
        f.write(str(path) + '\n' )
    #post = flatpages.get(path)
    post = flatpages.get_or_404(path)
    with open('log', 'a') as f:
        f.write(str(post) + '\n' )
    return render_template('post.html', post=post)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(host='0.0.0.0', debug=True)
