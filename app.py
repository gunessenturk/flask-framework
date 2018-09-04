from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
import numpy as np

import os

from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, LabelSet

app = Flask(__name__)

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        if os.path.exists("templates/stocks.html"):
            os.remove("templates/stocks.html")
        
        db_code = "EOD"
        # ds_code = "HD"
        ds_code = request.form['company']
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

        data=dict( date=df['date'].tolist(), price=df['closing'])

        p1 = figure(x_axis_type="datetime", title="Closing Stock Prices")
        p1.grid.grid_line_alpha=0.3
        p1.xaxis.axis_label = 'Date'
        p1.yaxis.axis_label = 'Price'

        p1.line(df['date'], df['closing'], color='#A6CEE3', legend=ds_code)

        p1.legend.location = "top_left"

        p1.patches('date', 'price', source=data)

        # open a browser
        output_file("templates/stocks.html", title="Stock Prices")
        show(gridplot([[p1]], plot_width=400, plot_height=400))

        return redirect('/graph')

@app.route('/graph')
def graph():
    return render_template('stocks.html')

if __name__ == '__main__':
  app.run(port=33507, debug=True)
