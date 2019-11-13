window.onload = function() {
  $.ajax({
    url: "http://localhost/web/data.php",
    method: "GET",
    success: function(data) {
      console.log(data);
      var date = [];
      var orders = [];

      for(var i in data) {
        date.push(data[i].date_ordered);
        orders.push(data[i].order_count);
      }
    
  new Chart(document.getElementById("line-chart"), {
    type: 'line',
    data: {
      labels: date,
      datasets: [{ 
          data: orders,
          label: "School Orders",
          borderColor: "#3e95cd",
          fill: false
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: 'School Orders Per Day'
      }
    }
  });
}})};