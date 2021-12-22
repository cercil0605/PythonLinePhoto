# coding: UTF-8
#現状の問題点 SSLができない（certなど）
from flask import Flask, render_template, request, redirect, url_for, Response
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "test\n"

if __name__ == '__main__':
    context = ('server.pem', 'server_key.key')
    app.run(host='0.0.0.0', port=4567, ssl_context=context, threaded=True, debug=True)