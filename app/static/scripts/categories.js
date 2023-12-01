document.addEventListener("DOMContentLoaded", function () {
    const showCategories = document.getElementById("showCategories");
    const categoryNav = document.getElementById("categoryNav");
    var switchNav = true;
    // const categoryNav = document.getElementById("categoryNav");
    showCategories.addEventListener("click", function () {
        if (!switchNav) {
            console.log("hide");
            switchNav = !switchNav;
            categoryNav.classList.add("slideOut");
            showCategories.classList.add("slideOut");
            showCategories.children[0].classList.remove("hidden")
            showCategories.children[1].classList.add("hidden")
            showCategories.style.backgroundColor = "#21A4D8";
        }
        else {
            console.log("show");
            switchNav = !switchNav;
            categoryNav.classList.remove("slideOut");
            showCategories.classList.remove("slideOut");
            showCategories.children[0].classList.add("hidden")
            showCategories.children[1].classList.remove("hidden")
            showCategories.style.backgroundColor = "red";
        }
    });
});