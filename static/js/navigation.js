let accessToken = localStorage.getItem('accessToken')
if (accessToken !== undefined && accessToken !== null){
    document.getElementById('tag-login').remove()
    document.getElementById('tag-registration').remove()
    document.getElementById('tag-logout').addEventListener('click',
        ()=> localStorage.removeItem('accessToken'))
}else{
    document.getElementById('tag-upload').remove()
    document.getElementById('tag-logout').remove()
}