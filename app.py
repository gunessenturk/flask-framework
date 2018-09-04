from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
import numpy as np

from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, LabelSet

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

        date = np.array(dataset[0])[:, 0]
        closing_price = np.array(dataset[0])[:, 1]
        df = pd.DataFrame({'date':date, 'closing':closing_price})
        df['date'] = pd.to_datetime(df['date'])

        file = open('output.txt', 'w')
        file.write('%s\n\n' % (df['date']))
        file.close()



        return redirect('/graph')

@app.route('/graph')
def graph():
    return render_template('stocks.html')

if __name__ == '__main__':
  app.run(port=33507, debug=True)
