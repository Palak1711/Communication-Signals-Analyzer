from flask import Flask, render_template, jsonify
from core.web_pipeline import run_web_session

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/start-session', methods=['POST'])
def start_session():
    result = run_web_session(duration=10)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)