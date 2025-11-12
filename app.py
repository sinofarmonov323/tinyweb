from osonweb import TinyWeb

app = TinyWeb()

@app.route("/")
def homepage():
    return app.render_html_file("index.html")

app.run()