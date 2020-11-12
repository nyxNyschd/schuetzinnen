from flask import Flask, request, render_template
import pandas as pd
import spacy
from spacy.lang.en import English
from backendKrams import suchfunktion

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def start():
    # short_desc_eng = pd.read_csv('cpv_short_desc_eng.csv', delimiter=',')
    # shorty = pd.DataFrame(short_desc_eng)
    # short_desc = shorty['short_desc_eng'].tolist()
    if request.method == 'POST':
        suchwort = request.form['input']
        results = suchfunktion.all_values_containing_substring(suchwort)
        return render_template('/suche.html', len=len(results), results=results)

    else:

        return render_template('/suche.html')


if __name__ == '__main__':
    app.run()
