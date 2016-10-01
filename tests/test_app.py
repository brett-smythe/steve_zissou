"""Tests for steve_zissou web app"""
# pylint: disable=import-error
import unittest
import json

from functools import wraps

import mock
from flask import Response

import steve_zissou


class SteveZissouAppCases(unittest.TestCase):
    """Tests for the steve_zissou web app"""
    # pylint: disable=too-many-public-methods

    def create_test_context(endpoint, http_method):
        """Decorator for creating contexts for eleanor tests"""
        # pylint: disable=no-self-argument
        def decorator(func):
            # pylint:disable=missing-docstring, unused-variable

            @wraps(func)
            def func_wrapper(self, *args, **kwargs):
                # pylint: disable=missing-docstring, unused-argument
                with steve_zissou.app.web_app.test_request_context(
                    endpoint, http_method
                ):
                    func(self, *args, **kwargs)
            return func_wrapper
        return decorator

    @mock.patch('steve_zissou.app.eleanor_twitter')
    @create_test_context('eleanor/twitter-users', 'GET')
    def test_get_twitter_users(self, mock_eleanor_twitter):
        """Test call to eleanor to get users"""
        mock_eleanor_twitter.get_tracked_twitter_users.return_value = {}
        steve_zissou.app.get_twitter_users()
        self.assertTrue(mock_eleanor_twitter.get_tracked_twitter_users.called)

    @mock.patch('steve_zissou.app.eleanor_twitter')
    @mock.patch('steve_zissou.app.request')
    @create_test_context('eleanor/tweets-on-date', 'POST')
    def test_tweet_search_on_date_200(self, mock_request,
                                      mock_eleanor_twitter):
        """Test searching for tweets on a specific day with success"""
        fake_data = {'faked_count': 15}
        test_response = Response(
            status=200,
            mimetype='application/json',
            response=json.dumps(fake_data)
        )
        mock_request.method = 'POST'
        mock_request.headers = {'content-type': 'application/json'}
        mock_request.json = {
            'twitter_username': 'Bucky',
            'search_date': '01/01/1945',
            'search_term': 'hydra'
        }
        mock_eleanor_twitter.tweet_search_on_date.return_value = fake_data
        return_resp = steve_zissou.app.tweet_search_on_date()
        mock_eleanor_twitter.tweet_search_on_date.assert_called_with(
            mock_request.json['twitter_username'],
            mock_request.json['search_date'],
            mock_request.json['search_term']
        )
        self.assertEqual(return_resp.status, test_response.status)
        self.assertEqual(return_resp.mimetype, test_response.mimetype)
        self.assertEqual(return_resp.response, test_response.response)

    @create_test_context('eleanor/tweets-on-date', 'POST')
    def test_tweet_search_on_date_204(self):
        """Test searching for tweets on a specific day without success"""
        return_resp = steve_zissou.app.tweet_search_on_date()
        self.assertEqual(return_resp.status, '204 NO CONTENT')
