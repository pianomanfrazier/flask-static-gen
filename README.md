# Flask Static Gen

A simple static site generator using [Flask](http://flask.pocoo.org), Frozen_flask, and markdown.

To install all dependencies create a virtual environment and install all the dependencies with pip.

```bash
virtualenv -p python3 venv
source ./venv/bin/activate
pip install -r requirements.txt
```

To run a live preview of the site run `./gen.py run`. And to build the site run `./gen.py build`.
