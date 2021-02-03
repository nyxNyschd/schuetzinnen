from flask import Flask, request, render_template
from Backend import suchfunktion

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        suchwort = request.form['input']
        results = suchfunktion.main_search(suchwort)
        similar_results = suchfunktion.similar_search(suchwort)
        similar_results = [text for text in similar_results if text not in results]
        return render_template('suche.html', len=len(results), results=results, similar_results=similar_results)
    else:
        return render_template('suche.html')

if __name__ == '__main__':
    app.run()