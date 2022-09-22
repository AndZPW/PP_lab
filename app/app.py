from flask import Flask
from flask import make_response
from waitress import serve

app = Flask(__name__)

status_code: int = 200


@app.route('/api/v1/hello-world-<variant>')
def index(variant: int):
    return make_response(f"Hello World {variant}", status_code)


if __name__ == '__main__':
    serve(app, port=5001)
