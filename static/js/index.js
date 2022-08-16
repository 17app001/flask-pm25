let chart1 = echarts.init(document.getElementById("main"));
let chart2 = echarts.init(document.getElementById("six"));

const dateEl = document.querySelector("#date");
const pm25HighSite = document.querySelector("#pm25_high_site");
const pm25HighValue = document.querySelector("#pm25_high_value");
const pm25LowSite = document.querySelector("#pm25_low_site");
const pm25LowValue = document.querySelector("#pm25_low_value");


window.onresize = function () {
    chart1.resize();
    chart2.resize();
};

drawPM25();

function renderMaxPM25(data) {
    const stationName = data["stationName"];
    const result = data["result"];
    const maxIndex = result.indexOf(Math.max(...result));
    const minIndex = result.indexOf(Math.min(...result));

    pm25HighSite.innerText = stationName[maxIndex];
    pm25HighValue.innerText = result[maxIndex];
    pm25LowSite.innerText = stationName[minIndex];
    pm25LowValue.innerText = result[minIndex];
    dateEl.innerText = data["date"];
}


function drawSixPM25() {
    chart2.showLoading();
    $.ajax(
        {
            url: "/six-pm25-json",
            type: "POST",
            dataType: "json",
            success: (data) => {
                chart2.hideLoading();
                drawSixPM25Charts(data);
            },
            error: () => {
                chart2.hideLoading();
                alert("讀取失敗!");
            }
        }
    );
}


function drawSixPM25Charts(data) {
    var option = {
        title: {
            text: 'PM2.5六都資訊圖'
        },
        tooltip: {},
        legend: {
            data: ['PM2.5']
        },
        xAxis: {
            data: data['cities']
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

    chart2.setOption(option);
}


function drawPM25() {
    chart1.showLoading();
    $.ajax(
        {
            url: "/pm25-json",
            type: "POST",
            dataType: "json",
            success: (data) => {
                chart1.hideLoading();
                drawPM25Charts(data);
                renderMaxPM25(data);
                drawSixPM25();
            },
            error: () => {
                chart1.hideLoading();
                alert("讀取失敗!");
            }
        }
    );
}

function drawPM25Charts(data) {
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

    chart1.setOption(option);
}
