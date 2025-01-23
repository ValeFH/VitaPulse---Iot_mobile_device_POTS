document.getElementById("btn_Registrarse").addEventListener("click",registro);
document.getElementById("btn_Iniciasesión").addEventListener("click",IniciarSesion);

//VARIABLES
var cont_login_registro = document.querySelector(".contenedor_login_registro");
var form_login = document.querySelector(".formulario_login");
var form_registro = document.querySelector(".formulario_registro");
var box_trasera_login = document.querySelector(".caja_trasera_login");
var box_trasera_registro = document.querySelector(".caja_trasera_registro");



function IniciarSesion(){
        form_registro.style.display ="none"; 
        cont_login_registro.style.left="10px";
        form_login.style.display="block";
        box_trasera_registro.style.opacity ="1";
        box_trasera_login.style.opacity ="0";
    }

function registro(){
        form_registro.style.display ="block"; //Que tenga un display tipo bloque
        cont_login_registro.style.left="410px";
        form_login.style.display="none";
       // box_trasera_registro.style.opacity ="0";
        box_trasera_login.style.opacity ="1";
    }