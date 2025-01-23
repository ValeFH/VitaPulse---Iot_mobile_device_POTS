<?php
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

    //Obtener datos del formulario
    $nombre_completo = $_POST['nombre_completo'];
    $correo = $_POST['correo'];
    $usuario = $_POST['usuario'];
    $contrasena = $_POST['contrasena'];
    
    
    // Validar que el correo electrónico contenga el símbolo "@"
    if (strpos($correo, '@') === false) {
        echo "El correo electrónico debe contener el símbolo '@'.";
    } else {
    // Si la validación es exitosa, proceder con la inserción en la base de datos
        //CREAR UNA QUERY
        // Insertar datos en la base de datos
        $sql = "INSERT INTO usuarios (nombre_completo, correo, usuario, contrasena) VALUES ('$nombre_completo', '$correo', '$usuario', '$contrasena')";
        
        if ($conn->query($sql) === TRUE) {
            echo "¡Gracias por Registrarte!";
        } else {
            echo "Error: " . $sql . "<br>" . $conn->error;
        }
    }
    // Cerrar la conexión
    $conn->close();
?>
