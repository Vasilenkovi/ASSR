var cooldown = false

function set_name(event) {
    const model_name_field = document.getElementById("model_name")
    model_name_field.value = event.target.value
}

function send_kw(e) {
    if (cooldown) {
        return
    }

    cooldown = true
    setTimeout(() => {cooldown = false}, 1000)

    const kv_params_tag = document.getElementById("kv-append")

    const kv_dict = {}
    for (var row of kv_params_tag.children) {
        const row_key = row.children[0].children[0]
        const row_value = row.children[1].children[0]

        if (row_key.value && row_value.value) {
            kv_dict[row_key.value] = row_value.value
        }
    }
    
    const params_tag = document.getElementById("parameters")
    params_tag.value = JSON.stringify(kv_dict)

    const form_tag = document.getElementById("task_from")
    form_tag.submit()
}

function prevent_enter_send(e) {
    if (e.keyCode == 13) {
        e.preventDefault()
    }
}

function main() {
    const model_name_select = document.getElementById("model_name_selector")
    model_name_select.addEventListener("change", set_name)

    const send_button = document.getElementById("task_send")
    send_button.addEventListener("click", send_kw)

    const form_tag = document.getElementById("task_from")
    form_tag.addEventListener("keypress", prevent_enter_send)
}

document.addEventListener("DOMContentLoaded", main)