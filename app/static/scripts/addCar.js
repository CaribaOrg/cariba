function submitCarForm() {
    const carTabs = document.getElementById('carTabs');
    const activeTab = carTabs.__x.$data.tab;
    if (activeTab === "fullDetails") {
        var button = document.getElementById('fullsubmit');
        button.click()
    }
    else {
        var button = document.getElementById('vinsubmit');
        button.click()
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