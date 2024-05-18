<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web Inicio de Sesion</title>
</head>

<style>
    body {
            height: 10px;
            background-image:url(portada.jpg);
            background-size: cover;
        }
    div {
            color: white;
            text-align: center;
            font-size:20px;
            font-family:'Times New Roman', Times, serif Haettenschweiler, 'Arial Narrow Bold', sans-serif;
            position: relative;
            top: 100px;
        }
    h1 {
            color: white;
            text-align: center;
            font-size:60px;
            font-family:'Times New Roman', Times, serif Haettenschweiler, 'Arial Narrow Bold', sans-serif;
            position: relative;
            top: 100px;
        }

                    .menu {
                        background-color: #333;
                        overflow: hidden;
                        position: fixed;
                        top: 0;
                        left: 0;
                        width: 100%;
                    }
                    .menu a {
                        float: left;
                        display: block;
                        color: white;
                        text-align: center;
                        padding: 14px 16px;
                        text-decoration: none;
                    }
                    .menu a:hover {
                        background-color: #111;
                    }
                    .content {
                        color: white;
                        text-align: center;
                        font-size: 20px;
                        margin-top: 50px;
                    }

</style>

<body>

<div class="menu">
        <a href="pagina_principal.html">Home</a>
        <a href="pagina_menu.html">Menu</a>
</div>

<script>    
        if (window.history.replaceState) {
            window.history.replaceState(null, null, window.location.href);
     }
    </script>

<h1>Creacion de cuenta</h1>
<div>
    <form action="" method="post">
        Nombre: <input type="text" name="nombre"/><br>  
        <br>
        Email: <input type="text" name="email"/><br>
        <br>
        Telefono: <input type="number" name="telefono"/></br>
        <br>
        Contraseña: <input type="password" name="pass"/></br>
        </br>
        <input type="submit" name='ENVIAR' value="ENVIAR">
    </form> 
</div>
<?php
if (isset($_POST['ENVIAR'])) {
    if (empty($_POST['nombre']) || empty($_POST['pass']) || empty($_POST['telefono']) || empty($_POST['email'])) {
        echo "</br></br></br></br></br></br>";
        echo "<center>";
        echo "Error: Rellene todos los datos";
    } else {
        // Conexión a la base de datos
        $conexion = mysqli_connect("db", "root", "test", "prueba_tfg");
        
        // Verificar si el email ya está registrado
        $email = mysqli_real_escape_string($conexion, $_POST['email']);
        $existe = mysqli_query($conexion, "SELECT COUNT(*) AS cantidad FROM clientes WHERE EMAIL='$email'");
        $fila = mysqli_fetch_assoc($existe);
        
        if ($fila['cantidad'] == 0) {
            // Obtener la fecha actual
            $fecha_actual = date("Y-m-d"); 
            
            // Convertir la contraseña en un hash
            $contrasena_hash = password_hash($_POST['pass'], PASSWORD_DEFAULT);
            
            // Preparar los valores para la inserción en la base de datos
            $nombre = mysqli_real_escape_string($conexion, $_POST['nombre']);
            $telefono = mysqli_real_escape_string($conexion, $_POST['telefono']);
            
            // Insertar los datos en la base de datos
            $query = "INSERT INTO clientes (NOMBRE, EMAIL, TLF, contrasenya, FECHA_ALTA, PUNTOS) 
                      VALUES ('$nombre', '$email', '$telefono', '$contrasena_hash', '$fecha_actual', 10)";
            
            if (mysqli_query($conexion, $query)) {
                echo "</br></br></br></br></br></br>";
                echo "<center>";
                echo "<table style='background-color: white;'><tr><td>Alta de $nombre realizada con éxito</td></tr></table>";
            } else {
                echo "Problemas con el insert: " . mysqli_error($conexion);
            }
        } else {
            echo "</br></br></br></br></br></br>";
            echo "<center>";
            echo "<table style='background-color: white;'><tr><td>El email $email ya está asociado a una cuenta, intente con otro</td></tr></table>";
        }

        mysqli_close($conexion);
    }
}
?>

</body>
</html>
