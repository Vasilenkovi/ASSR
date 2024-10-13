function check_rows(e) {
    const current_row = document.getElementById("current-kv-row")

    // tr -> [td] -> input
    const current_row_key = current_row.children[0].children[0]
    const current_row_value = current_row.children[1].children[0]

    if (current_row_key.value && current_row_value.value) {
        current_row.removeAttribute("id")

        const tr = document.createElement("tr")
        tr.id = "current-kv-row"

        for (var i = 0; i < 2; i++) {
            const td = document.createElement("td")
            
            const td_input = document.createElement("input")
            td_input.type = "text"
            td_input.classList.add("kv-inputs")
            td_input.addEventListener("change", check_rows)
            td_input.addEventListener("change", delete_empty)

            td.appendChild(td_input)
            tr.appendChild(td)
        }

        const append_target = document.getElementById("kv-append")
        append_target.appendChild(tr)
    }
}

function delete_empty(e) {
    // tr -> [td] -> input
    // Get row
    const row = e.target.parentElement.parentElement

    if (row.id == "current-kv-row") {
        return
    }

    const current_row_key = row.children[0].children[0]
    const current_row_value = row.children[1].children[0]

    if (!(current_row_key.value || current_row_value.value)) {
        row.remove()
    }
}

function main() {
    const current_row = document.getElementById("current-kv-row")

    // tr -> [td] -> input
    const current_row_key = current_row.children[0].children[0]
    current_row_key.addEventListener("change", check_rows)
    current_row_key.addEventListener("change", delete_empty)

    const current_row_value = current_row.children[1].children[0]
    current_row_value.addEventListener("change", check_rows)
    current_row_value.addEventListener("change", delete_empty)
}

window.addEventListener("DOMContentLoaded", main)