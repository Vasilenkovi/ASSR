class Checkbox_handler {
    constructor() {
        this.selected = []
    }

    attach_listeners() {
        const checkboxes = document.getElementsByClassName("large-checkbox")
    
        for (var c of checkboxes) {
            c.addEventListener("input", this.listener)

            if (this.selected.includes(c.dataset.pk)) {
                c.checked = true
            }
        }
    }

    listener = (e) => {
        const checkbox = e.target
        const pk = checkbox.dataset.pk
    
        if (checkbox.checked && !(this.selected.includes(pk))) {
            this.selected.push(pk)
        }
        else if (!checkbox.checked && this.selected.includes(pk)) {
            this.selected = this.selected.filter(x => x != pk)
        }
    }


}

export default Checkbox_handler