document.addEventListener("DOMContentLoaded", function () {
    var updateBtns = document.getElementsByClassName('update-cart');

    for (var i = 0; i < updateBtns.length; i++) {
        updateBtns[i].addEventListener('click', function (event) {
            event.preventDefault();
            var productId = this.dataset.product;
            var action = this.dataset.action;

            if (typeof user !== "undefined") {
                if (user === "AnonymousUser") {
                    console.log("Not logged in");
                } else {
                    updateUserOrder(productId, action);
                }
            } else {
                console.log("USER variable is undefined.");
            }
        });
    }

    function updateUserOrder(productId, action) {
        var url = 'update_item/';

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'productId': productId, 'action': action })
        })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            var quantityElement = document.getElementById('quantity-value-' + productId);
            var totalPriceElement = document.getElementById('total-price-' + productId);

            // Update the quantity element for the productId
            quantityElement.textContent = 'X' + data.quantity;

            // Update the cart total element on the page
            document.getElementById('cart-total').textContent = data.cart_total;

            // Update the total price for the specific item
            totalPriceElement.textContent = '$' + data.total_price.toFixed(2);

            // Reload the page while preserving the Y location
            window.scrollTo(0, window.scrollY);
        });
    }
});
