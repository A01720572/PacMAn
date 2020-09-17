"""Pacman, classic arcade game.

Exercises

1. Change the board.
2. Change the number of ghosts.
3. Change where pacman starts.
4. Make the ghosts faster/slower.
5. Make the ghosts smarter.

"""

from random import choice
from turtle import *
from freegames import floor, vector

state = {'score': 0} #Puntaje inicial del pacman (cuántas bolitas se come)
path = Turtle(visible=False)
writer = Turtle(visible=False)
aim = vector(5, 0)
pacman = vector(-40, -80) #Posición del pacman inicial
ghosts = [ #Posiciones iniciales de los fantasmas
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]
tiles = [ #Tablero: los 1 representan los espacios en donde el pacman se puede mover y los 0 son los espacios en el vacío
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0,
    0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

def square(x, y): #Función para dibujar un cuadrado que servirá para dibujar todo el tablero del juego
    "Draw square using path at (x, y)."
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()

def offset(point): #Función para posicionar los puntos, pacman y fantasmas, ajustando sus coordenadas para que queden dentro del path
    "Return offset of point in tiles."
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index

def valid(point): #Función que delimita el path: cuando el pacman o un fantasma lleguen a una posición del tablero en 0, estos toparán
    "Return True if point is valid in tiles."
    index = offset(point)

    if tiles[index] == 0:
        return False

    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0

def world(): #Función que colorea el tablero
    "Draw world using path."
    bgcolor('black') #El color del fondo será negro
    path.color('blue') #El color del path (donde las figuras sí se pueden mover) será azul

    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0: #En caso de que el pacman haya comido un punto, se vuelve a dibujar un cuadrado para quitar el punto
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y) #Dibuja un cuadrado con las coordenadas y la función square()

            if tile == 1: #Si la posición del tablero es 1, se le agregan unos puntos blancos (la comida del pacman)
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')

def move():
    "Move pacman and all ghosts."
    writer.undo()
    writer.write(state['score'])

    clear()
    
    if valid(pacman + aim): #Si no topa con los espacios en negro, el pacman se seguirá moviendo
        pacman.move(aim)

    index = offset(pacman)

    if tiles[index] == 1: #Si llega a un espacio en donde hay comida:
        tiles[index] = 2 #Ahora ese espacio tendrá el valor de 2 porque no es un espacio negro, pero tampoco uno que contiene comida
        state['score'] += 1 #Se aumenta un punto al puntaje
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y) #Se vuelve a dibujar el cuadrado para cubrir el punto blanco

    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow') #El dot es la figura del pacman

    for point, course in ghosts: #Los fantasmas se irán moviendo
        if valid(point + course): #Siempre y cuando estén dentro del path
            point.move(course)
            
        else: #Si topan tienen 4 opciones de cambio de dirección
            options = [
                vector(15, 0),#Para que los fantasmas sean mas rápidos se decidió cambiar los vectores de 5 a 15 para que cuanto topen se muevan distancias más largas en el mismo tiempo
                vector(-15, 0),
                vector(0, 15),
                vector(0, -15),
            ]
            plan = choice(options)
            #Las siguientes condiciones buscan en cuál cuadrante del tablero está el pacman
            #Se decide hacia donde girará el fantasma cuando tope:
            if ((pacman.x > 0 and course.x > 0) or (pacman.x < 0 and course.x < 0)) and pacman.y > 0:
                plan = vector(0, 15)
                if plan == course: #En caso de que se vuelva a repetir la direccion de donde viene, se genera una nueva
                    plan = choice(options) #choice() es una función que escoge una de las cuatro opciones de vectores
            elif ((pacman.x > 0 and course.x > 0) or (pacman.x < 0 and course.x < 0)) and pacman.y < 0:
                plan = vector(0, -15)
                if plan == course:
                    plan = choice(options)
            elif ((pacman.y > 0 and course.y > 0) or (pacman.y < 0 and course.y < 0)) and pacman.x > 0:
                plan = vector(15, 0)
                if plan == course:
                    plan = choice(options)
            elif ((pacman.y > 0 and course.y > 0) or (pacman.y < 0 and course.y < 0)) and pacman.x < 0:
                plan = vector(-15, 0)
                if plan == course:
                    plan = choice(options)
            #Así, los fantasmas se moverán al cuadrante en donde se encuentra el pacman y lo podrán perseguir de cierta manera
            course.x = plan.x #Se actualiza la direccion en la que se moverán los fantasmas
            course.y = plan.y

        up()
        goto(point.x + 10, point.y + 10)
        dot(20, 'red') #El dot rojo es la figura que representa a los fantasmas

    update()

    for point, course in ghosts: #Si un fantasma topa con el pacman el juego se termina
        if abs(pacman - point) < 20:
            return

    ontimer(move, 100)

def change(x, y): #Función que cambia la dirección en la que se mueve el pacman, si se encuentra dentro del path
    "Change pacman aim if valid."
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y

setup(420, 420, 370, 0) #Establece el tamaño de la ventana del juego
hideturtle()
tracer(False)
writer.goto(160, 160)
writer.color('white') #El puntaje se imprime de color blanco
writer.write(state['score'])
listen()
onkey(lambda: change(5, 0), 'Right') #Para mover al pacman con las teclas
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')
world()
move()
done()
