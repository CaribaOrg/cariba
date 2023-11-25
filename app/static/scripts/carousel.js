document.addEventListener("DOMContentLoaded", function () {
    // Get the carousel element
    const carousel = document.getElementById("carouselExampleCaptions");

    // Get the carousel items and indicators
    const items = carousel.querySelectorAll("[data-te-carousel-item]");
    const indicators = carousel.querySelectorAll("[data-te-carousel-indicators] button");

    // Get the previous and next buttons
    const prevButton = carousel.querySelector("[data-te-slide='prev']");
    const nextButton = carousel.querySelector("[data-te-slide='next']");

    // Set initial index
    let currentIndex = 0;

    // Function to show the current slide
    function showCurrentSlide() {
        items.forEach((item, index) => {
            if (index === currentIndex) {
                item.classList.add("transition-transform", "ease-in-out", "duration-600");
                item.style.transform = "translateX(0)";
            } else {
                item.classList.remove("transition-transform", "ease-in-out", "duration-600");
                item.style.transform = `translateX(${100 * (index - currentIndex)}%)`;
            }
        });

        // Update the indicators
        indicators.forEach((indicator, index) => {
            indicator.setAttribute("aria-current", index === currentIndex ? "true" : "false");
        });
    }

    // Function to show the next slide
    function showNextSlide() {
        currentIndex = (currentIndex + 1) % items.length;
        showCurrentSlide();
    }

    // Function to show the previous slide
    function showPrevSlide() {
        currentIndex = (currentIndex - 1 + items.length) % items.length;
        showCurrentSlide();
    }

    // Event listeners for next and previous buttons
    prevButton.addEventListener("click", showPrevSlide);
    nextButton.addEventListener("click", showNextSlide);

    // Event listeners for indicator buttons
    indicators.forEach((indicator, index) => {
        indicator.addEventListener("click", function () {
            currentIndex = index;
            showCurrentSlide();
        });
    });

    // Show the initial slide
    showCurrentSlide();
});
