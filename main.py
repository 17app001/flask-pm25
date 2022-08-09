from flask import Flask, render_template
from datetime import datetime
from scrape.pm25 import get_pm25


app = Flask(__name__)


@app.route('/pm25')
def pm25():
    columns, values = get_pm25()

    print(columns, values)

    return render_template('./pm25.html', **locals())


@app.route('/stock')
def get_stock():
    stocks = [
        {'分類': '日經指數', '指數': '22,920.30'},
        {'分類': '韓國綜合', '指數': '2,304.59'},
        {'分類': '香港恆生', '指數': '25,083.71'},
        {'分類': '上海綜合', '指數': '3,380.68'}
    ]

    date = get_today()

    return render_template('./stock.html', **locals())


@app.route('/bmi/name=<name>&height=<height>&weight=<weight>')
def get_bmi(name, height, weight):
    try:
        bmi = round(eval(weight)/(eval(height)/100)**2, 2)
        return f'{name} BMI:{bmi}'

    except Exception as e:
        print(e)
        return '請輸入正確的身高或體重!'


@app.route('/add/x=<x>&y=<y>')
def add(x, y):
    try:
        return f'{x}+{y}={eval(x)+eval(y)}'
    except Exception as e:
        print(e)
        return '<h1 style="color:red">輸入錯誤!</h1>'


# 單一參數用法
@app.route('/')
@app.route('/<name>')
def index(name='GUEST'):
    content = {
        'name': name,
        'date': get_today()
    }

    return render_template('./index.html', content=content)
    # return f'<h1>Hello, {name}</h1><p>{get_today()}</p>'


@app.route('/today')
def get_today():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    # print(pm25())
    # print(get_bmi('jerry', '167', '67'))
    app.run(debug=True)
