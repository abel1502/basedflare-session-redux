from __future__ import annotations
import typing
import functools
from urllib.parse import urlparse

import niquests
from .utils import solve_argon2, solve_sha256
from .exceptions import ChallengeRequestError


class BasedSession(niquests.Session):
    """A session that can solve BasedFlare challenges automatically."""
    
    __eager: bool
    __solvers: typing.Dict[str, typing.Callable[[str, str, int, int, int], int]]

    @functools.wraps(niquests.Session.__init__)
    def __init__(self, *args, eager: bool = False, **kwargs):
        super().__init__(*args, **kwargs)
        self.__eager = eager
        self.__solvers = {
            "argon2": solve_argon2,
            # sha256 does not require the same parameters as argon2 (time_cost, memory_cost)
            # but BasedFlare sends them anyway, so we have to wrap it to keep the same parser
            "sha256": lambda salt, secret, difficulty, *args: solve_sha256(
                salt, secret, difficulty
            ),
        }

    @functools.wraps(niquests.Session.request)
    def request(self, method: str, url: str, *args, **kwargs) -> niquests.Response:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        path = parsed_url.path
        
        # Solve the challenge eagerly if the session does not have the necessary cookie
        if (
            self.__eager and
            not self.cookies.get("_basedflare_pow", domain=f".{domain}") and
            path != "/.basedflare/bot-check"
        ):
            self.__solve_challenge(domain)

        res = super().request(method, url, *args, **kwargs)

        # Fallback to solving the challenge if the response is a redirect, e.g. the cookie is invalid
        if res.url and res.url != url:
            parsed_res_url = urlparse(res.url)
            
            if parsed_res_url.path == "/.basedflare/bot-check" and parsed_res_url.query.startswith("/"):
                self.__solve_challenge(domain)
                res = super().request(method, url, *args, **kwargs)

        return res

    def __solve_challenge(self, domain: str):
        challenge = self.__get_challenge(domain)
        if challenge is None:
            return
        if challenge["ca"]:
            raise NotImplementedError("CAPTCHA challenges are not supported")

        algorithm, params = challenge["pow"].split("#", 1)
        if algorithm not in self.__solvers:
            raise NotImplementedError(f"{algorithm} is not a supported algorithm")

        solution = self.__solvers[algorithm](
            *challenge["ch"].split("#")[0:2], *map(int, params.split("#"))
        )
        self.__post_challenge(domain, f"{challenge['ch']}#{solution}")

    def __get_challenge(self, domain: str) -> typing.Optional[typing.Dict[str, typing.Any]]:
        res = self.get(
            f"https://{domain}/.basedflare/bot-check",
            headers={"Accept": "application/json"},
        )
        if res.status_code == niquests.codes.not_found:
            return None
        if res.status_code != niquests.codes.forbidden:
            raise ChallengeRequestError(
                f"Unexpected status code {res.status_code} when fetching the challenge"
            )

        return res.json()

    def __post_challenge(self, domain: str, pow_response: str):
        res = self.post(
            f"https://{domain}/.basedflare/bot-check",
            data={"pow_response": pow_response},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        if res.status_code != niquests.codes.found:
            raise ChallengeRequestError(
                f"Unexpected status code {res.status_code} when posting the challenge solution"
            )
        if "_basedflare_pow" not in res.headers.get("Set-Cookie", ""):
            raise ChallengeRequestError(
                "The server did not send the bypass cookie after solving the challenge"
            )

