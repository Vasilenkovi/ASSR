document.addEventListener('DOMContentLoaded', function() {
    async function handleDeletion(btnId, checkboxClass, endpoint, paramName) {
        const btn = document.getElementById(btnId);
        if (!btn) return;

        btn.addEventListener('click', async function() {
            const checkedCheckboxes = document.querySelectorAll(`${checkboxClass}:checked`);
            const pathArray = window.location.pathname.split('/');
            const datasetSlug = pathArray[pathArray.indexOf('datasets-list') + 1];

            btn.disabled = true;
            const originalText = btn.textContent;
            btn.textContent = 'Processing...';

            try {
                for (const checkbox of checkedCheckboxes) {
                    const value = checkbox.dataset.col || checkbox.dataset.rowid;
                    
                    const response = await fetch(`/dataset/datasets-list/${datasetSlug}/${endpoint}/`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                            'X-CSRFToken': getCookie('csrftoken')
                        },
                        body: new URLSearchParams({ [paramName]: value })
                    });

                    if (!response.ok) {
                        console.error(`Failed to delete ${paramName} ${value}`);
                        continue;
                    }
                    console.log(`${paramName} ${value} deleted successfully`);
                }
                window.location.reload();
            } catch (error) {
                console.error('Error:', error);
            } finally {
                btn.disabled = false;
                btn.textContent = originalText;
            }
        });
    }


    handleDeletion('delete-rows-btn', '.row-checkbox', 'remove_row', 'row');
    handleDeletion('delete-cols-btn', '.column-header-checkbox', 'remove_column', 'column');
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