function carregarConteudo(url) {
    fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } })
        .then(response => response.text())
        .then(html => {
            document.getElementById("conteudo-dinamico").innerHTML = html;
            history.pushState({ url: url }, "", url); // Atualiza a URL do navegador
        })
        .catch(error => console.error("Erro na requisição:", error));
}

var atletaID = sessionStorage.getItem("atletaID");
if (atletaID) {
    document.getElementById("atletasSelect").value = atletaID;
    document.getElementById("atletasSelect").dispatchEvent(new Event("change"));
}



function atletaSelectEncomendas() {
    var atletaIDSession = document.getElementById("atletasSelect").value;
    sessionStorage.setItem("atletaID", atletaIDSession);

    var estadoEncomendaSession = document.getElementById("estadoEncomendaSelect").value
    sessionStorage.setItem("estadoEncomenda", estadoEncomendaSession);
    var estadoEncomenda = sessionStorage.getItem("estadoEncomenda");

    var atletaID = sessionStorage.getItem("atletaID");
    let bodyEncomendas = $('.table-encomendas tbody');
    
    if (atletaID.length > 0 ) {

        $.ajax({
            url: '/equipamentos/encomendas_por_atleta/' + atletaID + '/' + estadoEncomenda + '/',
            method: 'GET',
            dataType: 'json',
            success: function (data) {
                let resultados = data.resultados
                if (resultados.length > 0) {
                    bodyEncomendas.empty()

                    resultados.forEach(item => {
                        let row = `<tr>
                                    <td><input type="checkbox" name="selectEncomenda" class="form-check-input selectEncomenda" value="${item.id}">
                                        </td>
                                    <td>${item.atleta}</td>
                                    <td>${item.equipamento}</td>
                                    <td>${item.tamanho}</td>
                                    <td>${item.data_pedido}</td> 
                                    <td><input onchange="alterarEstadoEncomenda('${item.id}')" class="form-check-input estadoEncomenda" type="checkbox" name="entregue" id="entregue" ${item.entregue ? 'checked' : ''}></td>
                                    <td class="linha">
                                    <a href="/equipamentos/encomendas_uptade/${item.id}/"
                                        hx-push-url="true"
                                        class="link-ajax"><span
                                    class="material-symbols-outlined btn-operacoes"> edit</span></a>
                                    <a href="#" class="link-ajax" onclick="deleteEncomenda('${item.id}','${item.atleta}','${item.equipamento}')">
                                    <span class="material-symbols-outlined btn-operacoes">delete</span></a>
                                    </td>
                                    </tr>`

                        bodyEncomendas.append(row)
                    })
                } else {
                    bodyEncomendas.empty()
                    let row = `<tr>
                              <td colspan="6">Nenhuma encomenda encontrada</td>
                              </tr>`
                    bodyEncomendas.append(row)
                }
            },
            error: function (data) {
                bodyEncomendas.html('<tr><td colspan="3">Erro ao buscar encomendas.</td></tr>');
            }
        })


    }
    
}

$(document).on('click', '.pdf-encomendas', function (e) {
    e.preventDefault();

    var lista = [];
    $('.selectEncomenda').each(function () {
        if ($(this).is(':checked')) {
            lista.push($(this).val());
        }
    });

    var form = $('<form>', {
        method: 'POST',
        action: '/equipamentos/pdf_encomendas_atletas/',
        target: '_blank'
    });

    form.append($('<input>', {
        type: 'hidden',
        name: 'csrfmiddlewaretoken',
        value: $('input[name="csrfmiddlewaretoken"]').val()
    }));

    form.append($('<input>', {
        type: 'hidden',
        name: 'encomendas',
        value: JSON.stringify(lista)
    }));

    $('body').append(form);
    form.submit();
    form.remove();
});;

$(document).on('submit', '#form-new-encomenda', function (event) {
    event.preventDefault();
    console.log("Form encomendas encontrado");

    const formData = new FormData(this);
    var url = $(this).attr('data-url');
    console.log("URL:", url);

    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
        .then(response => response.json())
        .then(data => {
            console.log("Resposta do servidor:", data);
            if (data.success) {
                alert(data.message);
                carregarConteudo(window.urlEncomendasList);
            } else if (data.errors) {
                alert("Erros no formulário: " + JSON.stringify(data.errors));
            } else {
                alert(data.message || 'Erro ao criar encomenda.');
            }
        })
        .catch(error => {
            console.error('Erro na requisição:', error);
            alert('Erro inesperado.');
        })
});




function deleteEncomenda(id, atleta, equipamento) {
    if (confirm("Tem certeza que deseja apagar essa encomenda de " + equipamento + " para " + atleta + "?")) {
        fetch('/equipamentos/encomenda_delete/' + id + '/')
            .then(response => response.json())
            .then(data => {
                if (data.success || data.message) {
                    alert(data.message)
                    atletaSelectEncomendas()
                }
                else {
                    alert(data.message || 'Erro ao apagar encomenda.');
                }
            })

    }
    else {
        alert("Operação cancelada");
    }
}


function alterarEstadoEncomenda(idEncomenda) {
    let checkbox = event.target
    if (confirm("Tem certeza que deseja alterar o estado dessa encomenda?")) {
        fetch('/equipamentos/alterar_estado_encomenda/' + idEncomenda + '/')
            .then(response => response.json())
            .then(data => {
                if (data.success || data.message) {
                    alert(data.message)
                    atletaSelectEncomendas()
                }
                else {
                    alert(data.message || 'Erro ao apagar encomenda.');
                }
            })
    }
    else {
        checkbox.checked = !checkbox.checked
    }
}