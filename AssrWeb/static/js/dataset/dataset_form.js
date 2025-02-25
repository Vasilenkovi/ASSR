import Checkbox_handler from "./checkbox_handler.js"
import collect_metadata from "../core/collect_metadata.js";

const ch = new Checkbox_handler()

function preview(e) {
    const target_div = document.getElementById("preview-table")

    const div_container = document.createElement("div")
    div_container.classList.add("container-fluid", "d-flex", "justify-content-center")

    const div = document.createElement("div")
    div.classList.add("spinner-border", "text-secondary")
    div_container.appendChild(div)

    target_div.innerHTML = "";
    target_div.appendChild(div_container)

    const formData = new FormData();

    formData.append("pks", JSON.stringify(ch.selected))

    fetch(
        "/dataset/table",
        {
            "headers": {
                "X-CSRFToken": csrftoken
            },
            "method": "POST",
            "body": formData
        }
    ).then(
        (response) => response.json()
    ).then(
        (data) => {
            const html_safe = data["html_table"]
            target_div.innerHTML = html_safe
            
        }
    )
}

function send(e) {
    const formData = new FormData()

    formData.append("source_pks", JSON.stringify(ch.selected))

    const data = collect_metadata()
    const metadata_payload = {
        "name": data["name"],
        "author": data["file_author"],
        "key_value": data["file_kv"],
        "tags": data["tag_list"],
    }

    formData.append("metadata", JSON.stringify(metadata_payload))

    fetch(
        "/dataset/save",
        {
            "headers": {
                "X-CSRFToken": csrftoken
            },
            "method": "POST",
            "body": formData
        }
    ).then(
        (response) => {
            if (response.ok) {
                const button = document.getElementById("send-dataset")
                const previous_text = button.textContent
                
                button.textContent = "✓"
                setTimeout((button, previous_text) => {
                    button.textContent = previous_text
                    window.location.reload()
                }, 500, button, previous_text)
            }
            else {
                const button = document.getElementById("send-dataset")
                const previous_text = button.textContent
                
                button.textContent = "✖"
                setTimeout((button, previous_text) => {
                    button.textContent = previous_text
                }, 500, button, previous_text)
            }
        }
    )
}

function send_filter(e) {
    const page_num = e.target.dataset.page
    const url = `/source/filter-source-list?page=${page_num}` 

    const input = document.getElementById("search_source")
    const filter_string = input.value.trim()

    const formData = new FormData()
    formData.append("contains", filter_string)


    const path = window.location.pathname;
    const segments = path.split('/').filter(segment => segment !== '');
    const datasetIndex = segments.length > 0 ? parseInt(segments[segments.length - 1], 10) : null;

    formData.append("dataset_pk", datasetIndex)
    fetch(
        url,
        {
            "headers": {
                "X-CSRFToken": csrftoken
            },
            "method": "POST",
            "body": formData
        }
    ).then(
        (response) => {
            if (response.ok) {
                return response.json()
            }
        }
    ).then(
        (data) => {
            if (data) {
                const html_safe = data["table_html"]
                const target_div = document.getElementById("source-table")
                target_div.innerHTML = html_safe
    
                const forms = target_div.getElementsByTagName('form')
                for(const form of forms) {
                    const csrfInput = document.createElement('input')
                    csrfInput.type = 'hidden'
                    csrfInput.name = 'csrfmiddlewaretoken'
                    csrfInput.value = csrftoken
                    form.insertBefore(csrfInput, form.firstElementChild)
                }

                const source_search_as = document.getElementsByClassName("source-search-button")
                for (let a of source_search_as) {
                    a.addEventListener("click", send)
                }
                
                ch.attach_listeners()
            }
        }
    )
}

function send_source_pk(e) {
    const dataset_id = document.getElementById("dataset-id-div").dataset.dataset_id
    const formData = new FormData()

    formData.append("source_pks", JSON.stringify(ch.selected))

    fetch(
        `/dataset/${dataset_id}/save-source/`,
        {
            "headers": {
                "X-CSRFToken": csrftoken
            },
            "method": "POST",
            "body": formData
        }
    ).then(
        (response) => {
            if (response.ok) {
                const button = document.getElementById("source-list-update")
                const previous_text = button.textContent
                
                button.textContent = "✓"
                setTimeout((button, previous_text) => {
                    button.textContent = previous_text
                    window.location.reload()
                }, 500, button, previous_text)
            }
            else {
                const button = document.getElementById("source-list-update")
                const previous_text = button.textContent
                
                button.textContent = "✖"
                setTimeout((button, previous_text) => {
                    button.textContent = previous_text
                }, 500, button, previous_text)
            }
        }
    )
}

function main() {

    // These ids are defined for dataset creation page
    const preview_button = document.getElementById("load-preview")
    const send_button = document.getElementById("send-dataset")
    if (preview_button && send_button) {
        preview_button.addEventListener("click", preview)
        send_button.addEventListener("click", send)
    }

    // This id is defined for dataset view page
    const update_button = document.getElementById("source-list-update")
    if (update_button) {
        update_button.addEventListener("click", send_source_pk)
    }

    const source_search_button = document.getElementById("source-search-button-id")
    source_search_button.addEventListener("click", send_filter)

    const source_search_as = document.getElementsByClassName("source-search-button")
    for (let a of source_search_as) {
        a.addEventListener("click", send_filter)
    }

    ch.push_checked()
    ch.attach_listeners()
}

document.addEventListener("DOMContentLoaded", main)