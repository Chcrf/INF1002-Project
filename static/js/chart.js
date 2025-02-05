document.addEventListener("DOMContentLoaded", function(){
  var getclick = document.getElementById("toggle_button");
  var labelText = document.getElementById("toggle_asc_dsc");
  var orderup = 0 // 0 = asc, 1 = desc
  getclick.addEventListener('click',function(){
    if(orderup == 0){
      orderup = 1
      labelText.innerHTML = "Descending";
    }else{
      orderup = 0
      labelText.innerHTML = "Ascending";
    }
    getchart(orderup)
  });
  getchart(orderup)
})


function getchart(orderup){
  var chartDom = document.getElementById('graph1');
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
        dimensions: ['name', 'age', 'profession', 'score', 'date'],
        source: [
          ['Hannah Krause', 41, 'Engineer', 314, '2011-02-12'],
          ['Zhao Qian', 20, 'Teacher', 351, '2011-03-01'],
          ['Jasmin Krause ', 52, 'Musician', 287, '2011-02-14'],
          ['Li Lei', 37, 'Teacher', 219, '2011-02-18'],
          ['Karle Neumann', 25, 'Engineer', 253, '2011-04-02'],
          ['Adrian Groß', 19, 'Teacher', 10, '2011-01-16'],
          ['Mia Neumann', 71, 'Engineer', 165, '2011-03-19'],
          ['Böhm Fuchs', 36, 'Musician', 318, '2011-02-24'],
          ['Han Meimei', 67, 'Engineer', 366, '2011-03-12'],
        ]
      },
      {
        transform: {
          type: 'sort',
          config: { dimension: 'score', order: ordering }
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
      encode: { x: 'name', y: 'score' },
      datasetIndex: 1
    }
  };
  
  option && myChart.setOption(option);
}
