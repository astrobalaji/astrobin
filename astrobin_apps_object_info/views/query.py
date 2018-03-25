# Python
import json
from textwrap import dedent

# Django
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.generic import base

# This app
from astrobin_apps_object_info.object_query import object_query

class QueryView(base.View):
    def post(self, request, *args, **kwargs):
        try:
            postdata = json.loads(request.body)
        except ValueError:
            return HttpResponseBadRequest("Unable to parse JSON POSTDATA", content_type='text/plain')
        try:
            objname = postdata.get('name')
            if not objname:
                raise ValueError
        except:
            return HttpResponseBadRequest("JSON must contain 'name' attribute", content_type='text/plain')
        obj_info = object_query(name=objname)
        if obj_info:
            return HttpResponse(json.dumps(obj_info), content_type='application/json')
        else:
            return HttpResponseNotFound("Object not found", content_type='text/plain')

    def get(self, request, *args, **kwargs):
        objname = request.resolver_match.kwargs.get('objname')
        if objname:
            obj_info = object_query(name=objname)
            if obj_info:
                return HttpResponse(json.dumps(obj_info), content_type='application/json')
            else:
                return HttpResponseNotFound("Object not found", content_type='text/plain')
        else:
            usage = """\
            POST JSON to get object info:

            {{ "name": "M 82" }}

            Or, you can use GET:

            GET {}M+82

            Data will be returned as a JSON object, or a 404 if the object was not found.

            {{
                "query": "M 82",
                "detail_url": "http://simbad.u-strasbg.fr/simbad/sim-basic?Ident=M+82",
                "data_retrieved": "2018-03-24T05:21:12Z",
                "object_info": {{
                  "oid": 433918,
                  "mainId": "M 82",
                  "otype": "Interacting Galaxies",
                  "mtype": "I0edge",
                  "ra": 148.96845833333333,
                  "dec": 69.67970277777778,
                  "dim_wavelg": "I",
                  "dim_angle": 67,
                  "dim_majaxis": 5.070000171661377,
                  "dim_minaxis": 1.621999979019165,
                  "dim_qual": "C",
                  "idlist": [
                    "KPG 218b",
                    "LEDA 28655",
                    "M 82",
                    "[M98c] 095145.3+695511",
                    "MCG+12-10-011",
                    "NAME Cigar Galaxy",
                    "NAME UMa A",
                    "NGC 3034",
                    "[NKB95] N3034",
                    "NRAO 341",
                    ...
                    ...
                    ...
                  ]
                }}
            }}
            """.format(request.path)
            return HttpResponseBadRequest(dedent(usage), content_type='text/plain')
