
# import importlib
from distutils.log import debug
from flask import Flask, redirect, request, url_for, render_template, jsonify, json

from EquityBulls import limited
from Model import ModelPredictor
#from iifl import limitedIifl
from third import headings_links

app = Flask(__name__)  # define app
apiKey = app.config.from_envvar('APIKEY')

@app.route('/')  # path set
def home():
    return render_template('index.html')


@app.route('/equitybulls')  # path set
def EQ():
    return render_template('newsEquity.html', limited=limited)

# @app.route('/iifl') #path set
# def iifl():
#     return render_template('newsIifl.html',limitedIifl=limitedIifl)


@app.route('/livemint')  # path set
def livemint():
    return render_template('livemint.html', limited=headings_links)


@app.route('/predict', methods=['GET', 'POST'])  # path set
def predict():
    result = {}

    if request.method == 'GET' or request.method == 'POST':
        formData = request.form
        query = str(formData.get('query'))
        
        if (query):
            result = ModelPredictor()
            with open(file='result.json', mode='w+') as f:
                string_res = json.dumps({
                    "result": str(result[0])
                })
                f.write(string_res)
                
    with open(file='result.json') as file:
        data = file.read()
        result = json.loads(data)
    
    return render_template('predict.html', result=result)




@app.route('/formdisplay', methods=['GET', 'POST'])  # path set
def formdisplay():
    return render_template('predict.html', headings_links=headings_links)


@app.route('/sentiment')  # path set
def sentiment():
    return render_template('sentiment.html')


@app.route("/", methods=['GET', 'POST'])
def index():
    return jsonify({
        "msg": "Hello World"
    })


app.run(debug=True)

# @app.route("/<name>")
# def user(name):
#     return f"Hello {name}"


# @app.route("/admin/")
# def admin():
#     return redirect(url_for("user", name="Admin"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)

    # http_server = WSGIServer(('', 5000), app)
    # http_server.serve_forever()
