import selected from "./dataset_list_form.js";

function send(e) {
    const formData = new FormData();

    formData.append("pks", JSON.stringify(metadata_payload))

    fetch(
        "/datasets/table",
        {
            "headers": {
                "X-CSRFToken": csrftoken
            },
            "method": "POST",
            "body": formData
        }
    ).then(
        (response) => {
            response
        }
    )
}