from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def index():
    return render_template("home.html")


@app.route("/product/<name>")
def product_page(name):
    return render_template("product_details.html", product_name=name)


@app.route("/test/")
def test():
    return render_template("test.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
