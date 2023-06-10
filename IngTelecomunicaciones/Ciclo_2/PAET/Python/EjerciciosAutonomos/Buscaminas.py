import random
import tkinter as tk
from PIL import ImageTk, Image

# Dimensiones del tablero
filas = 8
columnas = 8
minas = 10

# Crear el tablero
tablero = [[0 for _ in range(columnas)] for _ in range(filas)]
minas_coords = []

# Cargar imágenes
imagen_mina = ImageTk.PhotoImage(Image.open("mina.png").resize((20, 20)))
imagenes_numeros = []
for i in range(1, 9):
    imagen_numero = ImageTk.PhotoImage(Image.open(f"numero-1.png").resize((20, 20)))
    imagenes_numeros.append(imagen_numero)

# Función para colocar las minas aleatoriamente
def colocar_minas():
    global minas_coords
    minas_coords = random.sample(range(filas * columnas), minas)
    for i in range(minas):
        fila = minas_coords[i] // columnas
        columna = minas_coords[i] % columnas
        tablero[fila][columna] = -1

# Función para contar el número de minas adyacentes a una celda
def contar_minas(fila, columna):
    if tablero[fila][columna] == -1:
        return -1
    count = 0
    for i in range(max(0, fila-1), min(fila+2, filas)):
        for j in range(max(0, columna-1), min(columna+2, columnas)):
            if tablero[i][j] == -1:
                count += 1
    return count

# Función para revelar una celda
def revelar_celda(fila, columna):
    if tablero[fila][columna] == -1:
        boton = botones[fila][columna]
        boton.config(image=imagen_mina, state=tk.DISABLED)
        messagebox.showinfo("Game Over", "Has perdido.")
        reiniciar_juego()
        return
    elif tablero[fila][columna] > 0:
        boton = botones[fila][columna]
        boton.config(image=imagenes_numeros[tablero[fila][columna]], state=tk.DISABLED)
        return
    elif tablero[fila][columna] == 0:
        visitados = set()
        visitados.add((fila, columna))
        queue = [(fila, columna)]
        while queue:
            f, c = queue.pop(0)
            for i in range(max(0, f-1), min(f+2, filas)):
                for j in range(max(0, c-1), min(c+2, columnas)):
                    if (i, j) not in visitados:
                        visitados.add((i, j))
                        if tablero[i][j] == 0:
                            queue.append((i, j))
                        elif tablero[i][j] > 0:
                            boton = botones[i][j]
                            boton.config(image=imagenes_numeros[tablero[i][j]], state=tk.DISABLED)
        return

# Función para reiniciar el juego
def reiniciar_juego():
    global tablero, minas_coords
    tablero = [[0 for _ in range(columnas)] for _ in range(filas)]
    minas_coords = []
    colocar_minas()
    for i in range(filas):
        for j in range(columnas):
            boton = botones[i][j]
            boton.config(image="", state=tk.NORMAL)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Buscaminas")

# Crear los botones del tablero
botones = [[0 for _ in range(columnas)] for _ in range(filas)]
for i in range(filas):
    for j in range(columnas):
        boton = tk.Button(ventana, width=20, height=20,
                          command=lambda fila=i, columna=j: revelar_celda(fila, columna))
        boton.grid(row=i, column=j)
        botones[i][j] = boton

# Colocar las minas en el tablero
colocar_minas()

# Iniciar la ventana principal
ventana.mainloop()
