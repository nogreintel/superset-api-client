"""A Superset REST Api Client."""
from functools import partial

from requests import Session


class SupersetClient:
    """A Superset Client."""

    def __init__(
        self,
        host,
        username,
        password,
        port=5000,
    ):
        self.host = host
        self.base_url = self._join_urls(host, "/api/v1")
        self.username = username
        self._password = password
        self.session = Session()

        # Try authentication
        response = self.session.post(self.login_endpoint, json={
            "username": self.username,
            "password": self._password,
            "provider": "db",
            "refresh": "true"
        })
        response.raise_for_status()
        tokens = response.json()
        self._token = tokens.get("access_token")
        self.refresh_token = tokens.get("refresh_token")

        # Bind method
        self.get = partial(
            self.session.get,
            headers=self._headers
        )
        self.post = partial(
            self.session.post,
            headers=self._headers
        )
        self.put = partial(
            self.session.put,
            headers=self._headers
        )
        self.delete = partial(
            self.session.delete,
            headers=self._headers
        )

    def _join_urls(self, *args) -> str:
        """Join multiple urls together.

        Returns:
            str: joined urls
        """
        urls = []
        for u in args:
            if u[0] == "/":
                u = u[1:]
            if u[-1] == "/":
                u = u[:-1]
            urls.append(u)
        return "/".join(urls)

    @property
    def password(self):
        return "*" * len(self._password)

    @property
    def login_endpoint(self):
        return self._join_urls(self.base_url, "/security/login")

    @property
    def refresh_endpoint(self):
        return self._join_urls(self.base_url, "/security/refresh")

    @property
    def token(self):
        return self._token

    @property
    def _headers(self):
        return {
            "authorization": f"Bearer {self.token}"
        }