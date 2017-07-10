import requests

class WebIO:
    def lmgtfy(self, message):
        params = {'q': message}
        resp = requests.get('https://lmgtfy.com/', params=params)
        return str(resp.url)
        