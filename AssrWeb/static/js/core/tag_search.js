
document.querySelector('.searchable-tag').onchange = function() {
    var tags = this.querySelectorAll('.searchable-tag');
    var search_tags = document.querySelector('.tags-list');
    for(let j of tags)
    {
        let i = j.parentElement;
        let query = document.querySelector('#tag-'+i.textContent.trim());
        if(query) // element exists
        {
            if (!j.checked)
            {
                let tag = document.getElementById("tag-"+i.textContent.trim())
                search_tags.removeChild(tag);
            }
        }
        else if(j.checked) // element checked but does not exist
        {
            let added_tag = document.createElement('label');
            added_tag.className  = "main-text deletable-tag tag-element";
            added_tag.id = "tag-"+i.textContent.trim();
            added_tag.innerHTML = i.textContent.trim();
            search_tags.append(added_tag);
        } // every else goes away
    }
};
