window.onload = function () {
    $("#submit").click(function () {
        Form();
        return false;
    });
    $("#validate").click(function () {
        Form();
        return false;
    });
    $("#csv").click(function () {
        processShipment();
    });

};

function Form() {
    var x = document.forms["orderForm"]["fOrderNumber"].value;
    if (x == "") {
        alert("Order Number must be filled out");
    }
    else {
        document.getElementById("orders").innerHTML = document.getElementById("orders").innerHTML + document.forms["orderForm"]["fOrderNumber"].value + ", ";
    }

}

function processShipment() {
    $.ajax({
        url: "/web/shipping.php",
        method: "GET",
        success: function (data) {
            selectedOrders = order_selection(data, document.getElementById("orders").innerHTML);
            add_address_split(selectedOrders);
            generate_csv(selectedOrders);
        }
    })

}

function order_selection(data, selection) {
    selectedOrders = [];
    selection = selection.split(", ")
    for (let i = 0; i < data.length; i++) {
        for (let j = 0; j < selection.length-1; j++) {
            if (data[i].order_number.includes(selection[j])) {
                selectedOrders.push(data[i]);
            }
        }
    }
    return selectedOrders;
}

function add_address_split(data) {

    for (let i = 0; i < data.length; i++) {
        split_address = address_split(data[i].address);
        data[i] = Object.assign(data[i], split_address);
    }
    return data
}

function address_split(addr) {
    nameLine = addr.split(", ");
    cityState = nameLine[2];
    cityState = cityState.split(" ");
    var address = {};
    address.building_name = nameLine[0];
    address.line1 = nameLine[1];
    address.city = cityState[0];
    address.state = cityState[1];
    address.zip = cityState[2];
    address.country = "US";
    return address
}

function generate_csv(data) {
    unused = "";
    charLimit = 35;
    csv = [];
    for (let i = 0; i < data.length; i++) {
        csv_temp =
            [
                data[i].order_number.substring(0, charLimit),
                (data[i].name + ": " + data[i].building_name).substring(0, charLimit),
                data[i].country,
                data[i].line1,
                unused,
                unused,
                data[i].city,
                data[i].state,
                data[i].zip,
                unused,
                unused,
                unused,
                unused,
                "2",
                unused,
                "20",
                unused,
                unused,
                unused,
                unused,
                unused,
                unused,
                unused,
                unused,
                "03",
                unused,
                unused,
                unused,
                unused,
                unused,
                unused,
                unused,
                unused,
                unused,
                unused,
                "sample@email.com",
                "1"
            ];
        csv.push(csv_temp);
    }
    console.log(csv)
    //https://stackoverflow.com/a/14966131
    let csvContent = "data:text/csv;charset=utf-8,"
        + csv.map(e => e.join(",")).join("\n");
    var encodedUri = encodeURI(csvContent);
    window.open(encodedUri);

}