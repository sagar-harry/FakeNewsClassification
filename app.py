from flask import Flask, render_template, request, jsonify
import os
import yaml
import joblib

params_path = "params.yaml"
webapp_root = "webapp"


static_dir = os.path.join(webapp_root, "static")
template_dir = os.path.join(webapp_root, "templates")
app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)

def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def predict(title, content):
    config = read_params(params_path)
    model_dir_path = config["prediction"]["final-model"]
    model = joblib.load(model_dir_path)
    prediction = model.predict([title+"---"+content])
    return prediction[0]

def api_response(request):
    try:
        title, content = request.json.values()
        response = "FAKE NEWS"
        if predict(title, content)==1:
            response="REAL NEWS"
        response_ = {"response": response}
        return response_
    except:
        print("Error has occured")
        return {"error":"Something went wrong"}


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            if request.form:
                title = request.form["title"]
                content = request.form["content"]
                response_ = predict(title, content)
                news_truth = "REAL NEWS"
                if response_==0:
                    news_truth="FAKE NEWS"
                return render_template("index.html", response_=news_truth)
            elif request.json:
                response_ = api_response(request)
                return jsonify(response_)
        except:
            print("Error occured")
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
