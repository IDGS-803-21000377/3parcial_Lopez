import os

ARCHIVO_TEMPORAL = "archivo.txt"

def guardar_pedido_temporal(nombre, tamaño, ingredientes, cantidad_pizzas, subtotal):
    """
    Guarda un pedido en el archivo temporal.
    """
    with open(ARCHIVO_TEMPORAL, "a", encoding="utf-8") as archivo:
        archivo.write(f"{nombre},{tamaño},{','.join(ingredientes)},{cantidad_pizzas},{subtotal}\n")

def leer_pedidos_temporales():
    """
    Lee los pedidos almacenados temporalmente.
    """
    pedidos = []
    if not os.path.exists(ARCHIVO_TEMPORAL):
        return pedidos  

    with open(ARCHIVO_TEMPORAL, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            datos = linea.strip().split(",")
            if len(datos) >= 5:  
                try:
                    nombre = datos[0]
                    tamaño = datos[1]
                    ingredientes = datos[2].split(",") if datos[2] else []
                    cantidad_pizzas = int(datos[3])
                    subtotal = float(datos[4])

                    pedidos.append({
                        "nombre": nombre,
                        "tamaño": tamaño,
                        "ingredientes": ingredientes,
                        "cantidad_pizzas": cantidad_pizzas,
                        "subtotal": subtotal
                    })
                except ValueError as e:
                    print(f"Error al leer un pedido: {e}")  
    return pedidos


def eliminar_pedido_temporal(index):
    """
    Elimina un pedido del archivo temporal por índice.
    """
    pedidos = leer_pedidos_temporales()
    
    if not pedidos:
        print(f"Pedidos disponibles: {len(pedidos)}, índice recibido: {index}")
        return False

    if 0 <= index < len(pedidos):
        del pedidos[index]
        
        with open(ARCHIVO_TEMPORAL, "w", encoding="utf-8") as archivo:
            for pedido in pedidos:
                archivo.write(f"{pedido['nombre']},{pedido['tamaño']},{','.join(pedido['ingredientes'])},{pedido['cantidad_pizzas']},{pedido['subtotal']}\n")
        
        print(f"Pedido eliminado correctamente. Ahora hay {len(pedidos)} pedidos en el archivo.")
        return True
    else:
        print(f"Índice no válido: {index}. Pedidos disponibles: {len(pedidos)}")
        return False
