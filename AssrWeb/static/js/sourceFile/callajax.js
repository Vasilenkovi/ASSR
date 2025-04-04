var last_row = 0

async function makeRequest(url, method, body) {

    let headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json'
    }

    if (method == 'POST') {
        headers['X-CSRFToken'] = document.querySelector('[name=csrfmiddlewaretoken]').value
    }

    let response = await fetch(url, {
        "headers": headers,
        "method": method,
        "body": body
    })

    return await response.json()
}

document.querySelector('#renderMore').onclick = async function getMoreLines() {
    const data = await makeRequest(
        window.location.href,
        'POST',
        JSON.stringify({'last-row': last_row})
    )
    console.log(data)
    let tablebody = document.getElementById('table-rows')

    let columns = Object.keys(data)
    if (Object.keys(data[columns[0]]).length != 0){
        for (let index_row = last_row; index_row < Object.keys(data[columns[0]]).length + last_row; index_row++){
            let insert_tr = document.createElement('tr')
            insert_tr.insertAdjacentHTML( // insert index as th
                'beforeend',
                `<th>${index_row}</th>`
            )

            insert_tr.insertAdjacentHTML( // insert index checkbox as td
                'beforeend',
                `<td data-col="0" data-row="${index_row}">\n<input class="row-checkbox" data_rowid="${index_row}" type="checkbox"/>\n</td>`
            )

            for (let column_index = 0; column_index < columns.length; column_index++){ // insert each column
                let contents = data[columns[column_index]][index_row]
                insert_tr.insertAdjacentHTML(
                    'beforeend',
                    `<td data-col="${column_index}" data-row="${index_row}">\n<input value="${contents}"/>\n</td>`
                )
            }
            tablebody.append(insert_tr) // append
        }
        last_row += Object.keys(data[columns[0]]).length
    }
    else {
        let button = document.getElementById('renderMore')
        button.disabled = true
        button.innerText = "Got nothing to render :("
    }
}
