from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint
import json
import os.path
from werkzeug.utils import secure_filename

# url_for: Creates the URL for us based on the function name

bp = Blueprint('urlshort', __name__)


# Jinja template
@bp.route('/')
def home():
    return render_template('home.html', code=session.keys())


# Flask by default has the security to say if you create a route, in this case our route for the home page,
# our route for your URL it only allows GET requests. Now if we want to have something like a POST we can, but we
# have to explicitly specify that.
@bp.route('/your-url', methods=['GET, POST'])
def your_url():
    if request.method == 'POST':
        urls = {}

        # To prevent users from overwriting existing data inside of our urls.json, we
        # need to do a check inside of our code and update the json file depending on that.
        if os.path.exists('urls.json'):  # check if file exists
            with open('urls.json') as urls_file:  # open json file
                urls = json.load(urls_file)

        if request.form['code'] in urls.keys():  # If the url exists in the file redirect the user to the home page.
            flash('Short name already been taken, please enter new short name')
            return redirect(url_for('urlshort.home'))

        # Checking if it's a file or URL
        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url': request.form['htmlFormUrlName']}  # Dictionary to add the urls
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save("C:/Users/INTEL/PycharmProjects/url-shortener/urlshort/static/user_files" + full_name)
            urls[request.form['code']] = {'file': full_name}  # Dictionary to add the files

        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)

            # Saving a cookie
            session[request.form['code']] = True  # here, for our purposes, we really don't need to store a value
            # associated with this code, thus, set this equal to just a Boolean. Can replace it to a timestamp etc
            # if needed.
        # We should use 'form' instead of 'args' to get parameter information from a POST request.
        return render_template('your_url.html', code=request.form['code'])
    else:
        # args is a dictionary for different parameters that could be passed in as get parameters.
        # return render_template('your_url.html', code=request.args['code'])

        # The code below redirects the user from /your-url to the home page
        return redirect(url_for('urlshort.home'))


# <string:code> says, is that look for, after the first slash on the website, any sort of string and put it in a
# variable called code
@bp.route('/<string:code>')  # this is a variable route.
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['urls'])
                else:
                    return redirect(url_for('static', filename='user_files' + urls[code]['file']))
    return abort(404)  # Error handling. The custom template for this is created below


@bp.errorhandler(404)
def page_no_found(error):
    return render_template('page_not_found.html'), 404


# Can create an json api by using jsonify
@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))


if __name__ == '__main__':
    bp.run()
