function setTooltips() {
    let tooltips = document.querySelectorAll('[data-toggle="tooltip"]');

    for (let i = 0; i < tooltips.length; i++) {
        let tooltip = new bootstrap.Tooltip(tooltips[i]);
    }
}

window.addEventListener('DOMContentLoaded', function () {
    setTooltips();
}, false);

document.addEventListener('htmx:afterRequest', evt => {
    var msg = evt.detail.xhr.responseText
    const status = evt.detail.xhr.status
    const warning = status >= 300

    if (status == 201 || status >= 400) {
        if (msg) {
            msg = msg.split(":")[1]
        }

        if (status == 422) {
            msg = "Dados do usuário inválidos ou não informados."
        }
        showToast(msg, warning)
    }
})

function showToast(msg, warning) {
    if (msg) {
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