import pandas as pd

api_url = 'https://sta.ci.taiwan.gov.tw/STA_AirQuality_v2/v1.0/Datastreams?$expand=Thing,Observations($orderby=phenomenonTime%20desc;$top=1)&$filter=name%20eq%20%27PM2.5%27%20and%20Thing/properties/authority%20eq%20%27%E8%A1%8C%E6%94%BF%E9%99%A2%E7%92%B0%E5%A2%83%E4%BF%9D%E8%AD%B7%E7%BD%B2%27%20and%20substringof(%27%E7%A9%BA%E6%B0%A3%E5%93%81%E8%B3%AA%E6%B8%AC%E7%AB%99%27,Thing/name)&$count=true'


def get_pm25(sort=False, show=False):
    datas = pd.read_json(api_url)['value']
    values = []

    for data in datas:
        city, stationName = data['Thing']['properties']['city'], data['Thing']['properties']['stationName']
        result, resultTime = data['Observations'][0]['result'], data['Observations'][0]['resultTime']

        if show:
            print(city, stationName, result, pd.to_datetime(
                resultTime).strftime('%Y-%m-%d %H:%M:%S'))

        values.append([city, stationName, result, pd.to_datetime(
            resultTime).strftime('%Y-%m-%d %H:%M:%S')])

    df = pd.DataFrame(
        values, columns=['city', 'stationName', 'result', 'resultTime'])

    if sort:
        df = df.sort_values('result', ascending=False)

    return list(df.columns), df.values.tolist()


if __name__ == '__main__':
    get_pm25()
