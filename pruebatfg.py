import mysql.connector
import math
import yaml
from datetime import datetime
import qrcode

def conectar_base_datos():
    # Establecer conexión con la base de datos
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="prueba_tfg"
        )
        print("Conexión exitosa a la base de datos")
        return conexion
    except mysql.connector.Error as err:
        print("Error al conectar a la base de datos:", err)
        return None

def obtener_platos_y_precios(conexion):
    platos_precios = []
    try:
        cursor = conexion.cursor()
        # Consulta para obtener la lista de platos y precios
        consulta = "SELECT id_plato, nombre, precio FROM menu"
        cursor.execute(consulta)
        platos = cursor.fetchall()
        # Almacenar platos y precios en una lista
        for plato in platos:
            platos_precios.append((plato[0], plato[1], plato[2]))
    except mysql.connector.Error as err:
        print("Error al ejecutar la consulta:", err)
    finally:
        if cursor:
            cursor.close()
    return platos_precios

def crear_cuenta_pedido(platos_precios, num_mesa):
    pedido = []
    total_cuenta = 0
    while True:
        seleccion = input("Ingrese el número de plato que desea agregar al pedido (0 para terminar): ")
        if seleccion == '0':
            break
        try:
            id_plato = int(seleccion)
            if id_plato < 1 or id_plato > len(platos_precios):
                print("Por favor, ingrese un número de plato válido.")
                continue
            plato = platos_precios[id_plato - 1]
            pedido.append(plato)
            total_cuenta += plato[2]
        except ValueError:
            print("Por favor, ingrese un número válido.")
    return [num_mesa, total_cuenta]

def seleccionar_mesa(mesas_ocupadas):
    while True:
        try:
            num_mesa = int(input("Ingrese el número de mesa para el pedido (0-9): "))
            if num_mesa < 0 or num_mesa > 9:
                print("Por favor, ingrese un número de mesa válido (0-9).")
            elif num_mesa in mesas_ocupadas:
                print("Esta mesa ya está ocupada. Por favor, seleccione otra mesa.")
            else:
                return num_mesa
        except ValueError:
            print("Por favor, ingrese un número válido.")

def menu():
    print("¡Bienvenido al programa!")
    print("Selecciona una opción:")
    print("1. Ver lista de platos y precios")
    print("2. Crear una cuenta para el pedido de un cliente")
    print("3. Pagar cuenta de una mesa")
    opcion = input("Ingrese el número de opción que desea: ")
    return opcion

def generar_yaml_pedido(pedido):
    # Calcular los puntos del pedido redondeando el precio total hacia arriba
    puntos_pedido = math.ceil(pedido[1])

    # Calcular la fecha actual en el formato adecuado para MySQL
    fecha_actual = datetime.now().strftime('%Y-%m-%d %H-%M-%S')

    # Generar el nombre único del archivo YAML
    nombre_archivo = f"pedido_{fecha_actual}.yaml"

    datos_pedido = {
        'id_restaurante': 1,  # Aquí debes especificar el ID del restaurante correspondiente
        'fecha_pedido': fecha_actual,  # Fecha actual en formato MySQL
        'precio_total': pedido[1],  # Precio total del pedido
        'puntos_pedido': puntos_pedido  # Puntos asociados al pedido
    }

    # Guardar el archivo YAML
    with open(nombre_archivo, 'w') as archivo_yaml:
        yaml.dump(datos_pedido, archivo_yaml, default_flow_style=False)

    # Generar el código QR a partir del contenido del archivo YAML
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(datos_pedido)
    qr.make(fit=True)

    # Guardar el código QR como imagen
    nombre_qr = f"pedido_{fecha_actual}.png"
    imagen_qr = qr.make_image(fill_color="black", back_color="white")
    imagen_qr.save(nombre_qr)


def main():
    conexion = conectar_base_datos()
    if conexion:
        platos_precios = obtener_platos_y_precios(conexion)
        mesas_ocupadas = []
        cuentas_por_mesa = []
        while True:
            opcion = menu()
            if opcion == '1':
                for plato in platos_precios:
                    print(f"{plato[0]}. {plato[1]} - ${plato[2]}")
            elif opcion == '2':
                num_mesa = seleccionar_mesa(mesas_ocupadas)
                mesas_ocupadas.append(num_mesa)
                cuenta_pedido = crear_cuenta_pedido(platos_precios, num_mesa)
                cuentas_por_mesa.append(cuenta_pedido)
                print("Pedido:")
                for plato in platos_precios:
                    print(f"{plato[0]}. {plato[1]} - ${plato[2]}")
                print(f"Total de la cuenta para la mesa {num_mesa}: ${cuenta_pedido[1]}")
            elif opcion == '3':
                print("Mesas ocupadas:")
                for mesa in mesas_ocupadas:
                    print(f"Mesa {mesa}")
                num_mesa = int(input("Ingrese el número de mesa para pagar la cuenta: "))
                total_a_pagar = 0
                for cuenta in cuentas_por_mesa:
                    if cuenta[0] == num_mesa:
                        total_a_pagar = cuenta[1]
                        cuentas_por_mesa.remove(cuenta)
                        break
                print(f"Total a pagar por la mesa {num_mesa}: ${total_a_pagar}")
                mesas_ocupadas.remove(num_mesa)
                # Generar YAML para el pedido y calcular puntos
                generar_yaml_pedido([num_mesa, total_a_pagar])
            else:
                print("Opción no válida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    main()
