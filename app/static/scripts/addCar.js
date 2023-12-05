function submitCarForm(add, id = '') {
    const carTabs = document.getElementById('carTabs');
    const activeTab = carTabs.__x.$data.tab;
    if (activeTab === "fullDetails") {
        if (add)
            var button = document.getElementById('fullsubmitadd');
        else
            var button = document.getElementById('fullsubmitedit' + id);
        button.click()
    }
    else {
        if (add)
            var button = document.getElementById('vinsubmitadd');
        else
            var button = document.getElementById('vinsubmitedit' + id);
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

function closeCarEditing(id) {
    const carEditing = document.getElementById("carEditing" + id);
    carEditing.classList.add("hidden");
}
function openCarEditing(id) {
    const carEditing = document.getElementById("carEditing" + id);
    carEditing.classList.remove("hidden");
}