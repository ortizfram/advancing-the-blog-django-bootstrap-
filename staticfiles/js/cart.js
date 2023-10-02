        document.addEventListener("DOMContentLoaded", function () {
            console.log('JavaScript loaded'); // for debugging

            var updateBtns = document.getElementsByClassName('update-cart');
            var cartTotalElement = document.getElementById('cart-total');
            var cartItemsElement = document.getElementById('cart-items');

<<<<<<< HEAD
            // Function to update the cart total
            function updateCartTotal() {
                console.log('Updating cart total...'); // Add this line for debugging
                var url = "update_item/";

                fetch(url, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken,
                    }
                })
                .then((response) => {
                    return response.json();
                })
                .then((data) => {
                    console.log('AJAX response data:', data); // Add this line for debugging
                    // Before assignment
                    console.log('Before assignment:', cartTotalElement.textContent);
                    // Update the cart total element on the page
                    cartTotalElement.textContent = data.cart_total.toFixed(2);
                    cartItemsElement.textContent = data.cart_quantity; // Add this line to update cart items count
                    console.log('After assignment:', cartTotalElement.textContent); // debugging
                });
            }

            // Call the function to update the cart total when the page loads
=======
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
>>>>>>> c08da420a6f263369e8e570f166a95ef14213fc5
            updateCartTotal();

            for (var i = 0; i < updateBtns.length; i++) {
                updateBtns[i].addEventListener('click', function (event) {
                    event.preventDefault();
                    var productId = this.dataset.product;
                    var action = this.dataset.action;

                    console.log('Button clicked:', productId, action);

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
