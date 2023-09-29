document.addEventListener("DOMContentLoaded", function () {
    console.log('JavaScript loaded'); // for debugging

    var updateBtns = document.getElementsByClassName('update-cart');
    var cartTotalElement = document.getElementById('cart-total');
    var cartItemsElement = document.getElementById('cart-items');

    // Function to update the cart total
    function updateCartTotal() {
        console.log('Updating cart total...');
        var url = "update_item/";

    
        fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            }
        })
        .then((response) => {
            if (!response.ok) {
                console.error('Response not ok:', response.status, response.statusText);
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then((data) => {
            console.log('AJAX response data:', data);
            // ... rest of your code
        })
        .catch((error) => {
            console.error('Fetch error:', error);
        });
    }

    // Call the function to update the cart total when the page loads
    updateCartTotal();

    for (var i = 0; i < updateBtns.length; i++) {
        updateBtns[i].addEventListener('click', function (event) {
            event.preventDefault();
            var productId = this.dataset.product;
            var action = this.dataset.action;
            console.log('productId:', productId,"action:", action);

            console.log("USER:", user)
            if (user === "AnonymousUser") {
                addCookieItem()
            } else {
                updateUserOrder(productId, action);
            }
        });
    }

    function addCookieItem(productId, action){
        console.log("Not logged in..");

        if(action == 'add'){
            if(cart[productId] == undefined){
                cart[productId] = {'quantity':1}
            }else{
                cart[productId]['quantity'] += 1
            }
        }

        if(action == 'remove'){
            cart[productId]['quantity'] -= 1

            if(cart[productId]['quantity'] <= 0){
                console.log('Remove Item')
                delete cart[productId]
            }
        }
        console.log("Cart:", cart)
        document.cookie = 'cart'+ JSONstringify(cart) + ";domain=;path=/"
        location.reload()
    }


    function updateUserOrder(productId, action) {
        console.log("User is logged in, sending data...")

        var url = "update_item/";

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

            // Update the total price for the specific item
            totalPriceElement.textContent =  data.item_total_price.toFixed(2);

            // Call the function to update the cart total when an item is updated
            updateCartTotal();
            location.reload();

            // Check if the quantity is 0, and if so, trigger a fast refresh
            if (data.quantity === 0) {
                location.reload();
            }
        });
    }
});
