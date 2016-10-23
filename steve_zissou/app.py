"""Main app module for steve_zissou service"""
# pylint: disable=import-error
import os
import json

from flask import Flask, render_template, Response, request, url_for

from utils import get_logger

from eleanor_client.endpoints import twitter as eleanor_twitter


static_url_path = '/static'
if 'RUN_ENV' in os.environ:
    if os.environ['RUN_ENV'] == 'production':
        web_app = Flask(
            __name__,
            root_path='/opt/steve-zissou/',
            static_folder=None
        )
else:
    web_app = Flask(
        __name__,
        static_url_path=static_url_path
    )


@web_app.route('/')
def app_root():
    """Base url for steve_zissou service"""
    logger = get_logger(__name__)
    logger.debug('Request made against root url')
    path_to_js = url_for('static', filename='main.min.js')
    return render_template('base.html', path_to_js=path_to_js)


@web_app.route('/eleanor/twitter-users', strict_slashes=False)
def get_twitter_users():
    """Pull twitter users from eleanor"""
    tracked_users = eleanor_twitter.get_tracked_twitter_users()
    return json.dumps(tracked_users)


@web_app.route('/eleanor/tweets-on-date', methods=['POST'],
               strict_slashes=False)
def tweet_search_on_date():
    """Run a search against eleanor with the provided parameters"""
    for k, v in request.headers.items():
        if k.lower() == 'content-type':
            if v.lower() == 'application/json':
                req_username = request.json['twitter_username']
                req_date = request.json['search_date']
                req_search_term = request.json['search_term']
                valid_req_data = req_username and req_date and req_search_term
                if valid_req_data:
                    search_data = eleanor_twitter.tweet_search_on_date(
                        req_username,
                        req_date,
                        req_search_term
                    )
                if search_data is None or not valid_req_data:
                    resp = Response(
                        status=204
                    )
                    return resp
                else:
                    resp = Response(
                        status=200,
                        mimetype='application/json',
                        response=json.dumps(search_data)
                    )
                    return resp
    resp = Response(
        status=204,
        mimetype='application/json',

    )
    return resp


def test():
    """Run the app in dev mode"""
    # the host is set to 0.0.0.0 because currently development happens between
    # two machines with one playing development host, were this to be a project
    # developed outside of a single person on a home network this would be
    # changed to 127.0.0.1
    web_app.run(host='0.0.0.0', port=5050)

if __name__ == '__main__':
    test()
