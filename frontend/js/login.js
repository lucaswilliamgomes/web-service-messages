function submitForm() {
    let URL = "http://127.0.0.1:8000";
    let name = document.getElementById("name").value;
    let xhr = new XMLHttpRequest();
    xhr.open("POST", URL, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    let requestBody = JSON.stringify({"name": name});
    xhr.send(requestBody);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
        if (xhr.status == 200) {
            user = JSON.parse(xhr.responseText)
            localStorage.setItem("name_user", user.name)
            window.location = "./messages.html";
        } else {
            alert("Usuário não encontrado!");
            localStorage.clear()
        }
        }
    };
}