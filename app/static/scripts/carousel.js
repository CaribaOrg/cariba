var cont = 0;
let xx;
function loopSlider() {
    xx = setInterval(function () {
        switch (cont) {
            case 0: {
                $("#slider-1").fadeOut(400);
                $("#slider-2").delay(400).fadeIn(400);
                $("#sButton1").removeClass("bg-primary");
                $("#sButton2").addClass("bg-primary");
                cont = 1;

                break;
            }
            case 1: {
                $("#slider-2").fadeOut(400);
                $("#slider-1").delay(400).fadeIn(400);
                $("#sButton2").removeClass("bg-primary");
                $("#sButton1").addClass("bg-primary");

                cont = 0;

                break;
            }
        }
    }, 8000);
}

function reinitLoop(time) {
    clearInterval(xx);
    setTimeout(loopSlider(), time);
}

function sliderButton1() {
    $("#slider-2").fadeOut(400);
    $("#slider-1").delay(400).fadeIn(400);
    $("#sButton2").removeClass("bg-primary");
    $("#sButton1").addClass("bg-primary");
    reinitLoop(4000);
    cont = 0;
}

function sliderButton2() {
    $("#slider-1").fadeOut(400);
    $("#slider-2").delay(400).fadeIn(400);
    $("#sButton1").removeClass("bg-primary");
    $("#sButton2").addClass("bg-primary");
    reinitLoop(4000);
    cont = 1;
}

document.addEventListener("DOMContentLoaded", function () {
    $("#slider-2").hide();
    $("#sButton1").addClass("bg-primary");

    loopSlider();
});
