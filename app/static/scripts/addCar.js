// script for add car form
document.addEventListener("DOMContentLoaded", function () {

});

function submitCarForm() {
    const carTabs = document.getElementById('carTabs');
    const activeTab = carTabs.__x.$data.tab;
    if (activeTab === "fullDetails") {
        console.log("this tab");
    }
    else {
        console.log("other tab");
    }
}

function closeCarModal() {
    const carModal = document.getElementById("carModal");
    carModal.classList.add("hidden");
}
function openCarModal() {
    const carModal = document.getElementById("carModal");
    carModal.classList.remove("hidden");
}