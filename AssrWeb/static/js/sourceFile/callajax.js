
var last_row = 0

async function makeRequest(url, method, body) {

    let headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json'
    }

    if (method == 'post') {
        headers['X-CSRFToken'] = document.querySelector('[name=csrfmiddlewaretoken]').value
    }

    let responce = await fetch(url, {
        method: method,
        headers: headers,
        body: body
    })

    return await responce.json()
}

document.querySelector('#renderMore').onclick = async function getMoreLines() {
    const data = await makeRequest(
        window.location.href,
        'post',
        JSON.stringify({'last-row': last_row})
    )
    let tablebody = document.getElementById('table_rows')

    let columns = Object.keys(data)
    for (let i = last_row; i < Object.keys(data[columns[0]]).length + last_row; i++){
        let insert_tr = document.createElement('tr')
        insert_tr.insertAdjacentHTML(
            'beforeend',
            "<th>" + i + "</th>"
        )
        columns.forEach(column => {
            let something = data[column][i]
            insert_tr.insertAdjacentHTML(
                'beforeend',
                "<td>" + something + "</td>"
            )
        });
        tablebody.append(insert_tr)
    }
    last_row += Object.keys(data[columns[0]]).length
}
