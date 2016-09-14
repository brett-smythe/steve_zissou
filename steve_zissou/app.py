"""Main app module for steve_zissou service"""
# pylint: disable=import-error
import json
from flask import Flask, render_template, Response, request

from utils import get_logger

from eleanor_client.endpoints import twitter as eleanor_twitter


logger = get_logger(__name__)

web_app = Flask(
    __name__,
    template_folder='/opt/steve-zissou/templates/',
    static_folder='/opt/steve-zissou/static/',
    static_url_path='static'
)


@web_app.route('/')
def app_root():
    """Base url for steve_zissou service"""
    logger.debug('Request made against root url')
    return render_template('base.html')


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
                    print req_username
                    print req_date
                    print req_search_term
                    search_data = eleanor_twitter.tweet_search_on_date(
                        req_username,
                        req_date,
                        req_search_term
                    )
                if search_data is None or not valid_req_data:
                    resp = Response(
                        status=204,
                        mimetype='application/json',

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
    """Run the app in test mode"""
    web_app.run(host='0.0.0.0', port=5050)

if __name__ == '__main__':
    test()
