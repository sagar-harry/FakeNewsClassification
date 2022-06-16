from flask import Flask, render_template, request, jsonify
import os
from prediction_service import prediction

webapp_root = "webapp"


static_dir = os.path.join(webapp_root, "static")
template_dir = os.path.join(webapp_root, "templates")
app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            if request.form:
                response_ = prediction.form_response(request.form)
                print("Rahul"*100)
                print(response_)
                news_truth = response_
                if response_==0:
                    news_truth="FAKE NEWS"
                elif response_==1:
                    news_truth = "REAL NEWS"
                return render_template("index.html", response_=news_truth)
            elif request.json:
                response_ = prediction.api_response(request.json)
                return jsonify(response_)
        except Exception as e:
            return render_template("404.html", error=e)
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

