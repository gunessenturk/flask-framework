from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        db_code = "EOD"
        ds_code = "HD"
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        url = 'https://www.quandl.com/api/v3/datasets/'+db_code+'/'+ds_code+'?column_index=4&start_date='+start_date+'&end_date='+end_date+'&api_key=D75Ftay9wEKd3jtrYJG8'
        r = requests.get(url)
        f = r.json()
        df = pd.DataFrame.from_dict(f)
        dataset = df.loc['data']

        file = open('output.txt', 'w')
        file.write('%s\n\n' % (f))
        file.close()

        return redirect('/graph')

@app.route('/graph')
def graph():
    return render_template('stocks.html')

if __name__ == '__main__':
  app.run(port=33507, debug=True)
