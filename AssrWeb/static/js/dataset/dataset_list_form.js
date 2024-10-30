var selected = []

function checkbox_handler(e) {
    const checkbox = e.target
    const pk = checkbox.dataset.pk

    if (checkbox.checked && !(selected.includes(pk))) {
        selected.push(pk)
    }
    else if (!checkbox.checked && selected.includes(pk)) {
        selected = selected.filter(x => x != pk)
    }
}

function main() {
    const checkboxes = document.getElementsByClassName("large-checkbox")

    for (var c of checkboxes) {
        c.addEventListener("input", checkbox_handler)
    }
}

document.addEventListener("DOMContentLoaded", main)

export default selected