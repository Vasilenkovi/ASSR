import SourceFile from "./source_file.js"
import collect_metadata from "./collect_metadata.js";
import load_metadata from "./load_metadata.js";

const file_dict = {}
var current_file = "";

function delete_file(e) {
    const parent = e.target.parentElement
    delete file_dict[parent.dataset.file_name]
    parent.remove()
}

function switch_file(e) {

    // No operation if file was not changed
    const parent_div = e.target.parentElement
    const clicked_file = parent_div.dataset.file_name
    if (current_file == clicked_file) {
        return
    }

    // Save current metadata
    if (current_file in file_dict) {
        const data = collect_metadata()
        file_dict[current_file].name = data["name"]
        file_dict[current_file].author = data["file_author"]
        file_dict[current_file].key_value = data["file_kv"]
        file_dict[current_file].tags = data["tag_list"]
    }

    current_file = clicked_file

    const name = file_dict[current_file].name
    const author = file_dict[current_file].author
    const kv_dict = file_dict[current_file].key_value
    const tag_list = file_dict[current_file].tags
    load_metadata(name, author, kv_dict, tag_list)
}

function display_files(e) {
    const parent = document.getElementById("file-div")

    for (var file of e.target.files) {

        if (file.name in file_dict) {
            return
        }

        file_dict[file.name] = new SourceFile(file.name, file.arrayBuffer())

        const file_div = document.createElement("div")
        file_div.classList.add("file-pill", "my-2", "d-flex", "justify-content-between")
        file_div.dataset.file_name = file.name

        const file_title = document.createElement("span")
        file_title.innerText = file.name
        file_title.classList.add("mx-2", "file-name")
        file_title.addEventListener("click", switch_file)
        file_div.appendChild(file_title)

        const delete_button = document.createElement("button")
        delete_button.innerText = "X"
        delete_button.classList.add("mx-2", "file-delete-button", "main-text")
        delete_button.addEventListener("click", delete_file)
        file_div.appendChild(delete_button)

        parent.appendChild(file_div)
    }
}

function main() {
    const file_input = document.getElementById("source-files")
    file_input.addEventListener("input", display_files)
}

window.addEventListener("DOMContentLoaded", main)