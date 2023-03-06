
window.onload = function() {
    fillPresentation();
    searchAllMessages(sended = true);
};

function getSentMessages() {
    searchAllMessages(sended = true)
}

function getReceivedMessages() {
    searchAllMessages(sended = false)
}

function fillPresentation() {
    const name_user = localStorage.getItem("name_user");
    let divPresentation = document.getElementById("presentation")
    let presentation = "Olá " + name_user;
    divPresentation.innerHTML = `<strong>${presentation}</strong>`;
}

function searchAllMessages(sended = true) {
    const name_user = localStorage.getItem("name_user");
    const xhr = new XMLHttpRequest();
    const url = "http://127.0.0.1:8000/messages";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    let requestBody = JSON.stringify({
        "name": name_user,
        "type": sended ? "sended" : "received"
    });
    xhr.send(requestBody);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            if (xhr.status == 200) {
                showAllReceivedMessages(JSON.parse(xhr.responseText));
            } else {
                alert("Erro ao buscar a lista de mensagens do user: " + name_user);
            }
        }
    };
}

function onClickRow() {
    let id = this.id;
    name_user = localStorage.getItem("name_user")
    if (name_user) {
        window.location.href = `http://127.0.0.1:8000/message/${name_user}/${id}`;
    } else {
        alert("Usuário não encontrado!");
        window.location = "./login.html";
    } 
}

function showAllReceivedMessages(messages) {
    let table = document.getElementById("table-messages");
    while (table.rows.length > 1) {
        table.deleteRow(1);
    }

    for (let i = 0; i < messages.length; i++) {
        let row = table.insertRow();
        row.id = messages[i].id;
        row.addEventListener("click", onClickRow);
        let senderCell = row.insertCell();
        let receiverCell = row.insertCell();
        let subjectCell = row.insertCell();
        senderCell.innerHTML = messages[i].name_sender;
        receiverCell.innerHTML = messages[i].name_receiver;
        subjectCell.innerHTML = messages[i].subject;
    }
}


// adiciona um listener de evento para o botão "Mensagens enviadas"
document.getElementById("sent-messages-button").addEventListener("click", getSentMessages);

// adiciona um listener de evento para o botão "Mensagens recebidas"
document.getElementById("received-messages-button").addEventListener("click", getReceivedMessages);
  
