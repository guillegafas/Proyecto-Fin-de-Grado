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

<h1>Inicio de Sesión</h1>
<div>
    <form action="" method="post">
        Email:
        <input type="text" name="email" required><br>
        <br>
        Contraseña:
        <input type="password" name="pass" required><br><br>
        <input type="submit" name="enviar" value="Iniciar sesion">
    </form> 
    <p>En caso de no tener cuenta, pueda crear una aqui<a href="crear_cuenta.php" class="button">Crear cuenta</a></p>
</div>
<?php

if(isset($_POST['enviar'])){
    // Recoger los datos del formulario
    $email = $_POST['email'];
    $contrasena = $_POST['pass'];

    // conexion con la bbdd
    $conexion = mysqli_connect("localhost", "root", "", "restaurante");
    
    // Verificar si el email ya está registrado
    $email = mysqli_real_escape_string($conexion, $_POST['email']);
    $existe = mysqli_query($conexion, "SELECT COUNT(*) AS cantidad, PASS FROM clientes WHERE EMAIL='$email'");
    $fila = mysqli_fetch_assoc($existe);

    if($fila['cantidad'] == 0){
        echo "</br></br></br></br></br></br>";
        echo "<center>";
        echo "<table style='background-color: white;'><tr><td>No existe usuario asociado con el mail escrito</td></tr></table>";
    } else{
        // Verificar si la contraseña es correcta
        $contrasena_hash = $fila['PASS'];
        if (password_verify($contrasena, $contrasena_hash)) {
            // Iniciar sesión
            session_start();
            // Redirigir a la página principal
            header("Location: pagina_principal.html");
            exit(); // Asegura que el script se detenga después de la redirección
        } else {
            echo "</br></br></br></br></br></br>";
            echo "<center>";
            echo "<table style='background-color: white;'><tr><td>La contraseña es incorrecta</td></tr></table>";
        }
    }
}
?>


</body>
</html>