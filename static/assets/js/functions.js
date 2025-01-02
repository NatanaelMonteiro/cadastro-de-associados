document.addEventListener('htmx:afterRequest', evt => {
    const status = evt.detail.xhr.status
    var msg = evt.detail.xhr.responseText
    var warning = true

    if (msg) {
        msg = msg.split(":")[1]
    }

    if (status == 201) {
        warning = false
    }

    if (status == 422) {
        msg = "Invalid user data"
    }
    showToast(msg, warning)
})

function showToast(msg, warning) {
    const elm = document.getElementById('toast')
    const toast = bootstrap.Toast.getOrCreateInstance(elm)
    const title = document.getElementById('toast-header');
    const title_msg = document.getElementById('title-msg');
    const toast_msg = document.getElementById("toast-message")
    var msg_tit = ""

    if (warning) {
        msg_tit = "Atenção!"
        title.classList.add('bg-danger');
        title.classList.remove('bg-primary');
    } else {
        msg_tit = "Mensagem"
        title.classList.add('bg-primary');
        title.classList.remove('bg-danger');
    }
    title_msg.innerHTML = msg_tit
    toast_msg.innerHTML = msg
    toast.show()
}

function confirme(event) {
    const checked = event.target.checked;
    const elm = document.getElementById("btn-salvar");

    if (checked) {
        elm.classList.replace("disabled", "enabled")
    } else {
        elm.classList.replace("enabled", "disabled")
    }
}