window.onload = function () {
    $.ajax({
        url: "/web/statusL.php",
        method: "GET",
        success: function (data) {
            $(document).ready(function () {
                //https://datatables.net/forums/discussion/32107/how-to-load-an-array-of-json-objects-to-datatables
                var aDemoItems = data
                //Load  data table
                var oTblReport = $("#LeftToPrint")
                oTblReport.DataTable({
                    "pageLength": 10,
                    data: aDemoItems,
                    "order": [[0, "desc"]],
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
                        { "data": "date_ordered", "title": "Date Ordered" },
                        { "data": "order_subject", "title": "Order Subject" },
                        { "data": "sheets", "title": "Sheets" },
                    ],
                });
            });
        }
    })
    $.ajax({
        url: "/web/statusP.php",
        method: "GET",
        success: function (data) {
            $(document).ready(function () {
                //https://datatables.net/forums/discussion/32107/how-to-load-an-array-of-json-objects-to-datatables
                var aDemoItems = data
                //Load  data table
                var oTblReport = $("#Printing")
                oTblReport.DataTable({
                    "pageLength": 10,
                    data: aDemoItems,
                    "order": [[0, "desc"]],
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
                        { "data": "order_subject", "title": "Order Subject" },
                        { "data": "status", "title": "Printer" },
                        { "data": "sheets", "title": "Sheets" },
                    ],
                });
            });
        }
    })
    $.ajax({
        url: "/web/statusG.php",
        method: "GET",
        success: function (data) {
            $(document).ready(function () {
                //https://datatables.net/forums/discussion/32107/how-to-load-an-array-of-json-objects-to-datatables
                var aDemoItems = data
                //Load  data table
                var oTblReport = $("#LeftToPrintSum")
                oTblReport.DataTable({
                    "pageLength": 10,
                    data: aDemoItems,
                    "columns": [
                        { "data": "name", "title": "Deliver To:" },
                        { "data": "sheets", "title": "Sheets" },
                    ]
                });
            });
        }
    })
};