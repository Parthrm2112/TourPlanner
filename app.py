from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Smart Tourism Project - Welcome!"

if __name__ == '__main__':
    app.run(debug=True)
