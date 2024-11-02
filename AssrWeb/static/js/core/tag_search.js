document.querySelector('.searchable-tag').onchange = function() {
    var tags = this.querySelectorAll('.searchable-tag');
    for(let i  of tags)
    {
        console.log(i.value);
        console.log(i.checked);
        if( document.querySelector('#tag-'+i.value) )
        {
            continue;
        }
        if(i.checked==false)
        {
             continue;
        }
        else
        {
             let added_tag = document.createElement('label');
             added_tag.className  = "main-text deletable-tag tag-element";
             added_tag.id = "tag-"+i.value;
             added_tag.innerHTML = i.value;
             var search_tags = document.querySelector('.tags-list');
             search_tags.append(added_tag);
        }
    }
};