var buttonClose = document.getElementById('about');
var clone = buttonClose.cloneNode(true);
var user = buttonClose.cloneNode(true);
clone.href = "logout";
clone.innerHTML = "<i class='fas fa-window-close'></i> Cerrar sesión";
clone.id = "closeSession";
user.href = "";
user.innerHTML = "<i class='fas fa-user'></i> Usuario";
user.id = "userInfo";
document.getElementById('menuButtons').appendChild(clone);
document.getElementById('menuButtons').appendChild(user);
