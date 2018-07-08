import os

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Testing 1,2,3"


if __name__ == '__main__':
    # Heroku defines the port we must use in the "PORT" env variable
    port = int(os.environ.get("PORT", 8000))
    print("Port to use {}".format(port))
    app.run(debug=True, port=port)