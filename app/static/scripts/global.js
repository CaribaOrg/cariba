// This script contains action that can be triggered from any route

function addToCart(product_id) {
    // Add a product to the cart
    fetch(`/add_to_cart/${product_id}`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update the cart count on the page
                document.getElementById('cart_items_count').innerText = `${data.cart_count}`;
            } else {
                console.error('Failed to add item to cart.');
            }
        })
        .catch(error => {
            console.error('Error adding item to cart:', error);
        });
}