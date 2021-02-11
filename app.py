from flask import Flask, request, render_template
from backend import suchfunktion
import time
from backend.suchfunktion import substring_cleaning, preprocess_query

app = Flask(__name__)
app.debug = True


@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        suchwort = request.form['input']
        suchwort = substring_cleaning(suchwort)
        suchwort = preprocess_query(suchwort)
        print(suchwort)
        start_time = time.time()
        results = suchfunktion.main_search(suchwort)
        time_1 = time.time() - start_time
        print("Time 1: ", time_1)
        similar_word = suchfunktion.similar_word(suchwort)
        print(similar_word)
        time_2 = time.time() - time_1
        print("Time 2: ", time_2)
        similar_results = suchfunktion.similar_search(similar_word)
        time_3 = time.time() - time_2
        print("Time 3: ", time_3)
        return render_template('suche.html', len=len(results), results=results, similar_results=similar_results,
                               similar_word=similar_word)
    else:
        return render_template('suche.html')


if __name__ == '__main__':
    app.run()
