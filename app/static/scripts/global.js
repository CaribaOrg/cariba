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

function IncreaseCartItem(product_id, product_price, inCart) {
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