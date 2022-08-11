
drawPM25();

function drawPM25() {
    $.ajax(
        {
            url: "/pm25-json",
            type: "POST",
            dataType: "json",
            success: (data) => {
                console.log(data);
                drawPM25Charts(data);
            },
            error: () => {
                alert("讀取失敗!");
            }
        }
    );
}

function drawPM25Charts(data) {
    var myChart = echarts.init(document.getElementById('main'));
    var option = {
        title: {
            text: 'PM2.5全台資訊圖'
        },
        tooltip: {},
        legend: {
            data: ['PM2.5']
        },
        xAxis: {
            data: data['stationName']
        },
        yAxis: {},
        series: [
            {
                name: '數值',
                type: 'bar',
                data: data['result']
            }
        ]
    };

    myChart.setOption(option);
}
