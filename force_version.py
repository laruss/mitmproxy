import json
import time
import urllib

from mitmproxy import ctx, http


def request(flow: http.HTTPFlow) -> None:

    version_name = '5.24'
    version_code = '2982'
    version_full = '{}.{}'.format(version_name, version_code)

    tokens = {
        'version': version_full,
        'version_code': version_code,
        'versionName': version_full,
        'versionCode': version_code
    }

    def replace_all(dict, tokens):
        for key,value in tokens.items():
            if key in dict:
                dict[key] = value

    if flow.request.method == 'GET':
        replace_all(flow.request.query, tokens)

    if flow.request.method == 'POST':
        request_text = flow.request.get_text()
        request_json = json.loads(request_text)
        replace_all(request_json, tokens)
        if 'versions' in request_json:
            replace_all(request_json['versions'], tokens)
        flow.request.set_text(json.dumps(request_json))
