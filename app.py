from flask import Flask, request, render_template
from Backend import suchfunktion

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        suchwort = request.form['input']
        results = suchfunktion.main_search(suchwort)
        return render_template('suche.html', len=len(results), results=results)
    else:
        return render_template('suche.html')

if __name__ == '__main__':
    app.run()