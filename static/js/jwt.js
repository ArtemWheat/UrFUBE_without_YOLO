document.getElementById("jwt").value = localStorage.getItem('accessToken')
//document.getElementById("upload_form").addEventListener("submit", function(event) {
//  event.preventDefault();
//  var xhr = new XMLHttpRequest();
//  xhr.open(this.method, this.action, true);
//  xhr.onload = function() {
//    if (xhr.status === 201) {
//      alert("Ваш файл успешно загружен!");
//      window.location.href = xhr.getResponseHeader("Location");
//    }
//  };
//  var formData = new FormData(this);
//  xhr.send(formData);
//});
