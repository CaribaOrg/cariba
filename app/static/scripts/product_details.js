document.addEventListener("DOMContentLoaded", function () {
    // change product details big image
    const big_image = document.getElementById('big_image');
    const imgs_holder = document.getElementById('imgs_holder')
    var lil_images = imgs_holder.children;
    for (var i = 0; i < lil_images.length; i++) {
        lil_images[i].addEventListener('mouseover', function () {
            big_image.src = this.src;
        });
    }
});

function buyNow(product_id) {
    const quantityCount = document.getElementById("quantityCount");
    const quantityValue = parseInt(quantityCount.value);
    fetch(`/add_to_cart/${product_id}/${quantityValue}`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update the cart count
                window.location.href = '/myCart';
            } else {
                console.error('Failed to add item to cart.');
            }
        })
        .catch(error => {
            console.error('Error adding item to cart:', error);
        });
}
function addToCart2(product_id, addToCartButton) {
    const quantityCount = document.getElementById("quantityCount");
    const quantityValue = parseInt(quantityCount.value);
    fetch(`/add_to_cart/${product_id}/${quantityValue}`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update the cart count
                document.getElementById('cart_items_count').innerText = `${data.cart_count}`;
                addToCartButton.classList.add("hidden");

            } else {
                console.error('Failed to add item to cart.');
            }
        })
        .catch(error => {
            console.error('Error adding item to cart:', error);
        });
}