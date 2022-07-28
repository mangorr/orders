$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#order_id").val(res.id);
        $("#customer_id").val(res.customer_id);
        $("#tracking_id").val(res.tracking_id);
        $("#status").val(res.status);
        $("#created_time").val(res.created_time);
        /*
        if (res.available == "CREATED") {
            $("#status").val("CREATED");
        } else {
            $("#status").val("false");
        }
        */
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#customer_id").val("");
        $("#tracking_id").val("");
        $("#status").val("PLACED");
        $("#created_time").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").val("");
        $("#flash_message").val(message);
    }

    // ****************************************
    // Create an Order
    // ****************************************

    $("#create-btn").click(function () {

        var customer_id = $("#customer_id").val();
        var tracking_id = $("#tracking_id").val();
        var status = $("#status").val();//== "CREATED";

        var data = {
            "customer_id": customer_id,
            "tracking_id": tracking_id,
            "status": status,
        };

        $("#flash_message").val("");

        var ajax = $.ajax({
            type: "POST",
            url: "/orders",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function (res) {
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update an Order
    // ****************************************

    $("#update-btn").click(function () {

        var order_id = $("#order_id").val();
        var customer_id = $("#customer_id").val();
        var tracking_id = $("#tracking_id").val();
        var status = $("#status").val();

        var data = {
            "id": order_id,
            "customer_id": customer_id,
            "tracking_id": tracking_id,
            "status": status
        };

        $("#flash_message").val("");

        var ajax = $.ajax({
            type: "PUT",
            url: `/orders/${order_id}`,
            contentType: "application/json",
            data: JSON.stringify(data)
        })

        ajax.done(function (res) {
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve an Order
    // ****************************************

    $("#retrieve-btn").click(function () {

        $("#flash_message").val("");
        var order_id = $("#order_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: `/orders/${order_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function (res) {
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete an Order
    // ****************************************

    $("#delete-btn").click(function () {
        $("#flash_message").val("");

        var order_id = $("#order_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: `/orders/${order_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function (res) {
            clear_form_data()
            flash_message("Order has been Deleted!")
        });

        ajax.fail(function (res) {
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Cancel a Order
    // ****************************************

    $("#cancel-btn").click(function () {
        $("#flash_message").val("");

        var order_id = $("#order_id").val();

        var ajax = $.ajax({
            type: "PUT",
            url: `/orders/${order_id}/cancel`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function (res) {
            clear_form_data()
            flash_message("Order has been CANCELLED!")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#order_id").val("");
        $("#flash_message").val("");
        clear_form_data()
    });

    // ****************************************
    // List all Orders
    // ****************************************

    // $("#listall-btn").click(function () {

    //     var ajax = $.ajax({
    //         type: "GET",
    //         url: "/api/orders",
    //         data: ''
    //     })

    //     ajax.done(function (res) {
    //         //alert(res.toSource())
    //         $("#search_results").empty();
    //         $("#search_results").append('<table class="table-striped" cellpadding="10">');
    //         var header = '<tr>'
    //         header += '<th style="width:10%">ID</th>'
    //         header += '<th style="width:40%">customer_id</th>'
    //         header += '<th style="width:40%">tracking_id</th>'
    //         header += '<th style="width:10%">status</th></tr>'
    //         $("#search_results").append(header);
    //         var firstOrder = "";
    //         for (var i = 0; i < res.length; i++) {
    //             var order = res[i];
    //             var row = "<tr><td>" + order.id + "</td><td>" + order.customer_id + "</td><td>" + order.tracking_id + "</td><td>" + order.status + "</td></tr>";
    //             $("#search_results").append(row);
    //             if (i == 0) {
    //                 firstOrder = order;
    //             }
    //         }

    //         $("#search_results").append('</table>');

    //         // copy the first result to the form
    //         if (firstOrder != "") {
    //             update_form_data(firstOrder)
    //         }

    //         flash_message("Success")
    //     });

    //     ajax.fail(function (res) {
    //         flash_message(res.responseJSON.message)
    //     });

    // });

    // // ****************************************
    // // Search Query String
    // // ****************************************

    // $("#search-btn").click(function () {

    //     var ele = document.getElementsByName('query_option');
    //     var queryString = ""

    //     var data={}
    //     if (ele[0].checked) {
    //         data["customer_id"] = $("#query").val();
    //     }else if(ele[1].checked) {
    //         data["status"] = $("#query").val();
    //     }else if(ele[2].checked){
    //         data["product_id"] = $("#query").val();
    //     }else{
    //         flash_message("Please select one of the query type!")
    //         return 
    //     }

    //     var ajax = $.ajax({
    //         type: "GET",
    //         url: "/orders",
    //         data: JSON.stringify(data)
    //     })

    //     ajax.done(function (res) {
    //         //alert(res.toSource())
    //         $("#search_results").empty();
    //         $("#search_results").append('<table class="table-striped" cellpadding="10">');
    //         var header = '<tr>'
    //         header += '<th style="width:10%">ID</th>'
    //         header += '<th style="width:40%">customer_id</th>'
    //         header += '<th style="width:40%">tracking_id</th>'
    //         header += '<th style="width:10%">status</th></tr>'
    //         $("#search_results").append(header);
    //         var firstOrder = "";
    //         for (var i = 0; i < res.length; i++) {
    //             var order = res[i];
    //             var row = "<tr><td>" + order.id + "</td><td>" + order.customer_id + "</td><td>" + order.tracking_id + "</td><td>" + order.status + "</td></tr>";
    //             $("#search_results").append(row);
    //             if (i == 0) {
    //                 firstOrder = order;
    //             }
    //         }

    //         $("#search_results").append('</table>');

    //         // copy the first result to the form
    //         if (firstOrder != "") {
    //             update_form_data(firstOrder)
    //         }

    //         flash_message("Success")
    //     });

    //     ajax.fail(function (res) {
    //         flash_message(res.responseJSON.message)
    //     });

    // });


    // ****************************************************
    // O R D E R   I T E M S
    // ****************************************************

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_item_form_data(res) {
        $("#item_id").val(res.id);
        $("#item_order_id").val(res.order_id);
        $("#product_id").val(res.product_id);
        $("#quantity").val(res.quantity);
        $("#price").val(res.price);
    }

    /// Clears all form fields
    function clear_item_form_data() {
        $("#item_order_id").val("");
        $("#product_id").val("");
        $("#quantity").val("");
        $("#price").val("");
        
    }

    // Updates the flash message area
    function flash_item_message(message) {
        $("#flash_message_item").val("");
        $("#flash_message_item").val(message);
    }

    // ****************************************
    // Create an Item
    // ****************************************

    $("#create-item-btn").click(function () {
        $("#flash_message_item").val("");

        var order_id = $("#item_order_id").val();
        var product_id = $("#product_id").val();
        var quantity = $("#quantity").val();
        var price = $("#price").val();

        var data = {
            "order_id": order_id,
            "product_id": product_id,
            "quantity": quantity,
            "price": price
        };

        var ajax = $.ajax({
            type: "POST",
            url: `/orders/${order_id}/items`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function (res) {
            update_item_form_data(res)
            flash_item_message("Success")
        });

        ajax.fail(function (res) {
            flash_item_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update an Item
    // ****************************************

    $("#update-item-btn").click(function () {
        $("#flash_message_item").val("");

        var item_id = $("#item_id").val();
        var order_id = $("#item_order_id").val();
        var product_id = $("#product_id").val();
        var quantity = $("#quantity").val();
        var price = $("#price").val();

        var data = {
            "id": item_id,
            "order_id": order_id,
            "product_id": product_id,
            "quantity": quantity,
            "price": price,
        };

        var ajax = $.ajax({
            type: "PUT",
            url: `/orders/${order_id}/items/${item_id}`,
            contentType: "application/json",
            data: JSON.stringify(data)
        })

        ajax.done(function (res) {
            update_item_form_data(res)
            flash_item_message("Success")
        });

        ajax.fail(function (res) {
            flash_item_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve an Item
    // ****************************************

    $("#retrieve-item-btn").click(function () {
        $("#flash_message_item").val("");

        var item_id = $("#item_id").val();
        var order_id = $("#item_order_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: `/orders/${order_id}/items/${item_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function (res) {
            //alert(res.toSource())
            update_item_form_data(res)
            flash_item_message("Success")
        });

        ajax.fail(function (res) {
            clear_item_form_data()
            flash_item_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete an Item
    // ****************************************

    $("#delete-item-btn").click(function () {
        $("#flash_message_item").val("");

        var item_id = $("#item_id").val();
        var order_id = $("#item_order_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: `/orders/${order_id}/items/${item_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function (res) {
            clear_item_form_data()
            flash_item_message("Item has been Deleted!")
        });

        ajax.fail(function (res) {
            flash_item_message("Server error!")
        });
    });



    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-item-btn").click(function () {
        $("#item_id").val("");
        $('#flash_message_item').val("");
        clear_item_form_data()
    });

    // ****************************************
    // List all Items
    // ****************************************

    $("#listall-item-btn").click(function () {

        var order_id = $("#orderid").val();
        if (order_id != "") {
            var u = "/api/orders/" + order_id + "/items";
        }
        else {
            var u = "/api/items";
        }


        var ajax = $.ajax({
            type: "GET",
            url: u,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function (res) {
            //alert(res.toSource())
            $("#search_item_results").empty();
            $("#search_item_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th style="width:10%">Item ID</th>'
            header += '<th style="width:30%">Product_id</th>'
            header += '<th style="width:30%">quantity</th>'
            header += '<th style="width:10%">Price</th>'
            header += '<th style="width:20%">Order ID</th></tr>'

            $("#search_item_results").append(header);
            var firstOrder = "";
            for (var i = 0; i < res.length; i++) {
                var order = res[i];
                var row = "<tr><td>" + order.id + "</td><td>" + order.product_id + "</td><td>" + order.quantity + "</td><td>" + order.price + "</td><td>" + order.order_id + "</td></tr>";
                $("#search_item_results").append(row);
                if (i == 0) {
                    firstOrder = order;
                }
            }

            $("#search_item_results").append('</table>');

            // copy the first result to the form
            if (firstOrder != "") {
                update_item_form_data(firstOrder)
            }

            flash_item_message("Success")
        });

        ajax.fail(function (res) {
            flash_item_message(res.responseJSON.message)
        });

    });

})