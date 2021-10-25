var buttonClose = document.getElementById('about');
var clone = buttonClose.cloneNode(true);
clone.href = "logout";
clone.innerHTML = "Cerrar sesión";
clone.id = "closeSession";
document.getElementById('menuButtons').appendChild(clone);
