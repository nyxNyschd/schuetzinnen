from flask import Flask, request, render_template
from Backend import suchfunktion
import time
from Backend.suchfunktion import substring_cleaning, preprocess_query

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        suchwort = request.form['input']
        suchwort = substring_cleaning(suchwort)
        suchwort = preprocess_query(suchwort)
        start_time=time.time()
        results = suchfunktion.main_search(suchwort)
        time_1=time.time()-start_time
        print("Time 1: ", time_1)
        similar_results = suchfunktion.similar_search(suchwort)
        time_2=time.time()-time_1

        print("Time 2: ", time_2)
        similar_results = [text for text in similar_results if text not in results]
        time_3=time.time()-time_2
        print("Time 3: ", time_3)
        return render_template('suche.html', len=len(results), results=results, similar_results=similar_results)
    else:
        return render_template('suche.html')

if __name__ == '__main__':
    app.run()