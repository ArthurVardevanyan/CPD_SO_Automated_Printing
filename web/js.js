window.onload = function () {
    $.ajax({
        url: "http://localhost/web/orders.php",
        method: "GET",
        success: function (data) {
            $(document).ready(function () {
                //https://datatables.net/forums/discussion/32107/how-to-load-an-array-of-json-objects-to-datatables
                var aDemoItems = data;

                //Load  data table
                var oTblReport = $("#orders")

                oTblReport.DataTable({
                    data: aDemoItems,
                    "order": [[0, "desc"]],
                    "columns": [
                        { "data": "order_number", "title": "Order Number" },
                        { "data": "order_subject", "title": "Order Subject" },
                        { "data": "date_ordered", "title": "Date Ordered" },
                        { "data": "cost", "title": "Cost" },
                        { "data": "status", "title": "Status" }
                        //{ "data": "first_name", "title": "First Name" },
                        //{ "data": "last_name", "title": "Last Name" }
                    ]
                });
            });
        }
    })
};