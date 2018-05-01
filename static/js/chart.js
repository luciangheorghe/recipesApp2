// Global parameters:
// do not resize the chart canvas when its container does (keep at 600x400px)
Chart.defaults.global.responsive = false;

// define the chart data
var chartData = {
  labels : [{% for item in the_recipe %}
             "{{item.time}}",
            {% endfor %}],
  datasets : [{
      label: '{{ legend }}',
      fill: true,
      lineTension: 0.1,
      backgroundColor: "rgba(75,192,192,0.4)",
      borderColor: "rgba(75,192,192,1)",
      borderCapStyle: 'butt',
      borderDash: [],
      borderDashOffset: 0.0,
      borderJoinStyle: 'miter',
      pointBorderColor: "rgba(75,192,192,1)",
      pointBackgroundColor: "#fff",
      pointBorderWidth: 1,
      pointHoverRadius: 5,
      pointHoverBackgroundColor: "rgba(75,192,192,1)",
      pointHoverBorderColor: "rgba(220,220,220,1)",
      pointHoverBorderWidth: 2,
      pointRadius: 1,
      pointHitRadius: 10,
      data : [{% for item in the_recipe %}
                {{item.time}},
              {% endfor %}],
      spanGaps: false
  }]
}

// get chart canvas
var ctx = document.getElementById("myChart").getContext("2d");

// create the chart using the chart canvas
var myChart = new Chart(ctx, {
  type: 'line',
  data: chartData,
});








































//
// let myChart = document.getElementById('myChart').getContext('2d');
//
//     // Global Options
//     Chart.defaults.global.defaultFontFamily = 'Lato';
//     Chart.defaults.global.defaultFontSize = 18;
//     Chart.defaults.global.defaultFontColor = '#777';
//
//     let massPopChart = new Chart(myChart, {
//       type:'bar', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
//       data:{
//         labels:[{% for item in recipe %}
//                   "{{item.time}}",
//                 {% endfor %}],
//         datasets:[{
//           label:'{{the_recipe.title}}',
//           data:[
//             {% for item in recipe %}
//                   {{item.time}},
//             {% endfor %}
//           ],
//           backgroundColor:'green',
//           // backgroundColor:[
//           //   'rgba(255, 99, 132, 0.6)',
//           //   'rgba(54, 162, 235, 0.6)',
//           //   'rgba(255, 206, 86, 0.6)',
//           //   'rgba(75, 192, 192, 0.6)',
//           //   'rgba(153, 102, 255, 0.6)',
//           //   'rgba(255, 159, 64, 0.6)',
//           //   'rgba(255, 99, 132, 0.6)'
//           // ],
//           borderWidth:1,
//           borderColor:'#777',
//           hoverBorderWidth:3,
//           hoverBorderColor:'#000'
//         }]
//       },
//       options:{
//         title:{
//           display:true,
//           text:'Nutrition',
//           fontSize:18
//         },
//         legend:{
//           display:true,
//           position:'right',
//           labels:{
//             fontColor:'#000'
//           }
//         },
//         layout:{
//           padding:{
//             left:50,
//             right:0,
//             bottom:0,
//             top:0
//           }
//         },
//         tooltips:{
//           enabled:true
//         }
//       }
//     });
