import pytest
from flask import url_for, g


def assert_status_with_message(status_code=200, response=None, message=None):
    """
    Check to see if a message is contained within a response.

    :param status_code: Status code that defaults to 200
    :type status_code: int
    :param response: Flask response
    :type response: str
    :param message: String to check for
    :type message: str
    :return: None
    """
    assert response.status_code == status_code
    assert message in str(response.data)


class ViewTestMixin(object):
    """
    Automatically load in a session and client, this is common for a lot of
    tests that work with views.
    """

    @pytest.fixture(autouse=True)
    def set_common_fixtures(self, session, client):
        self.session = session
        self.client = client
        g.user = 1
        g.customer_id = 0

    def set_globals(self, user_id=1, customer_id=0):
        g.user = user_id
        g.customer_id = customer_id

    def login(self, username="admin", password="IsThisAGoodPassword1!"):
        """
        Login a specific user.

        :return: Flask response
        """
        user_dict = {"admin": "P@ssw0rdP@ssw0rd1!", "foo": "P@ssw0rdP@ssw0rd1!"}
        return login(self.client, username, user_dict.get(username, password))

    def logout(self):
        """
        Logout a specific user.

        :return: Flask response
        """
        return logout(self.client)


def login(client, username="", password=""):
    """
    Log a specific user in.

    :param client: Flask client
    :param username: The username
    :type username: str
    :param password: The password
    :type password: str
    :return: Flask response
    """
    user = dict(username=username, password=password)

    response = client.post(url_for("core.login"), data=user, follow_redirects=True)

    return response


def logout(client):
    """
    Log a specific user out.

    :param client: Flask client
    :return: Flask response
    """
    return client.get(url_for("core.logout"), follow_redirects=True)
