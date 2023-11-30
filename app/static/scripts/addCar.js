// script for add car form
document.addEventListener("DOMContentLoaded", function () {

});

function submitCarForm() {
    const activeTab = Alpine.data('component-name').tab;
    if (activeTab === "fullDetails") {

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