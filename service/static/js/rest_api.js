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
            url: "/api/orders",
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
            url: `/api/orders/${order_id}`,
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
            url: `/api/orders/${order_id}`,
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
            url: `/api/orders/${order_id}`,
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
            url: `/api/orders/${order_id}/cancel`,
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
            url: `/api/orders/${order_id}/items`,
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
            url: `/api/orders/${order_id}/items/${item_id}`,
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
            url: `/api/orders/${order_id}/items/${item_id}`,
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
            url: `/api/orders/${order_id}/items/${item_id}`,
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

    
})