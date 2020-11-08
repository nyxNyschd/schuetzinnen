from flask import Flask, request, render_template

from backendKrams import datastuff

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        suchwort = request.form['input']
        results = datastuff.all_values_containing_substring(suchwort)
        return render_template('/suche.html', len=len(results), results=results)

    else:

        return render_template('/suche.html')


if __name__ == '__main__':
    app.run()
