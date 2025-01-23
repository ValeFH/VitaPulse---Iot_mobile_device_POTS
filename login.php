<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login y Registro - VitaPulse</title>
    <link rel="shortcut icon" href="./images/favicon.png" type="image/x-icon">
    <link rel="stylesheet" href="./css/normalize.css">
    <link rel="stylesheet" href="./css/estilo_login.css">
    </head>
    <body>
        <main>
        <!--Diseño de bloque para registro y login-->
        <div class="contenedor_todo">
            <div class="caja_trasera">
                
                <div class=".caja_trasera_login">
                    <h3>¿Ya tienes una cuenta?</h3>
                    <p>Inicia sesión para entrar en la página</p>
                    <button id="btn_Iniciasesión">Iniciar sesión</button>
                </div> 
                <div class=".caja_trasera_registro">
                    <h3>¿Aún no tienes una cuenta?</h3>
                    <p>Registrate</p>
                    <button id="btn_Registrarse">Registrarse</button>
                    
                </div> 
            </div>
            <!--Formulario de LOGIN y REGISTRO-->
            <div class="contenedor_login_registro">
                
                <!--Formulario de LOGIN-->
                <form action="php/login_usuario.php" method="post" class="formulario_login">
                    <h2> Iniciar sesión</h2>
                    
                    <input type="text" id="username" placeholder ="Usuario" name= "username" required><br><br>
                    <input type="password" id="clave" placeholder ="Contraseña" name= "clave" required><br><br>
                    <button>Entrar</button>
                </form>
                
                <!--Formulario de REGISTRO-->
                 <form action="php/registro_usuarios.php" method="post" class="formulario_registro">
                    <h2>Registrarse</h2>
                     <input type="text" id="nombre_completo" placeholder ="Nombre Completo" name= "nombre_completo" required><br><br>
                     <input type="text" id="correo" placeholder ="Correo Electrónico" name= "correo" required><br><br>
                     <input type="text" id="usuario" placeholder ="Usuario" name= "usuario" required><br><br>
                     <input type="password" id="contrasena" placeholder ="Contraseña" name= "contrasena" required><br><br>
                     <button>Registrarse</button>
            
                     
                 </form>
                 
            </div>
        </div>
        </main>
        <script src="./js/login_registro.js"></script>
    </body>
</html>