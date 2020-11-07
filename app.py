from flask import Flask, request, render_template

import dumpAndRetrieve

app = Flask(__name__)


@app.route('/')
def searchBunny():
    render_template('suchfeld_Front.html')


@app.route('/', methods=['POST'])
def searchBunny_post():

    text = request.form['myForm']
    return dumpAndRetrieve.probier_mal_das(text)


if __name__ == '__main__':
    app.run()

#$('#<form-id>').serialize()