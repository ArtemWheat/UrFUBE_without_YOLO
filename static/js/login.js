async function login(){
    let email = document.getElementById("email").value
    let password = document.getElementById("password").value
    let authdata = {
        'username': email,
        'password': password,
        'grant_type': '',
        'scope': '',
        'client_id': '',
        'client_secret': '',
    }

    let response = await fetch("/auth/jwt/login",
        {
            method: 'POST',
            body: new URLSearchParams(authdata),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'accept': 'application/json'
            },
        })

    if (response.status === 200){
        alert("Успех!")
        window.location.href = 'https://urfube-4h1y.onrender.com/';
    }
    else {
        response.json().then(x => alert(JSON.stringify(x)))
        return
    }

    let object = await response.json()
    let token = object['access_token']
    localStorage.setItem('accessToken', 'Bearer '+ token)
}