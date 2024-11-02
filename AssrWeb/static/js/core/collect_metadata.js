function collect_metadata() {
    const file_name = document.getElementById("id_name")
    const file_author = document.getElementById("id_author")
    const file_kv = document.getElementById("kv-append")
    const file_tags = document.getElementById("id_tag")

    const kv_dict = {}
    for (var row of file_kv.children) {
        const row_key = row.children[0].children[0]
        const row_value = row.children[1].children[0]

        if (row_key.value && row_value.value) {
            kv_dict[row_key.value] = row_value.value
        }
    }

    const tag_list = []
    for (var div of file_tags.children) {
        const checkbox = div.children[0].childNodes[0]
        const label = div.children[0].childNodes[1]

        if (checkbox.checked) {
            tag_list.push(label.textContent.trim())
        }
    }

    return {
        "name": file_name.value,
        "file_author": file_author.value,
        "file_kv": kv_dict,
        "tag_list": tag_list
    }
}

export default collect_metadata