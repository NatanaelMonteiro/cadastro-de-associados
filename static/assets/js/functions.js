document.addEventListener('htmx:afterRequest', evt => {
    var msg = evt.detail.xhr.responseText
    const status = evt.detail.xhr.status
    const warning = status >= 300

    setTooltips();

    if (status > 200) {
        if (status >= 400) {
            if (msg) {
                msg = msg.split(":")[1]
            }

            if (status == 422) {
                msg = "Dados do usuário inválidos ou não informados."
            }
        }
        showToast(msg, warning)
    }
})

function setTooltips() {
    let tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');

    for (let i = 0; i < tooltips.length; i++) {
        let tooltip = new bootstrap.Tooltip(tooltips[i]);
    }
}

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

function agree(event) {
    const checked = event.target.checked;
    const elm = document.getElementById("btn-salvar");

    if (checked) {
        elm.classList.replace("disabled", "enabled")
    } else {
        elm.classList.replace("enabled", "disabled")
    }
}

function defaultSelectOption(id, defaultValue) {
    const select = document.getElementById(id);
    select.value = defaultValue;
}

function defaultRadioOption(id, defaultValue) {
    const select = document.getElementById(id);
    select.checked = (id == defaultValue);
};

let admin = document.getElementById("admin-settings");

if (admin != null) {
    admin.addEventListener("htmx:confirm", confirm, false);
    admin.addEventListener('htmx:beforeSwap', evt => {
        if (evt.detail.xhr.status >= 300) {
            evt.detail.shouldSwap = false
            return
        }
    })
}

function confirm(evt) {
    if (evt.detail.question !== null) {
        evt.preventDefault();

        let msg = ''

        if (evt.detail.elt.id == 'admin') {
            msg = 'Você deseja realmente conceder poderes de Administrador para o usuário'
        } else if (evt.detail.elt.id == 'remove') {
            msg = 'Você deseja mesmo retirar as permissões de administrador do usuário'
        } else if (evt.detail.elt.id == 'delete') {
            msg = 'Você deseja mesmo excluir do sistema o usuário'
        } else {
            msg = 'Voce deseja mesmo aplicar essa alteração no cadastro de'
        }

        msg = `${msg} ${(evt.detail.question).toUpperCase()}?`

        const isWarning = (evt.detail.verb == "delete");

        Swal.fire({
            customClass: { confirmButton: isWarning ? "bg-warning" : "bg-normal" },
            buttonsStyling: false,
            showCancelButton: true,
            reverseButtons: true,
            confirmButtonText: "SIM",
            cancelButtonText: "NÃO",
            title: 'Favor confirmar!',
            text: msg,
        }).then(function (res) {
            if (res.isConfirmed) evt.detail.issueRequest(true)
        })
    }
}
