document.addEventListener("DOMContentLoaded", function () {
    displayJobSalary();
    
});

function displayJobSalary(){
    var getclick = document.getElementById("toggle_button");
    var orderup = 0 // 0 = asc, 1 = desc
    getclick.addEventListener('click', function () {
        if (orderup == 0) {
            document.getElementById("toggle_asc_dsc").innerHTML="Descending";
            orderup = 1
        } else {
            document.getElementById("toggle_asc_dsc").innerHTML="Ascending";
            orderup = 0
        }
        getchart(orderup, Jdata)
    });
    fetch('json/JobvsSalary.json')
        .then(response => response.json())
        .then(data => {
            Jdata = data
            getchart(orderup, Jdata);
        })
        .catch(error => console.error("Error loading JSON:", error));
}

function getchart(orderup, jsonData) {
    var chartDom = document.getElementById('graph3');

    // Edit width and height
    var parentDiv = document.querySelector(".carousel-item.active .carousel-graph");

    var myChart = echarts.init(chartDom);
    var option;
    var ordering = 1
    if (orderup == 0) {
        ordering = 'desc'
    } else {
        ordering = 'asc'
    }


    option = {
        tooltip: {
            trigger: 'axis'
        },
        dataset: [
            {
                dimensions: ['Job', 'Salary'],
                source: jsonData
            },
            {
                transform: {
                    type: 'sort',
                    config: { dimension: 'Salary', order: ordering }
                }
            }
        ],
        xAxis: {
            type: 'category',
            axisLabel: { interval: 0, rotate: 20 }
        },
        yAxis: {},
        series: {
            type: 'bar',
            encode: { x: 'Job', y: 'Salary' },
            datasetIndex: 1,
        }
    };

    if (parentDiv.offsetHeight != 0){
        myChart.resize({height: 420, width: parentDiv.offsetWidth});
    }
    option && myChart.setOption(option);
}