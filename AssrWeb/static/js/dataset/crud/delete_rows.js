document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('delete-rows-btn').addEventListener('click', async function() {
        const checkedCheckboxes = document.querySelectorAll('.row-checkbox:checked');
        const pathArray = window.location.pathname.split('/');
        const datasetSlug = pathArray[pathArray.indexOf('datasets-list') + 1];
        

        const btn = this;
        btn.disabled = true;
        btn.textContent = 'Deleting...';

        try {

            for (const checkbox of checkedCheckboxes) {
                const rowId = checkbox.dataset.rowid;
                
                const response = await fetch(`/dataset/datasets-list/${datasetSlug}/remove_row/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: new URLSearchParams({ 'row': rowId })
                });

                if (!response.ok) {
                    console.error(`Failed to delete row ${rowId}`);
                    continue; 
                }
                
                console.log(`Row ${rowId} deleted successfully`);
            }
            

            window.location.reload();
            
        } catch (error) {
            console.error('Error:', error);
        } finally {
            btn.disabled = false;
            btn.textContent = 'Delete Selected Rows';
        }
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