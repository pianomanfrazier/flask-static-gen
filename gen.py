#!./venv/bin/python

import sys
from flask import Flask, render_template
import markdown
from flask_frozen import Freezer
import yaml

app = Flask(__name__)
freezer = Freezer(app)

app.jinja_env.filters['markdown'] = lambda text: markdown.markdown(text, extensions=['markdown.extensions.tables'])

def parse(markdown):
  """
  Parse the yaml meta data from the markdown file

  @param markdown --- a markdown file with yaml meta data in its head
  @return [meta, markdown] --- meta is a dict of key value pairs, markdown is a string of body content
  """
  meta = ""
  body = ""
  cnt = 0
  with open(markdown) as fout:
    for line in fout:
      if "-" in set(line) or "." in set(line):
        cnt+=1
      if cnt < 2:
        meta += line
      elif cnt == 2:
        cnt+=1 #consume the closing yaml marker
      else:
        body += line
  meta = yaml.load(meta)
  return [meta, body]

@app.route('/')
@app.route('/index/')
def index():
  return render_template('index.html', title="My Static Generator")

@app.route('/posts/<string:title>/')
@app.route('/posts/')
def posts(title=None):
  if title != None:
    md_text=""
    _file = './posts/' + title + ".md"
    meta, md_text = parse(_file)
    return render_template('posts.html', meta=meta, md_text=md_text)
  else:
    return render_template('posts.html', meta=None, md_text=None)

@freezer.register_generator
def posts_generator():
  yield '/posts/my-first-post/'
  yield '/'

if __name__ == "__main__":
  if len(sys.argv) < 2:
    sys.exit("usage: ./gen.py <run|build>")
  if sys.argv[1] == 'run':
    app.run(debug=True)
  elif sys.argv[1] == 'build':
    freezer.freeze()
