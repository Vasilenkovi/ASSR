class SocketHandler {

    constructor(url) {
        this.url = url
        this.cooldown = false
        this.socket = new WebSocket(this.url)
        this.socket.onmessage = this.recieve
    }

    reconnect() {
        this.socket = new WebSocket(this.url)
    }
    
    send(e) {
        if (this.cooldown) {
            return
        }
    
        this.cooldown = true
        setTimeout(() => {this.cooldown = false}, 1000)
    
        const tag_input = document.getElementById("new-tag")
    
        switch (this.socket.readyState) {
            case WebSocket.CONNECTING:
                return
    
            case WebSocket.OPEN:
                const payload = {
                    "Type": "CreateTagRequest",
                    "TagName": tag_input.value
                }
                this.socket.send(
                    JSON.stringify(payload)
                )
                return
    
            default:
                this.reconnect()
                return
        }
    }
    
    recieve(e) {
        const data = JSON.parse(e.data)
        const tag_input = document.getElementById("new-tag")
    
        if (data["success"]) {
            tag_input.value = ""
            tag_input.placeholder = "Новый тэг"
    
            const tag_id = data["id"]
            const tag_name = data["name"]
            const tag_count = tag_input.children.length
    
            const id_parent = document.getElementById("id_tag")
            const wrapper_div = document.createElement("div")
    
            const label = document.createElement("label")
            label.for = `id_tag_${tag_count}`
    
            const checkbox = document.createElement("input")
            checkbox.type = "checkbox"
            checkbox.name = "tag"
            checkbox.value = tag_id
            checkbox.classList.add("px-2")
            checkbox.id = `id_tag_${tag_count}`
            checkbox.checked = true
            label.appendChild(checkbox)
    
            const text = document.createTextNode(" " + tag_name)
            label.appendChild(text)
    
            wrapper_div.appendChild(label)
            id_parent.appendChild(wrapper_div)
        }
        else {
            if (data["reason"]) {
                tag_input.value = ""
                tag_input.placeholder = "тэг существует"
            }
        }
    }
}

export default SocketHandler