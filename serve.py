# serve.py
import falcon
from sentistrength_id import sentistrength

config = dict()
config["negation"] = True
config["booster"] = True
config["ungkapan"] = True
config["consecutive"] = True
config["repeated"] = True
config["emoticon"] = True
config["question"] = True
config["exclamation"] = True
config["punctuation"] = True
senti = sentistrength(config)


def max_body(limit):
    def hook(req, resp, resource, params):
        length = req.content_length
        if length is not None and length > limit:
            msg = ('The size of the request is too large. The body must not '
                   'exceed ' + str(limit) + ' bytes in length.')
            raise falcon.HTTPRequestEntityTooLarge(
                'Request body is too large', msg)
    return hook


class SentimentResource:

    @falcon.before(max_body(64 * 2048))
    def on_post(self, req, resp):
        """Handles API requests"""
        try:
            text = req.params['text']
            if type(text) == list:
                text = ','.join(text)
        except KeyError:
            raise falcon.HTTPBadRequest(
                'Missing thing',
                'A thing must be submitted in the request body.')
        data = senti.main(text)
        resp.media = data

api = falcon.API()
api.req_options.auto_parse_form_urlencoded = True
api.add_route('/', SentimentResource())
