import SocketHandler from "../core/tag_socket.js"

const socket_handler_obj = new SocketHandler(`ws://${window.location.host}/ws/add-dataset-tag/`)

function send_button_wrapper(e) {
    socket_handler_obj.send(e)
}

function main() {
    const id_parent = document.getElementById("create-tag")
    id_parent.addEventListener("click", send_button_wrapper)
}

window.addEventListener("DOMContentLoaded", main)