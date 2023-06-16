async function registration() {
    let email = document.getElementById("email").value
    let password = document.getElementById("password").value
    let authdata = JSON.stringify({
        'email': email,
        'password': password,
        "is_active": true,
        "is_superuser": false,
        "is_verified": false
    })

    let response = await fetch("/auth/register", {
        method: 'POST', body: authdata,
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
          },
    })

    if (response.status === 201) {
        alert("Вы зарегестрированны!")
        window.location.href = 'https://urfube-4h1y.onrender.com/';
    }else{
        response.json().then(x => alert(JSON.stringify(x)))
    }
}