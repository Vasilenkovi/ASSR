document.querySelector('.searchable-tag').onchange = function() {
    var tags = this.querySelectorAll('.searchable-tag');
    for(let j of tags)
    {
    let i = j.parentElement;
                console.log("started");
        if(document.querySelector('#tag-'+i.textContent.trim()) )
        {
            console.log("exist");
            continue;
        }
        if(j.checked==false)
        {
                    console.log("unchecked");
             continue;
        }
        else
        {
             let added_tag = document.createElement('label');
             added_tag.className  = "main-text deletable-tag tag-element";
             added_tag.id = "tag-"+i.textContent.trim();
             added_tag.innerHTML = i.textContent.trim();
             var search_tags = document.querySelector('.tags-list');
             search_tags.append(added_tag);
        }
    }
};