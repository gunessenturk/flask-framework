from flask import Flask, render_template, request, redirect

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

        return redirect('/graph')

@app.route('/graph')
def graph():
    return render_template('stocks.html')

if __name__ == '__main__':
  app.run(port=33507, debug=True)
