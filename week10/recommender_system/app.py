"""
A web server that provides a movie recommender web page

uses Flask:
    pip install flask

run it with:
    python app.py
"""

from flask import Flask, render_template
from flask.json import jsonify
from recommender_program import get_recommendation
#    ^^ .py file        ^^ function or variable inside recommender.py

# set up flask with a name for the web app
app = Flask('movie_recommender')


# create a page and connect it to Flask
@app.route('/')  # this is a "decorator", it makes something special happen behind the scenes
def main_page():
    movie = get_recommendation()
    image = 'ship.jpg'
    print("MOVIE RECOMMENDATION:", movie)
    return render_template('recommendation.html', 
                           movie_name=movie,
                           image_name=image)
    # in templates/
    
@app.route('/recommender_api')
def api():
    movie = get_recommendation()
    result = {'movie': movie, 'score': 1.23}
    return jsonify(result)

@app.route('/hello')  # connects the URL 127.0.0.1:5000/hello to this function
def hello_xyz():
    return '''<h1>hello world</h1>
    <a href="/">get a movie recommendation</a>
    '''



# starts the server
# in production: host is 0.0.0.0 AND SWITCH DEBUG OFF!
app.run(host='127.0.0.1', port=5000, debug=True)