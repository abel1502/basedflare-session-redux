# basedflare-session-niquests

[![PyPI version](https://img.shields.io/pypi/v/basedflare-session-niquests.svg)](https://pypi.org/project/basedflare-session-niquests/)
[![Python versions](https://img.shields.io/pypi/pyversions/basedflare-session-niquests.svg)](https://pypi.org/project/basedflare-session-niquests/)
[![License](https://img.shields.io/pypi/l/basedflare-session-niquests.svg)](LICENSE)

This is a port of [basedflare-session](https://github.com/loynet/basedflare-session/) to [niquests](https://github.com/jawah/niquests). Big thanks to @loynet and @jawah for their work! I intend to maintain this fork up to date with the original package, as well as introduce improvements where applicable.

## Original description

A package that extends [Python's niquests session](https://docs.python-requests.org/en/latest/_modules/requests/sessions/) to solve some [BasedFlare](https://basedflare.com/) Proof of Work (PoW) challenges automatically.
It also includes utility functions to solve the challenges manually.

Please note that **this package is a work in progress** and may not function in all cases.
Currently, it supports the `argon2` and `sha256` PoW challenges.
Any other challenge, such as a CAPTCHA, will raise an exception.

## Usage

Suppose `example.com` is a website that requires you to solve a challenge before you can access it. Below is a simple
example of how to use the package:

```python
from basedflare_session import BasedSession

# Create a new session
session = BasedSession()

# Use the session to send a GET request
response = session.get('https://example.com')

# Print the response
print(response.text)
```