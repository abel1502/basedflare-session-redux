# basedflare-session-redux

[![PyPI version](https://img.shields.io/pypi/v/basedflare-session-redux)](https://pypi.org/project/basedflare-session-redux/)
[![Python versions](https://img.shields.io/pypi/pyversions/basedflare-session-redux)](https://pypi.org/project/basedflare-session-redux/)
[![License](https://img.shields.io/pypi/l/basedflare-session-redux)](LICENSE)

A package that extends Python's [niquests](https://niquests.readthedocs.io/en/latest/api.html#request-sessions) or [requests](https://requests.readthedocs.io/en/latest/api.html#request-sessions) session to solve some [BasedFlare](https://basedflare.com/) Proof of Work (PoW) challenges automatically.
It also includes utility functions to solve the challenges manually.

Please note that **this package is a work in progress** and may not function in all cases.
Currently, it supports the `argon2` and `sha256` PoW challenges.
Any other challenge, such as a CAPTCHA, will raise an exception.

_Fork notice:_ This is a port of [basedflare-session](https://github.com/loynet/basedflare-session/) to support both[niquests](https://github.com/jawah/niquests) and [requests](https://github.com/psf/requests). It uses my [anyquests](https://github.com/abel1502/anyquests) package for that. It also introduces some improvements, such as correctly handling sites that do not use BasedFlare. Big thanks to @loynet and @jawah for their work! I intend to maintain this fork up to date with the original package, as well as introduce further improvements where applicable.

_Rename notice:_ This project was briefly knows as `basedflare-session-niquests`. Since release 0.3.0 it is fully renamed to `basedflare-session-redux`. The project under the previous name is now archived on PyPI and will not be updated.

## Usage

Suppose `example.com` is a website that requires you to solve a challenge before you can access it. Below is a simple
example of how to use the package:

```python
from basedflare_session_redux import BasedSession

# Create a new session
session = BasedSession()

# Use the session to send a GET request
response = session.get('https://example.com')

# Print the response
print(response.text)
```
