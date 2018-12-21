from flask import Flask, render_template

app = Flask(__name__)

@app.route('/hello')
def hello():

    src = 'https://wallpaperbrowse.com/media/images/soap-bubble-1958650_960_720.jpg'
    return render_template('hello.html', img=src)

@app.route('/')
def not404():
    return "at least not a 404 error!"

if __name__ == '__main__':
    app.run(debug=True)