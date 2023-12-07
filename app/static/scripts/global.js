// This script contains action that can be triggered from any route

function addToCart(product_id, buttonCaller) {
    var addImg = buttonCaller.children[0];
    var removeImg = buttonCaller.children[1];
    if (!addImg.classList.contains("hidden")) {
        // Add a product to the cart
        console.log(product_id)
        fetch(`/add_to_cart/${product_id}/1`, { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update the cart count on the page and the add img to remove img
                    removeImg.classList.remove("hidden");
                    addImg.classList.add("hidden");
                    document.getElementById('cart_items_count').innerText = `${data.cart_count}`;

                } else {
                    console.error('Failed to add item to cart.');
                }
            })
            .catch(error => {
                console.error('Error adding item to cart:', error);
            });
    }
    else {
        // Remove a product from the cart
        fetch(`/remove_from_cart/${product_id}/1`, { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update the cart count on the page
                    addImg.classList.remove("hidden");
                    removeImg.classList.add("hidden");
                    document.getElementById('cart_items_count').innerText = `${data.cart_count}`;

                } else {
                    console.error('Failed to add item to cart.');
                }
            })
            .catch(error => {
                console.error('Error adding item to cart:', error);
            });
    }
}

function IncreaseCartItem(product_id, inCart) {
    // Add a product to the cart
    if (inCart) {
        fetch(`/add_to_cart/${product_id}/1`, { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update the cart count
                    location.reload();
                } else {
                    console.error('Failed to add item to cart.');
                }
            })
            .catch(error => {
                console.error('Error adding item to cart:', error);
            });
    }
    else {
        const quantityCount = document.getElementById("quantityCount");
        if (quantityCount.value < parseInt(quantityCount.max)) {
            quantityCount.value = parseInt(quantityCount.value) + 1;
        }
    }

}

function decreaseProductQuantity(product_price) {
    const quantityCount = document.getElementById("quantityCount");
    if (quantityCount.value >= 2) {
        quantityCount.value = parseInt(quantityCount.value) - 1;
    }
}

function removeFromCart(product_id, item_quantity, buttonCaller, inCart) {
    fetch(`/remove_from_cart/${product_id}/${item_quantity}`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update the cart count on the page
                const cartItem = buttonCaller.parentNode.parentNode.parentNode.parentNode
                cartItem.classList.add("hidden");
                if (inCart) {
                    location.reload();
                } else {
                    document.getElementById('cart_items_count').innerText = `${data.cart_count}`;
                }
                // document.getElementById('cart_items_count').innerText = `${data.cart_count}`;
            } else {
                console.error('Failed to add item to cart.');
            }
        })
        .catch(error => {
            console.error('Error adding item to cart:', error);
        });
}

// subscribe to the newsletter
function newsletterForm() {
    var email = document.getElementById('newsletter_email').value;

    // Create an XMLHttpRequest object
    var xhr = new XMLHttpRequest();

    xhr.open('POST', '/subscribe', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

    // Define the callback function when the request is complete
    xhr.onload = function () {
        if (xhr.status === 200) {
            // Successful response, handle it accordingly
            console.log(xhr.responseText);
            // You might want to update the UI or show a success message here
        } else {
            // Request failed, handle errors
            console.error('Form submission failed');
        }
    };

    // Prepare the data to be sent (in this case, a simple email parameter)
    var formData = 'email=' + encodeURIComponent(email);

    // Send the request
    xhr.send(formData);
}

// close flash
function closeFlashMessage(button) {
    button.closest('.flash-message').remove();
}

// copy to clipboard
function copyToClipboard() {
    // Get the text content of the span
    var textToCopy = document.getElementById('orderID').innerText;

    // Create a temporary textarea element
    var tempInput = document.createElement('textarea');

    // Set the value of the temporary textarea to the text content
    tempInput.value = textToCopy;

    // Append the temporary textarea to the document
    document.body.appendChild(tempInput);

    // Select the text in the textarea
    tempInput.select();
    tempInput.setSelectionRange(0, 99999); /* For mobile devices */

    // Copy the text inside the text field
    navigator.clipboard.writeText(tempInput.value);

    // Remove the temporary textarea
    document.body.removeChild(tempInput);

    var copyButton = document.getElementById("copyBtn");
    copyButton.children[0].classList.add("hidden")
    copyButton.children[1].classList.remove("hidden")
    setTimeout(function () {
        copyButton.children[0].classList.remove("hidden")
        copyButton.children[1].classList.add("hidden")
    }, 2000); // Reset button text after 2 seconds (adjust as needed)
}

// messaging stuff
function set_message_count(n) {
    const count = document.getElementById('message_count');
    count.innerText = n;
    count.style.visibility = n ? 'visible' : 'hidden';
  }