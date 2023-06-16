const form = document.getElementById('upload_form')
const name = document.getElementById('name')
const video = document.getElementById('video')
let token = localStorage.getItem('accessToken')


function handleFormSubmit(event) {
    console.log('dsfsd')
    event.preventDefault()
    var fields = new FormData(form)
    upload(fields)
}

form.addEventListener('submit', handleFormSubmit)

function upload(data){
    let xhr = new XMLHttpRequest();
    let url = new URL('https://urfube-4h1y.onrender.com/upload');
    url.searchParams.set('name', name);
    url.searchParams.set('file', video);
    url.searchParams.set('jwttoken', token);
    xhr.open("POST", url)
    if (token === undefined || token == null){
        alert('Авторизуйтесь для загрузки видео')
        return
    }
    xhr.send(data)

    xhr.onload = function() {
        if (xhr.status == 200 | xhr.status == 202) {
            alert('Видео загружено')
            window.location.href = 'https://urfube-4h1y.onrender.com/';

        }else if (xhr.status == 415) {
            alert('Видео не соответствует формату')
        }else if (xhr.status == 401) {
            alert('Вы не авторизованы')
        }else {
            alert(`Ошибка ${xhr.status}: ${xhr.statusText}`);
        }
      };

      xhr.onerror = function() {
        alert("Попробуйте позже");
      };
  }
