document.addEventListener('DOMContentLoaded', function() {

    const inputs = document.querySelectorAll('.table-cell');


    inputs.forEach(input => {
        input.addEventListener('change', function() {

            const td = this.closest('td');
            

            const rowId = td.getAttribute('data-row');
            const colId = td.getAttribute('data-col');
            const newValue = this.value;


            const pathArray = window.location.pathname.split('/');
            const datasetSlug = pathArray[pathArray.indexOf('datasets-list') + 1];


            fetch(`/dataset/datasets-list/${datasetSlug}/edit_cell/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: new URLSearchParams({
                    'row': rowId,
                    'column': colId,
                    'new_value': newValue
                })
            })
            .then(response => {
                if (response.ok) {
                    console.log('Cell updated successfully');
                } else {
                    console.error('Failed to update cell');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
});


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}