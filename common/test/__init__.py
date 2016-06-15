import unittest
import json
import yaml
import importlib
import http.client

from os import path
from flask.json import dumps
from flask.testing import FlaskClient
from flask.wrappers import Response
from contextlib import wraps


def load_fixtures(app, db, fixtures):
    """
    Load one or more fixtures into the database.

    The fixture paths should be relative to the Flask app. The best way to describe it is as being
    similar in structure to the path used to import a regular Python module in your application: it should
    have the same root and the same elements, but use slashes instead of periods as delimiters.

     The fixtures YAML should look like this:

        - model: fully.qualified.ModelName
          records:
            - id: 1
              attribute1: value1
              attribute2: value2
              attribute3: value3
            - id: 2
              attribute1: value1
              attribute2: value2
              attribute3: value3
            ...

    (Some bits of the implementation copied from https://github.com/croach/Flask-Fixtures which sadly does not
    support Python 3.)
    """

    for fixture in fixtures:
        fixture_path = path.join(path.dirname(app.root_path), fixture)
        app.logger.info('Loading fixture: %s', fixture_path)
        with open(fixture_path) as f:
            fixtures = yaml.load(f.read())
            for fixture in fixtures:
                module_name, class_name = fixture['model'].rsplit('.', 1)
                module = importlib.import_module(module_name)
                model = getattr(module, class_name)
                for fields in fixture['records']:
                    db.session.add(model(**fields))
        db.session.commit()


def assert_response_ok(http_method):
    """
    Wrap the given HTTP method and assert it returns 200 OK status code.
    """

    @wraps(http_method)
    def wrapper(*args, **kwargs):
        response = http_method(*args, **kwargs)
        assert response.status_code == http.client.OK
        return response
    return wrapper


class TestingClient(FlaskClient):
    """
    Customize the test client.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_ok = assert_response_ok(self.get)
        self.patch_ok = assert_response_ok(self.patch)
        self.post_ok = assert_response_ok(self.post)
        self.head_ok = assert_response_ok(self.head)
        self.put_ok = assert_response_ok(self.put)
        self.delete_ok = assert_response_ok(self.delete)
        self.trace_ok = assert_response_ok(self.trace)
        self.options_ok = assert_response_ok(self.options)

    def post_json(self, url, payload):
        """
        Send a POST request with JSON content in the body.
        """

        return self.post(url,
                         content_type='application/json',
                         data=dumps(payload, indent=2))

    def post_json_ok(self, url, payload):
        """
        Send a POST request with JSON content in the body and verify that HTTP 200 comes back.
        """

        return self.post_ok(url,
                            content_type='application/json',
                            data=dumps(payload, indent=2))

    def put_json(self, url, payload):
        """
        Send a PUT request with JSON content in the body.
        """

        return self.put(url,
                        content_type='application/json',
                        data=dumps(payload, indent=2))

    def put_json_ok(self, url, payload):
        """
        Send a PUT request with JSON content in the body and verify that HTTP 200 comes back.
        """

        return self.put_ok(url,
                           content_type='application/json',
                           data=dumps(payload, indent=2))


class TestingResponse(Response):
    """
    Customize the standard response class to ease testing.
    """

    @property
    def json(self):
        return json.loads(self.data.decode('utf-8'))


class BaseFlaskTestCase(unittest.TestCase):
    """
    Base class for Flask and SQLAlchemy tests. This class resets the test database and populates it with any
    fixture data before every test. It also manages the Flask request context and the associated SQLAlchemy session
    to mimic the handling of an actual request.

    Things should work without a request context too. If you don't want one, override :meth:`.make_request_context()`
    to return `None`.

    Fixtures are specified using a class-level `fixtures` attribute:

        fixtures = ['path/to/fixtures.yaml']

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = None
        self.db = None

    def setUp(self):
        """
        Configure the Flask app for testing, setup a Flask request context, reset the test database, and
        load fixture data. Fixtures are specified using a class-level `fixtures` attribute:

            fixtures = ['path/to/fixtures.yaml']

        """

        assert hasattr(self, 'app'), 'Please provide a reference to the Flask app'
        assert hasattr(self, 'db'), 'Please provide a reference to the Flask SQLAlchemy object'

        # Configure app for testing
        self.app.testing = True
        self.app.response_class = TestingResponse
        self.app.test_client_class = TestingClient
        self.client = self.app.test_client()

        self.context = self.make_request_context()
        if self.context is not None:
            self.context.push()

        try:
            self.create_schema()
            load_fixtures(self.app, self.db, getattr(self, 'fixtures', []))
        except Exception:
            # Don't leave the database in a bad state if fixture loading or schema creation fail. This avoids
            # cascading errors that cause all subsequent tests to fail.
            self.db.session.rollback()
            raise

    def make_request_context(self):
        """
        Override to customize Flask request context. Return None if you don't want one.
        """

        return self.app.test_request_context()

    def create_schema(self):
        """
        Wipe and re-create the test database schema.
        """

        self.assert_is_test_env()
        self.db.drop_all()
        self.db.create_all()

    def assert_is_test_env(self):
        """
        Sanity check before blowing everything away
        """

        db_url = self.app.config['SQLALCHEMY_DATABASE_URI']
        msg = '{!r} does not appear to be a test database'
        assert 'test' in db_url, msg.format(db_url)

    def tearDown(self):
        """
        Flush any pending data to the database so that any bad SQL forces an error.

        Shutdown the SQLAlchemy session.

        Pop the (optional) Flask request context. This emulates the normal flow in a Flask app where the context is
        popped when the app finishes handling the request.
        """

        # Flushing leftover SQL to the database at the end of every test catches bugs that manifest themselves only
        # at the database level, such as constraint violations or model attributes with values that cannot be
        # represented in SQL but are perfectly fine in Python. SQLAlchemy has its own heuristics governing when to
        # flush, such as before issuing any queries, but there is no guarantee it happens after every test so we do
        # it here. Committing the session also forces a flush but is a heavier operation.
        try:
            self.db.session.flush()
        finally:
            self.db.session.rollback()

            # Tearing down all sessions seems drastic, but simply rolling back the current transaction does not
            # terminate all database connections, which can cause the tests to hang.
            self.db.session.close_all()

            # This de-scopes the SQLAlchemy session. Flask-SQLAlchemy does this when the Flask request context is
            # popped, but it's convenient to treat them as orthogonal concerns so that this test does not require
            # a request context.
            self.db.session.remove()
            if self.context is not None:
                self.context.pop()

    def assertEntitiesContain(self, actual_entities, expected_entities):
        """
        Check that the given list of actual entities matches those expected. Entities are matched on the
        basis of their 'id'. The comparison of actual to expected is not a straight up equality check. Rather,
        this method verifies that every actual entity is a superset of the corresponding expected entity. In
        other words, all key/value pairs in expected must be in actual, but actual may also contain additional
        keys that are ignored.
        """

        self.assertEqual(len(actual_entities), len(expected_entities), 'Entity lengths don\'t match')

        actual_entities_by_id = {x['id']: x for x in actual_entities}
        for expected in expected_entities:
            id = expected['id']
            actual = actual_entities_by_id.get(id)
            self.assertIsNotNone(actual, 'No actual entity for id {id}'.format(id=id))
            if not set(actual.items()).issuperset(set(expected.items())):
                self.fail('Actual does not have everything expected: {actual}, {expected}'.format(actual=actual,
                                                                                                  expected=expected))

    def canonicalRepr(self, payload):
        """
        Canonicalize a JSON payload intended to be consumed by Ember Data's Rest or JSONAPI adaptors by sorting
        top-level lists. This enables comparison of responses with == and leverages pytest's magic introspection.
        """

        return {key: sorted(value, key=lambda x: (x['id'], x.get('type'))) if isinstance(value, list) else value
                for key, value in payload.items()}
