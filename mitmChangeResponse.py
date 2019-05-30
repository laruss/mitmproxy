from mitmproxy import ctx, http
import json
'''sets NEW_RESPONSE_CODE to API methods, not listed in ChangeResponseCode.white_list'''

NEW_RESPONSE_BODY = None #{"no_action":1}
NEW_RESPONSE_CODE = 429
NEW_RESPONSE_HEADERS = {"Retry-After":"5"}
REQ_PATHES_TO_CHANGE = ["getordersbyfilter"]

class ChangeResonse:
    def __init__(self):
        self.request_path = None

    def request(self, flow):
        self.request_path = flow.request.path

    def response(self, flow):
        for el in REQ_PATHES_TO_CHANGE:
            if el in self.request_path:
                print(flow.response.headers)
                self.setNewCode(flow)
                self.changeHeaders(flow)
                self.setNewBody(flow)

    def setNewCode(self, flow):
        if NEW_RESPONSE_CODE:
            flow.response.status_code = NEW_RESPONSE_CODE

    def changeHeaders(self, flow):
        if NEW_RESPONSE_HEADERS:
            for new_header, nh_content in NEW_RESPONSE_HEADERS.items():
                if new_header in flow.response.headers:
                    flow.response.headers[new_header] = nh_content
                else: flow.response.headers.update({new_header:nh_content})

    def setNewBody(self, flow):
        if NEW_RESPONSE_BODY:
            flow.response.text = json.dumps(NEW_RESPONSE_BODY)

addons = [
    ChangeResonse()
]