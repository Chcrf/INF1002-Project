document.addEventListener("DOMContentLoaded", function () {
    displayPieChart();

});

function displayPieChart() {
    fetch('json/pie.json')
        .then(response => response.json())
        .then(data => {
            Jdata = data;
            getchart(Jdata); // Pass Jdata to getchart
        })
        .catch(error => console.error("Error loading JSON:", error));

    function getchart(jsonData) { // Accept jsonData as an argument
        var chartDom = document.getElementById('graph2');

        // Edit width and height
        var parentDiv = document.querySelector(".carousel-item.active .carousel-graph");

        var myChart = echarts.init(chartDom);

        var option;

        option = {
            tooltip: {
                trigger: 'item'
            },
            series: [
                {
                    name: 'Job Categories',
                    type: 'pie',
                    radius: '50%',
                    data: jsonData,
                    emphasis: {
                        itemStyle: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    },
                    label: {
                        formatter: '{b}: {c} ({d}%)'
                    }
                }
            ]
        };

        myChart.resize({ height: parentDiv.offsetHeight, width: parentDiv.offsetWidth });
        option && myChart.setOption(option);
    }
}