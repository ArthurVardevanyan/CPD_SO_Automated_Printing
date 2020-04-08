window.onload = function () {
    $("#submit").click(function () {
        Form();
        return false;
    });
    $("#package").click(function () {
        document.getElementById("orders").innerHTML = document.getElementById("orders").innerHTML + "<br><br>";
        return false;
    });
    $("#clear").click(function () {
        document.getElementById("orders").innerHTML = "";
        document.getElementById("validation").innerHTML = ""
        return false;
    });
    $("#validate").click(function () {

        validateShipment();
        return false;
    });
    $("#csv").click(function () {
        processShipment();
    });
    $(function () {
        //https://stackoverflow.com/a/2215467
        $("form").submit(function () { return false; });
    });
    var input = document.getElementById("fOrderNumber");

    input.addEventListener("keyup", function (event) {
        https://www.w3schools.com/howto/howto_js_trigger_button_enter.asp
        // Number 13 is the "Enter" key on the keyboard
        if (event.keyCode === 13) {
            // Cancel the default action, if needed
            event.preventDefault();
            // Trigger the button element with a click
            document.getElementById("submit").click();
            return false;

        }
    });


};

function Form() {
    var x = document.forms["orderForm"]["fOrderNumber"].value;
    if (x == "") {
        alert("Order Number must be filled out");
    }
    else {
        document.getElementById("orders").innerHTML = document.getElementById("orders").innerHTML + document.forms["orderForm"]["fOrderNumber"].value + ", ";
        document.forms["orderForm"]["fOrderNumber"].value = "";
    }

}

function validateShipment() {
    $.ajax({
        url: "/web/shipping.php",
        method: "GET",
        success: function (data) {
            shipment_validation(data);
        }
    })

}

function processShipment() {
    $.ajax({
        url: "/web/shipping.php",
        method: "GET",
        success: function (data) {
            selectedPackages = shipment_validation(data);
            if (!selectedPackages) { return }
            selectedPackages = add_address_split(selectedPackages);
            selectedPackages = orderToPackageMerge(selectedPackages);
            generate_csv(selectedPackages);
        }
    })

}
function shipment_validation(data) {
    flag = true;
    document.getElementById("validation").innerHTML = ""
    selectedPackages = order_selection(data, document.getElementById("orders").innerHTML);
    for (let i = 0; i < selectedPackages.length; i++) {

        val = validate_package(selectedPackages[i])
        if (val[0]) {

            document.getElementById("validation").innerHTML = document.getElementById("validation").innerHTML + "<p style='color:green'>Validation Successful</p>";
        }
        else {
            document.getElementById("validation").innerHTML = document.getElementById("validation").innerHTML + "<p style='color:red'>Validation Failed: " + val[1] + "</p>";
            flag = false;
        }

    }
    if (flag) {
        return selectedPackages
    }
    else { return flag }
}
function order_selection(data, selection) {
    selectedPackages = [];
    selection = selection.split("<br>")
    selections = []
    for (let i = 0; i < selection.length; i++) {
        selections.push(selection[i].split(", "));
    }
    for (let j = 0; j < selections.length; j++) {
        selectedPackage = [];
        for (let k = 0; k < selections[j].length - 1; k++) {
            for (let i = 0; i < data.length; i++) {
                if (data[i].order_number.includes(selections[j][k])) {
                    selectedPackage.push(JSON.parse(JSON.stringify(data[i])));
                }
            }
        }
        if (selectedPackage.length > 0) {
            selectedPackages.push(selectedPackage);
        }
    }
    return selectedPackages;
}

function validate_package(package) {
    for (let i = 1; i < package.length; i++) {
        if (package[i].address !== package[0].address) {
            return [false, "Teacher MisMatch"];
        }
    }
    return [true];

}

function add_address_split(data) {
    for (let i = 0; i < data.length; i++) {

        for (let j = 0; j < data[i].length; j++) {
            split_address = address_split(data[i][j].address);
            data[i][j] = Object.assign(data[i][j], split_address);
        }
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

function orderToPackageMerge(data) {
    packages = []
    for (let i = 0; i < data.length; i++) {
        orders = ""
        for (let j = 0; j < data[i].length; j++) {
            orders = orders + (data[i][j].order_number).split("-")[0] + ":";
        }
        data[i][0].order_number = orders;
        packages.push(data[i][0]);
    }
    return packages
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
    //https://stackoverflow.com/a/14966131
    let csvContent = "data:text/csv;charset=utf-8,"
        + csv.map(e => e.join(",")).join("\n");
    var encodedUri = encodeURI(csvContent);
    window.open(encodedUri);

}