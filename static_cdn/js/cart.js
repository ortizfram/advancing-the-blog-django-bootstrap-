document.addEventListener("DOMContentLoaded", function () {
    console.log('JavaScript loaded'); // for debugging

    // Initialize formData with empty values
    var formData = {
        form: {
            name: null,
            email: null,
            total: null,
        },
        shipping: {
            address: null,
            state: null,
            country: null,
            zipcode: null,
        },
    };

    // Function to submit the form data
    function submitFormData(formData) {
        console.log("submitFormData called");
        var url = "{% url 'store:process_order' %}";
        var csrftoken = getCookie("csrftoken");
        console.log("CSRF Token:", csrftoken);

        // Before sending the data
        console.log(formData);

        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken,
            },
            body: JSON.stringify(formData),
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            console.log("Success:", data);
            if (data.message) {
                alert(data.message);
            }
            window.location.href = "{% url 'store:store' %}";
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("An error occurred while processing your request.");
        });
    }

    var user = "{{ request.user }}";
    var paymentButton = document.getElementById("make-payment");
    var emailInput = document.querySelector('[name="email"]');

    if (user !== "AnonymousUser") {
        // User is logged in, hide user-info and show shipping-info
        emailInput.style.display = "none";
    }

    var formFields = document.querySelectorAll(
        'input[type="text"], input[type="email"]'
    );

    // Attach input event listeners to update the form
    formFields.forEach(function (field) {
        field.addEventListener("input", function () {
            paymentButton.disabled = false;
        });
    });

    // Event listener for form submission
    document.getElementById("form").addEventListener("submit", function (e) {
        e.preventDefault();

        // Update formData with the form data
        formData.form.name = document.querySelector('[name="name"]').value;
        formData.form.email = document.querySelector('[name="email"]').value;

        // Extract the total from totalElement
        formData.form.total = totalElement.textContent;

        formData.shipping.address = document.querySelector('[name="address"]').value;
        formData.shipping.state = document.querySelector('[name="state"]').value;
        formData.shipping.country = document.querySelector('[name="country"]').value;
        formData.shipping.zipcode = document.querySelector('[name="zipcode"]').value;

        // Call submitFormData with the updated formData
        submitFormData(formData);
    });

    // Event listener for the "Make payment" button
    paymentButton.addEventListener("click", function (e) {
        // Pass formData to submitFormData
        submitFormData(formData);
    });

});
