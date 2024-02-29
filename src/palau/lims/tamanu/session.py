# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta
import json
import requests
import six
from palau.lims import logger

# endpoint-specific slugs
from palau.lims.tamanu.resource import BaseResource

SLUGS = (
    ("login", "api"),
)

# default slug
DEFAULT_SLUG = "api/integration/fhir/mat"

# basic headers
HEADERS = (
    ("X-Version", "1.0.0"),
    ("X-Tamanu-Client", "mSupply"),
    ("Content-Type", "application/json"),
)


class TamanuSession(object):

    token = "unk"

    def __init__(self, host):
        self.host = host

    def login(self, email, password):
        auth = dict(email=email, password=password)
        resp = self.post("login", payload=auth)
        self.token = resp.json().get("token")
        if self.token:
            return True
        return False

    def get_slug(self, endpoint):
        slug = dict(SLUGS).get(endpoint)
        if slug:
            return slug
        return DEFAULT_SLUG

    def get_url(self, endpoint):
        """Returns the url of the remote instance and endpoint
        """
        if self.host not in endpoint:
            slug = self.get_slug(endpoint)
            parts = filter(None, [self.host, slug, endpoint])
            endpoint = "/".join(parts)
        return endpoint

    def jsonify(self, data):
        output = {}
        for key, value in data.items():
            if not isinstance(value, six.string_types):
                value = json.dumps(value)
            output[key] = value
        return output

    def post(self, endpoint, payload, timeout=5):
        url = self.get_url(endpoint)
        payload = self.jsonify(payload)

        # Send the POST request
        logger.info("[POST] {}".format(url))
        logger.info("[POST PAYLOAD] {}".format(repr(payload)))
        resp = requests.post(url, json=payload, timeout=timeout)

        # Return the response
        return resp

    def get(self, endpoint, params=None, **kwargs):
        url = self.get_url(endpoint)

        # add the default headers
        headers = kwargs.pop("headers", {})
        headers.update(dict(HEADERS))

        # inject the auth token
        headers["Authorization"] = "Bearer {}".format(self.token)
        kwargs["headers"] = headers

        # do the GET request
        logger.info("[GET] {}".format(url))
        logger.info("[GET PARAMS] {}".format(repr(params)))
        resp = requests.get(url, params=params, **kwargs)

        # return the response
        return resp.json() or {}

    def get_resource_by_uid(self, resource_type, uid):
        endpoint = "{}/{}".format(resource_type, uid)
        return self.get(endpoint)

    def get_resources(self, resource_type, **kwargs):
        last_updated = kwargs.pop("_lastUpdated", None)
        if isinstance(last_updated, timedelta):
            last_updated = datetime.now() + last_updated
        if isinstance(last_updated, datetime):
            last_updated = last_updated.strftime("%Y-%m-%dT%H:%M:%SZ")
            kwargs["_lastUpdated"] = "gt{}".format(last_updated)

        # get the raw data in json format
        data = self.get(resource_type, params=kwargs)

        # entries are a list of dicts under 'entry'
        entries = data.get("entry", [])

        # each entry has the resource itself under 'resource'
        resources = map(lambda entry: entry.get("resource"), entries)
        resources = filter(None, resources)
        return [BaseResource(self, resource) for resource in resources]
