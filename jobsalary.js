

document.addEventListener("DOMContentLoaded", function(){
  var getclick = document.getElementById("toggle_button");
  var orderup = 0 // 0 = asc, 1 = desc
  getclick.addEventListener('click',function(){
    if(orderup == 0){
      orderup = 1
    }else{
      orderup = 0
    }
    getchart(orderup,Jdata)
  });
  fetch('JobvsSalary.json')
  .then(response => response.json())
  .then(data => {
    Jdata = data
    getchart(orderup, Jdata);
    })
.catch(error => console.error("Error loading JSON:", error));
  });

  

function getchart(orderup,jsonData){
  var chartDom = document.getElementById('main');
  var myChart = echarts.init(chartDom);
  var option;
  var ordering = 1
  if (orderup == 0){
    ordering = 'desc'
  }else{
    ordering = 'asc'
  }
    

  option = {
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
      axisLabel: { interval: 0, rotate: 30 }
    },
    yAxis: {},
    series: {
      type: 'bar',
      encode: { x: 'Job', y: 'Salary' },
      datasetIndex: 1,
    }
  };
  
  option && myChart.setOption(option);
}
