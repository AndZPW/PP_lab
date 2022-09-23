from flask import Flask
from flask import make_response
from waitress import serve

app = Flask(__name__)

status_code: int = 200


@app.route('/api/v1/hello-world-11')
def index(variant: int):
    return make_response(f"Hello World 11", status_code)


if __name__ == '__main__':
    serve(app, port=5001)
