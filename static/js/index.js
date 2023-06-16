let videos = document.getElementsByTagName('video')
let i = 0
for (let elem of document.getElementsByTagName('li')){
    let video = videos[i]
    i += 1
    let url = video.getAttribute('src')
    let id = url.split('/').reverse()[0]
    elem.addEventListener('click', (e) => onclick(id))
}

function onclick(videoId){
    window.location.replace('/video/' + videoId)
}