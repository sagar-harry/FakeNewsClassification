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
                title = request.form["title"]
                content = request.form["content"]
                response_ = prediction.predict(title, content)
                news_truth = "REAL NEWS"
                if response_==0:
                    news_truth="FAKE NEWS"
                elif response_==-1:
                    news_truth="Enter a valid value"
                return render_template("index.html", response_=news_truth)
            elif request.json:
                response_ = prediction.api_response(request)
                return jsonify(response_)
        except Exception as e:
            return render_template("404.html", error=e)
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

