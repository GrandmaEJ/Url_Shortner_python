from flask import Flask, render_template
from us import init_routes

app = Flask(__name__)
init_routes(app)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8398)