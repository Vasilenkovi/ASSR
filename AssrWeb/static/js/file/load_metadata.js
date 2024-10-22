import check_rows from "../widgets/table_keys.js"

function load_metadata(name, author, kv_dict, tag_list) {
    const file_name = document.getElementById("id_name")
    file_name.value = name
    const file_author = document.getElementById("id_author")
    file_author.value = author

    // Clear table
    const file_kv = document.getElementById("kv-append")
    const static_children = Array.prototype.slice.call(file_kv.children)
    for (var row of static_children) {
        if (!(row.id == "current-kv-row")) {
            row.remove()
        }
    }

    for (const [key, value] of Object.entries(kv_dict)) {
        const current_row = document.getElementById("current-kv-row")

        // tr -> [td] -> input
        const current_row_key = current_row.children[0].children[0]
        const current_row_value = current_row.children[1].children[0]

        current_row_key.value = key
        current_row_value.value = value

        check_rows()
    }
    
    const file_tags = document.getElementById("id_tag")
    for (var div of file_tags.children) {
        const checkbox = div.children[0].childNodes[0]
        const label = div.children[0].childNodes[1]

        if (tag_list.includes(label.textContent.trim())) {
            checkbox.checked = true
        }
        else {
            checkbox.checked = false
        }
    }
}

export default load_metadata