var cont = 0;
var intervalId;

function loopSlider() {
    intervalId = setInterval(function () {
        switch (cont) {
            case 0:
                transitionSlides("#slider-1", "#slider-2", "#sButton1", "#sButton2");
                cont = 1;
                break;
            case 1:
                transitionSlides("#slider-2", "#slider-1", "#sButton2", "#sButton1");
                cont = 0;
                break;
        }
    }, 8000);
}

function transitionSlides(fadeOutElem, fadeInElem, removeClassBtn, addClassBtn) {
    $(fadeOutElem).fadeOut(400, function () {
        // Hide the outgoing slide after the fadeOut animation
        $(this).hide();
    });
    $(fadeInElem).delay(400).fadeIn(400);
    $(removeClassBtn).removeClass("bg-primary");
    $(addClassBtn).addClass("bg-primary");
}

function stopSlider() {
    clearInterval(intervalId);
}

function restartSlider() {
    stopSlider();
    loopSlider();
}

function sliderButton(index) {
    if (index === 0 && cont !== 0) {
        transitionSlides("#slider-2", "#slider-1", "#sButton2", "#sButton1");
        cont = 0;
        restartSlider();
    } else if (index === 1 && cont !== 1) {
        transitionSlides("#slider-1", "#slider-2", "#sButton1", "#sButton2");
        cont = 1;
        restartSlider();
    }
}

$(document).ready(function () {
    $("#slider-2").hide();
    $("#sButton1").addClass("bg-primary");

    loopSlider();

    // Pause carousel when the tab is not visible
    $(document).on("visibilitychange", function () {
        if (document.hidden) {
            stopSlider();
        } else {
            restartSlider();
        }
    });

    // Restart the slider when the page gains focus
    $(window).on("focus", function () {
        restartSlider();
    });

    // Pause the slider when the page loses focus
    $(window).on("blur", function () {
        stopSlider();
    });
});