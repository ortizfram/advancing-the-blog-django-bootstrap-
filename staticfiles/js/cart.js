document.addEventListener("DOMContentLoaded", function () {
    // Get all elements with the class 'update-cart' (Add buttons)
    var updateBtns = document.getElementsByClassName('update-cart');

    // Loop through each button and add a click event listener
    for (var i = 0; i < updateBtns.length; i++) {
        updateBtns[i].addEventListener('click', function () {
            var productId = this.dataset.product;
            var action = this.dataset.action;
            console.log("-> update-cart:", "productId", productId, "Action:", action);

            // Check if the user variable is defined (loaded in base.html)
            if (typeof user !== "undefined") {
                console.log("USER:", user);
                if (user === "AnonymousUser") {
                    console.log("# Not logged in");
                } else {
                    updateUserOrder(productId, action);
                }
            } else {
                console.log("USER variable is undefined.");
            }
        });
    }

    // console.log("Script loaded: update-cart"); // Debugging

    function updateUserOrder(productId, action) {
        // console.log("User: ", user, "authenticated, sending data...");

        var url = 'update_item/';

        // Send POST request with product ID and action as JSON data
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'productId': productId, 'action': action })
        })

        // Handle the response as JSON
        .then((response) => {
            return response.json();
        })

        .then((data) => {
            console.log("data:", data.message);
        
            var quantityElement = $('#quantity-value-' + productId);
            if (quantityElement.length > 0) {
                quantityElement.text(data.quantity);
            }

            // Update the cart total element on the page
            document.getElementById('cart-total').textContent = data.cart_total;

            // Update the total price for the specific item
            var totalPriceElement = $('#total-price-' + productId);
            if (totalPriceElement.length > 0) {
                totalPriceElement.text('$' + data.total_price.toFixed(2));
            }
        });

        // console.log("Script loaded: updateUserOrder"); // Debugging
    }
});
