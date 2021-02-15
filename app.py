from flask import Flask, request, render_template
from backend import suchfunktion

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        suchwort = request.form['input']
<<<<<<< HEAD
        results = suchfunktion.suche_substring(suchwort)
=======
        results = suchfunktion.all_values_containing_substring(suchwort)
>>>>>>> f8acc12... Review Code
        return render_template('suche.html', len=len(results), results=results)

    else:

        return render_template('suche.html')


# @app.route('/', methods=['GET', 'POST'])
# def more():
#     if request.method == 'GET':
#         ergebnisse = request.form['submit']
#         showmores = suchfunktion.values_containing_substring(ergebnisse)
#         return render_template('suche.html', len=len(showmores), showmores=showmores)
#
#     else:
#
#         return render_template('suche.html')
#
#
# def contact():
#     if request.method == 'POST':
#         if request.form['submit_button'] == 'Do Something':
#             ergebnisse = request.form['submit']
#             showmores = suchfunktion.values_containing_substring(ergebnisse)
#             return render_template('suche.html', len=len(showmores), showmores=showmores)
#         else:
#
#             return render_template('suche.html')


if __name__ == '__main__':
    app.run()
