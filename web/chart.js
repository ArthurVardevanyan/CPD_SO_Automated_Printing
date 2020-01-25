window.onload = function () {
  $.ajax({
    url: "http://localhost/web/data.php",
    method: "GET",
    success: function (data) {
      console.log(data);
      var date = [];
      var orders = [];

      for (var i in data) {
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
    }
  })
  $.ajax({
    url: "http://localhost/web/cost.php",
    method: "GET",
    success: function (data) {
      console.log(data);
      var order = [];
      var cost = [];

      for (var i in data) {
        order.push(data[i].order_number);
        cost.push(data[i].cost);
      }

      new Chart(document.getElementById("Price-line-chart"), {
        type: 'line',
        data: {
          labels: order,
          datasets: [{
            data: cost,
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
    }
  })
  $.ajax({
    url: "http://localhost/web/recent.php",
    method: "GET",
    success: function (data) {
      console.log(data);
      $(document).ready(function () {
//https://datatables.net/forums/discussion/32107/how-to-load-an-array-of-json-objects-to-datatables
        var aDemoItems = data;

        //Load  datatable
        var oTblReport = $("#tblReportResultsDemographics")

        oTblReport.DataTable({
          data: aDemoItems,
          "columns": [
            { "data": "order_number", "title": "Number" },
            { "data": "status", "title": "Status" },
            { "data": "cost", "title": "Cost" },
          ]
        });
      });
      //#var RecentOrders = "<tr><th>Order Number</th><th>Order Status</th><th>Order Cost</th></tr>";
      //for (let i = data.length - 1; i >= 0; i--) {
      //  RecentOrders = RecentOrders + "<tr><td>" + data[i].order_number + "</td><td>" + data[i].status + "</td><td>$" + data[i].cost.slice(0, 5) + "</td></tr>";
      //}
      //document.getElementById("RecentOrders").innerHTML = RecentOrders;



    }
  })
};