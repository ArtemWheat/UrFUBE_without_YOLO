let like = document.getElementById('like_block');
let videoId = window.location.toString().split('/').reverse()[0];
let checked = document.getElementById('checked')
const form = document.getElementById('video_form')
let token = localStorage.getItem('accessToken')

function handleFormSubmit(event) {
    console.log('dsfsd')
    event.preventDefault()
    var fields = new FormData(form)
    upload(fields)
}

form.addEventListener('submit', handleFormSubmit)


like.addEventListener('click',  async () => {

    let accessToken = localStorage.getItem('accessToken')
    if (accessToken === undefined || accessToken == null){
        return
    }
    let liked = checked.checked
    let type = 'like'
    if (liked){
        type = 'dislike'
    }
    let request = await fetch("/video/" + videoId + '/' + type + '/' + accessToken, {
        method: 'POST',
        headers: {
            'Authorization': accessToken,
        }
    })
    if (request.status === 200 || request.status === 201){
        let count = document.getElementById('count_likes')
        if (type === 'like'){
            count.innerText = String(Number(count.innerText) + 1)
        }else{
            count.innerText = String(Number(count.innerText) - 1)
        }
        checked.checked = !checked.checked
        update_like_img()
        return
    }
    request.json().then(x => JSON.stringify(x))
})


async function is_liked(){
    let accessToken = localStorage.getItem('accessToken')
    let request = await fetch('/video/' + videoId +'/is_liked/' + accessToken, {
        method: 'GET',
        headers: {
            'Authorization': accessToken,
            'accept': '*/*'
        }
    })

    if (request.status === 200){
        checked.checked = (await request.json())['is_liked']
        update_like_img()
    }
}

function update_like_img(){
    let not_liked = "https://img.icons8.com/?size=512&id=U6uSXVbuA1xU&format=svg"
    let liked = "https://img.icons8.com/?size=512&id=WhoOVX5nZuxR&format=svg"
    if (checked.checked){
            let like = document.getElementById('like')
            like.src = liked
        }else{
            let like = document.getElementById('like')
            like.src = not_liked
        }
}

is_liked().then(() => {})


function upload(data){

    id = form.getAttribute('name')
    let xhr = new XMLHttpRequest();
    let url = new URL('http://88.218.62.143/delete');
    url.searchParams.set('id', id);
    url.searchParams.set('jwttoken', token);
    xhr.open("POST", url)
    if (token === undefined || token == null){
        alert('Вам нельяза удалять видео')
        return
    }
    xhr.send(data)

    xhr.onload = function() {
        if (xhr.status == 200 | xhr.status == 204) {
            alert('Видео удалено')
            window.location.href = 'http://88.218.62.143/';

        }else if (xhr.status == 401) {
            alert('Это не ваше видео')
        }else {
            alert(`Ошибка ${xhr.status}: ${xhr.statusText}`);
        }
      };

      xhr.onerror = function() {
        alert("Попробуйте позже");
      };
  }
