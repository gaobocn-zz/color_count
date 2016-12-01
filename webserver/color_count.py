from flask import Flask, request, abort, g
import os
import requests
from StringIO import StringIO
from wand.image import Image
from urlparse import urlparse
from tempfile import NamedTemporaryFile
from subprocess import check_output, call
import commands
# import datetime
import logging
import sqlite3
import urllib2
import re


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

def get_valid_filename(s):
    """
    FROM django/utils/text.py
    Returns the given string converted to a string that can be used for a clean
    filename. Specifically, leading and trailing spaces are removed; other
    spaces are converted to underscores; and anything that is not a unicode
    alphanumeric, dash, underscore, or dot, is removed.
    >>> get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'
    """
    s = s.strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

tempfilepath = "mytempfile"

def new_image(img_url):
    # print ('new_image: ' + img_url)
    try:
        req = urllib2.urlopen(img_url)
    except:
        return "Couldn't download image!"
    img = req.read()
    img_name = get_valid_filename(re.search(url_r, img_url).group(0))
    img_ext = re.search(ext_r, img_name).group(0)
    if not img_name:
        return "Invalid File"
    # while(os.path.isfile("images/" + img_name)):
    #     img_name = str(randint(0,1000000)) + img_ext
    #     print(img_name)
    # rewrite one file every time
    with open(tempfilepath, 'w') as img_file:
        img_file.write(img)
    num_colors = check_output(["/usr/bin/identify", "-format", "%k", tempfilepath])
    # call(["/bin/rm", "images/" + img_name])
    if not num_colors.isdigit():
        return "Color check failed"
    add_query = "INSERT INTO img_cache (\'url\',\'color_count\') \
        VALUES (\'" + img_url + "\',\'" + num_colors + "\')"
    add_exec = get_db().execute(add_query, ())
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
    print(url)
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
