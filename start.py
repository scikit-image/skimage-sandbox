from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return 'The server is up!'

@app.route('/code')
def write_code():
	return render_template('runcode.html')

@app.route('/runcode', methods=['POST'])
def run_code():
	content = request.json['data']
	# DEBUG print content
	# fire up docker
	return jsonify(result='AJAX test complete');

if __name__ == '__main__':
    app.run()