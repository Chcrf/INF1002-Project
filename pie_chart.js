document.addEventListener("DOMContentLoaded", function(){
  fetch('pie.json')
    .then(response => response.json())
    .then(data => {
      Jdata = data;
      getchart(Jdata); // Pass Jdata to getchart
    })
    .catch(error => console.error("Error loading JSON:", error));

  function getchart(jsonData){ // Accept jsonData as an argument
    var chartDom = document.getElementById('main');
    var myChart = echarts.init(chartDom);
    var option;

    option = {
      title: {
        text: 'Top 15 Job Categories',
        left: 'center'
      },
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

    option && myChart.setOption(option); 
  }
});