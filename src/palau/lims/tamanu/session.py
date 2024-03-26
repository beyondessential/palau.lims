# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta
import json
import requests
import six
from palau.lims.tamanu import logger
from palau.lims.tamanu.interfaces import ITamanuResource
from palau.lims.tamanu.resources import TamanuResource
from zope.component import queryAdapter

# endpoint-specific slugs
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
        logger.info("[GET] {} (params={})".format(url, repr(params)))
        resp = requests.get(url, params=params, **kwargs)

        # return the response
        return resp.json() or {}

    def get_resource_by_uid(self, resource_type, uid):
        endpoint = "{}/{}".format(resource_type, uid)
        item = self.get(endpoint)
        return self.to_resource(item)

    def to_resource(self, item):
        """Converts the item to a Tamanu resource of suitable type
        """
        if not item:
            return None

        # items without these keys are not supported
        required = ["resourceType", "id"]
        for key in required:
            if not item.get(key, False):
                logger.error("Cannot get resource: %s is empty" % key)
                return None

        # Look-up the proper type by using named adapters, where the name
        # is the value for 'resourceType' name
        resource_type = item.get("resourceType")
        name = "tamanu.resource.{}".format(resource_type)
        resource = queryAdapter(self, ITamanuResource, name)
        if resource:
            return resource.wrap(item)

        # Fall-back to default
        return TamanuResource(self, data=item)

    def get_resources(self, resource_type, **kwargs):
        last_updated = kwargs.pop("_lastUpdated", None)
        identifier = kwargs.pop("identifier", None)
        if isinstance(last_updated, timedelta):
            last_updated = datetime.now() + last_updated
        if isinstance(last_updated, datetime):
            last_updated = last_updated.strftime("%Y-%m-%dT%H:%M:%SZ")
            kwargs["_lastUpdated"] = "gt{}".format(last_updated)
        if identifier:
            kwargs["identifier"] = identifier
        # get the raw data in json format
        data = self.get(resource_type, params=kwargs)

        # entries are a list of dicts under 'entry'
        entries = data.get("entry", [])

        # each entry has the resource itself under 'resource'
        items = map(lambda entry: entry.get("resource"), entries)

        # return the proper resource types
        resources = map(self.to_resource, items)
        return filter(None, resources)
