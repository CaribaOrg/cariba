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