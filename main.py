from flask import Flask, render_template, request
from datetime import datetime
from scrape.pm25 import get_pm25
import json

app = Flask(__name__)


@app.route('/pm25-charts')
def pm25_charts():
    return render_template('./pm25-charts.html')


# 取得資料庫或爬蟲的資料回傳json資料結構
@app.route('/pm25-json', methods=['GET','POST'])
def pm25_json():
    columns, values = get_pm25()

    stationName = [value[1] for value in values]
    result = [value[2] for value in values]

    data = {'stationName': stationName, 'result': result}

    return json.dumps(data, ensure_ascii=False)


@app.route('/pm25', methods=['GET', 'POST'])
def pm25():
    sort = False
    # 使用GET接收
    # if request.args.get('sort'):
    #     sort = True
    if request.method == 'POST':
        sort = True if request.form.get('sort') else False

    date = get_today()
    columns, values = get_pm25(sort=sort)

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
