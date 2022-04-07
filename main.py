import requests
from flask import Flask, request, Response
from config import urls, origin
from flask_cors import CORS, cross_origin

app = Flask(__name__)
# CORS(app, resources=r"/*":{"origins": "*"}})
CORS(app)
SITE_NAME = 'http://proxy.40146762.qpc.hal.davecutting.uk'


# https://medium.com/customorchestrator/simple-reverse-proxy-server-using-flask-936087ce0afb
@app.route('/', defaults={'path': ''}, methods=["GET"])
@app.route('/<path:path>', methods=["GET"])
@cross_origin()
def proxy(path):
    requrl = ""
    if not request.args:
        msg = "No arguments recieved"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400
    if request.method == 'GET':
        new_path = getKeysByValue(urls, path)
        x = request.args.get('x')
        y = request.args.get('y')
        print(request.args)
        params = {'x': x, 'y': y}
        # path is url of api
        resp = requests.get(f'{new_path}', params=params)
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
    return response


def getKeysByValue(urldict, valuetofind):
    list_of_items = urldict.items()
    for item in list_of_items:
        if item[0] == valuetofind:
            newurl = str(item[1]).replace("'", "").replace('[', "").replace(']', "")
            return newurl


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
    # app.run()
