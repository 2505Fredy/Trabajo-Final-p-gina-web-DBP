
var menu= document.getElementById('menu');
menu.parentNode.removeChild(menu);

var changeForm= document.getElementById('changeForm');
changeForm.onclick = () => {
    var email= document.getElementById('email');
    document.getElementById('emailtwo').value = '';
    if (changeForm.innerHTML=='Iniciar sesión'){
        email.style.display = 'none';
        document.getElementById('emailtwo').required = false;
        changeForm.innerHTML = 'Registrarme';
        document.querySelector('.message').innerHTML = '¿No estás registrado? ';
        document.querySelector('.message').appendChild(changeForm);
    }
    else{
        email.style.display = 'block';
        document.getElementById('emailtwo').required = true;
        changeForm.innerHTML = 'Iniciar sesión';
        document.querySelector('.message').innerHTML = '¿Estás registrado? ';
        document.querySelector('.message').appendChild(changeForm);
    }
}

var submitVar = document.getElementById('submit');
submitVar.onclick = () => {
    document.getElementById('formOne').submit = "True";
}