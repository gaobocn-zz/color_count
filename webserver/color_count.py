from flask import Flask, request, abort, g
import os
import requests
from StringIO import StringIO
from wand.image import Image
from io import BytesIO
from urlparse import urlparse
from tempfile import NamedTemporaryFile
from subprocess import check_output, call
import commands
# import datetime
import logging
import sqlite3
import urllib
import subprocess


url_r = r'([^\/]+\.[^\/]+$)'
ext_r = r'(\.[^\/]+)$'

def get_db():
    if not hasattr(g, 'sqlite_db'):
        db_name = app.config.get('DATABASE', 'img_cache.db')
        g.sqlite_db = sqlite3.connect(db_name)
    return g.sqlite_db


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

def check_img_cache(img_url):
    look_query = "SELECT color_count FROM img_cache \
        WHERE url=" + "\'" + img_url + "\'";
    look_exec = get_db().execute(look_query, ())
    look_result = look_exec.fetchone()
    look_exec.close()
    if look_result:
        return look_result[0]
    else:
        return -1

temp_file_name = 'timage'

def new_image(url):
    filename = url.split('/')[-1]
    urllib.urlretrieve(url, './%s' % filename)
    num_colors = subprocess.check_output("identify -format %k ./" + filename, shell=True)
    add_query = """INSERT INTO img_cache (url, color_count) VALUES (?,?)"""
    params = (url, num_colors)
    add_exec = get_db().execute(add_query, params)
    get_db().commit()
    add_exec.close()
    return num_colors


app = Flask(__name__)

# handler = logging.FileHandler('flask.log')
# handler.setLevel(logging.INFO)
# app.logger.addHandler(handler)

@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')

@app.route("/")
def home():
    return "To use the API, the URL must be `images.gaobocn.com/api/num_colors?src=https://www.wikipedia.org/portal/wikipedia.org/assets/img/Wikipedia-logo-v2@2x.png`."

@app.route("/api/num_colors")
def num_colors():
    url = request.args.get('src')
    color_n = check_img_cache(url)
    if color_n == -1:
    # app.logger.info("cache: miss")
        color_n = new_image(url)
    else:
        pass
        # app.logger.info("cache: hit" + url)
    return str(color_n)

if __name__ == "__main__":
    app.run() #if run locally ane exposed to public network
