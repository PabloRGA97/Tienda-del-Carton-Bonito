# PROYECTO TIENDA

#importaciones
import os
import time
import tkinter as tk  # Biblioteca para crear interfaces gráficas
from tkinter import Tk, Label
from tkinter import messagebox  # Para mostrar mensajes emergentes (ej: errores)
from PIL import Image, ImageTk  # Para trabajar con imágenes en tkinter
from colorama import Fore, Back, Style, init  # Para dar color al texto en consola
import pygame  # Para reproducir música

# Iniciar musica
pygame.mixer.init()
cancion = "canciones\music.mp3"  # Ruta de la canción

# Banner de bienvenida en ASCII
letrero = ("""
             _        _      _____ ___ _____ _   _ ____    _            
            | |      / \    |_   _|_ _| ____| \ | |  _ \  / \           
            | |     / _ \     | |  | ||  _| |  \| | | | |/ _ \          
            | |___ / ___ \    | |  | || |___| |\  | |_| / ___ \         
            |_____/_/   \_\   |_| |___|_____|_| \_|____/_/   \_\        
                             ____  _____ _                              
                            |  _ \| ____| |                             
                            | | | |  _| | |                             
                            | |_| | |___| |___                          
                            |____/|_____|_____|                         
  ____    _    ____ _____ ___  _   _   ____   ___  _   _ ___ _____ ___  
 / ___|  / \  |  _ \_   _/ _ \| \ | | | __ ) / _ \| \ | |_ _|_   _/ _ \ 
| |     / _ \ | |_) || || | | |  \| | |  _ \| | | |  \| || |  | || | | |
| |___ / ___ \|  _ < | || |_| | |\  | | |_) | |_| | |\  || |  | || |_| |
 \____/_/   \_\_| \_\|_| \___/|_| \_| |____/ \___/|_| \_|___| |_| \___/ 
""")

# Diccionario de usuarios y contraseñas
usuarios = {}
usuario_admin = "admin"
contraseña_admin = "CartonPresioso"

# Diccionario con productos en venta, separados por categoría
inventario = {
    "pokemon": [
        {"Codigo":"1", "nombre": "Charizard", "cantidad": 10, "precio": 55.00},
        # ... más cartas ...
        {"Codigo":"21", "nombre": "e-Nigma", "cantidad": 15, "precio": 14.90},
    ],
    "decks": [
        {"Codigo":"1", "nombre": "Deck Ancient Box", "cantidad": 3, "precio": 47.22},
        # ... más decks ...
        {"Codigo":"10", "nombre": "Deck Dragapult", "cantidad": 4, "precio": 61.22},
    ],
}

ventas = []  # Lista para guardar ventas realizadas
compras = []  # Compras temporales hasta ser finalizadas
pedidos = []
total = 0

# Rutas de las imágenes de productos (por código)
catalogo_pkm_1 = "imagenes/cartas/1.PNG"
# ... hasta el catalogo_pkm_21, catalogo_deck_10 (omitido por brevedad)

# Carpetas base de imágenes por tipo de producto
carpetas_imagenes = {
    "1": "imagenes/cartas",
    "2": "imagenes/decks",
}

# Verifica que existan las carpetas de imágenes
for carpeta in carpetas_imagenes.values():
    if not os.path.exists(carpeta):
        print(f"La carpeta {carpeta} no existe.")
        exit()

# Construcción de rutas de imágenes ordenadas por menú (para mostrar en la interfaz)
imagenes_por_menu = {
    "1": [os.path.join(carpetas_imagenes["1"], f"{i}.PNG") for i in range(1, 22)],
    "2": [os.path.join(carpetas_imagenes["2"], f"{i}.PNG") for i in range(1, 11)],
}

# COMIENZO DEL PROGRAMA
os.system("cls")

# Inicia la música y muestra el letrero en consola
while True:
    pygame.mixer.music.load(cancion)
    pygame.mixer.music.play()
    print(Fore.RED + letrero)
    print(Fore.BLUE + "Bienvenido a la Tienda Online de TCG")

    # LOGIN DE ADMIN
    usuario = input("Introduce el nombre de usuario: ")
    contraseña = input("Introduce la contraseña: ")
    if usuario == usuario_admin and contraseña == contraseña_admin:
        os.system("cls")
        while True:
            print("\n--- Menú Administrador ---")
            print("1. Consultar Inventario")
            print("2. Generar Venta")
            print("3. Consultar Ventas")
            print("4. Modificar Precios de Cartas")
            print("5. Eliminar Productos")
            print("6. Salir")
            opcion_admin = input("Elige una opción: ")

            if opcion_admin == "1":  # Mostrar inventario
                os.system("cls")
                for categoria in inventario.keys():
                    print(f"Categoria: {categoria.capitalize()}")
                    for item in inventario[categoria]:
                        print(f"{item['Codigo']} - {item['nombre']} - {item['cantidad']} unidades - {item['precio']} €")

            elif opcion_admin == "2":  # Generar venta
                os.system("cls")
                print("\n--- Generar Venta ---")

                # Crear ventana gráfica para mostrar productos
                ventana = tk.Tk()  # Nueva ventana
                ventana.title("Menú de Imágenes")

                etiqueta_menu = tk.Label(ventana, text="Seleccione un menú (1 o 2):")
                etiqueta_menu.pack(pady=10)

                for opcion in ["1", "2"]:
                    boton_menu = tk.Button(
                        ventana,
                        text=f"Menú {opcion}",
                        command=lambda opcion=opcion: (
                            [widget.destroy() for widget in ventana.winfo_children()],  # Elimina botones anteriores
                            tk.Label(ventana, text=f"Seleccione un número del 1 al {len(imagenes_por_menu[opcion])}:").pack(pady=10),
                            [
                                tk.Button(
                                    ventana,
                                    text=str(i),
                                    command=lambda opcion=opcion, i=i: (
                                        Image.open(imagenes_por_menu[opcion][i - 1]).show()
                                        if os.path.exists(imagenes_por_menu[opcion][i - 1])
                                        else messagebox.showerror("Error", "La imagen no existe.")
                                    )
                                ).pack(pady=5) for i in range(1, len(imagenes_por_menu[opcion]) + 1)
                            ]
                        )
                    )
                    boton_menu.pack(pady=5)

                ventana.mainloop()  # Ejecuta el bucle de la ventana

                # Después de cerrar la ventana, vuelve al flujo en consola
                # Aquí se pide código y cantidad para procesar la venta
                # ... (continuación del procesamiento de compras y ventas en consola)

            elif opcion_admin == "3":
                os.system("cls")
                print("\n--- Ventas Realizadas ---")
                # Muestra resumen de todas las ventas

            elif opcion_admin == "4":
                os.system("cls")
                print("\n--- Modificar Precios ---")
                # Permite cambiar precios ingresando el código de producto

            elif opcion_admin == "5":
                os.system("cls")
                print("\n--- Eliminar Productos ---")
                # Permite eliminar cartas del inventario por código

            elif opcion_admin == "6":
                os.system("cls")
                break  # Sale del menú admin

            else:
                print("Opción no válida")

    else:
        print("Usuario o contraseña incorrectos. Inténtalo de nuevo.")
