from flask import Flask, request


app = Flask(__name__)

@app.route('/')
def hello_world():
  return f'Hello, {request.remote_addr}!'

@app.route("/headers")
def headers():
  headers = f'<html>\n<pre>\n{request.headers}</pre>\n</html>\n'
  return headers

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8000)
