from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session, Response

app = Flask(__name__, static_url_path='/static')


@app.route('/generate', methods=['POST'])
def generate():
	print(request.data)
	return "true"

@app.route('/download', methods=['GET'])
def download():
	with open("addresses.csv") as fp:
		csv = fp.read()
	#csv = '1,2,3\n4,5,6\n'
	return Response(
		csv,
		mimetype="text/csv",
		headers={"Content-disposition":
				 "attachment; filename=addresses.csv"})

@app.route('/test', methods=['GET'])
def testPage():
	return render_template("index1.html")

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=5000)