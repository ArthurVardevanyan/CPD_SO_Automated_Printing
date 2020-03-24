window.onload = function () {
  $.ajax({
    url: "/web/dataY.php",
    method: "GET",
    success: function (data) {
      var date = [];
      var orders = [];
      for (var i in data) {
        date.push(data[i].date_ordered);
        orders.push(data[i].order_count);
      }
      var lineChart = new Chart(document.getElementById("line-chart"), {
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
      $("#orders_1").click(function () {
        var data = lineChart.data;
        data.labels = date;
        data.datasets[0].data = orders;
        lineChart.update();
      });
      $("#orders_2").click(function () {
        $.ajax({
          url: "/web/dataM.php",
          method: "GET",
          success: function (data) {
            var dateW = [];
            var ordersW = [];
            for (var i in data) {
              dateW.push(data[i].date_ordered);
              ordersW.push(data[i].order_count);
            }
            var data = lineChart.data;
            data.labels = dateW;
            data.datasets[0].data = ordersW;
            lineChart.update();
          }
        })
      });
      $("#orders_3").click(function () {
        $.ajax({
          url: "/web/dataW.php",
          method: "GET",
          success: function (data) {
            var dateW = [];
            var ordersW = [];
            for (var i in data) {
              dateW.push(data[i].date_ordered);
              ordersW.push(data[i].order_count);
            }
            var data = lineChart.data;
            data.labels = dateW;
            data.datasets[0].data = ordersW;
            lineChart.update();
          }
        })
      });
    }
  })
  $.ajax({
    url: "/web/cost.php",
    method: "GET",
    success: function (data) {
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
    url: "/web/recent.php",
    method: "GET",
    success: function (data) {
      $(document).ready(function () {
        //https://datatables.net/forums/discussion/32107/how-to-load-an-array-of-json-objects-to-datatables
        var aDemoItems = data;
        //Load  data table
        var oTblReport = $("#tblReportResultsDemographics")
        oTblReport.DataTable({
          data: aDemoItems,
          "order": [[0, "desc"]],
          "pageLength": 20,
          "columns": [
            {
              "data": "order_number", "title": "Order Number",
              "render": function (data, type, row, meta) {
                if (type === 'display') {
                  data = '<a href=/web/order.php?id=' + aDemoItems[meta.row].email_id + '&on=' + data + '>' + data + '</a>';
                }
                return data;
              }
            },
            { "data": "order_subject", "title": "Subject" },
            { "data": "status", "title": "Status" },
          ]
        });
      });
    }
  })
};