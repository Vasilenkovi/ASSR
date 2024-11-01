import selected from "./dataset_list_form.js";
import collect_metadata from "../core/collect_metadata.js";

function preview(e) {
    const formData = new FormData();

    formData.append("pks", JSON.stringify(selected))

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
            const target_div = document.getElementById("preview-table")
            target_div.innerHTML = html_safe
        }
    )
}

function send(e) {
    const formData = new FormData()

    formData.append("source_pks", JSON.stringify(selected))

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

function main() {
    const preview_button = document.getElementById("load-preview")
    preview_button.addEventListener("click", preview)

    const send_button = document.getElementById("send-dataset")
    send_button.addEventListener("click", send)
}

document.addEventListener("DOMContentLoaded", main)