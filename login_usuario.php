<?php
    session_start();
    
    // Conexión a la base de datos
    $servername = "localhost";
    $username = "id21310560_vitapulse";
    $password = "Ariana0208.";
    $dbname = "id21310560_login_registro_datos";
    
    $conn = new mysqli($servername, $username, $password, $dbname);
    
    // Verificar la conexión
    if ($conn->connect_error) {
        die("La conexión a la base de datos falló: " . $conn->connect_error);
    }
    
    // Obtener datos del formulario
    $usuario_l = $_POST['username'];
    $contrasena_l = $_POST['clave'];
    
    // Consulta SQL para verificar las credenciales
    $sql2 = "SELECT * FROM usuarios WHERE usuario = '$usuario_l' AND contrasena = '$contrasena_l'";
    $result = $conn->query($sql2);
    
    if ($result->num_rows == 1) {
        echo "bienvenido";
        // Iniciar sesión y redirigir al usuario
        $_SESSION['usuario'] = $usuario_l;
        header("Location: datos.html");
        exit();
    } else {
        // Credenciales incorrectas, mostrar mensaje de error
        echo "Usuario o contraseña incorrectos.";
    }
    
    // Cerrar la conexión
    $conn->close();
?>