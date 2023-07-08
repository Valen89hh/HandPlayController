from tkinter import *
from Manos import Manos
import multiprocessing
import threading
import cv2
import pyautogui
import time

# crear la variables para almacenar los procesos
manos_process = None
ventana = None
terminate_process_hands = False
""" key_left_process = None
key_rigth_process = None """
key_up_process = None

press_left = False
press_right = False
press_up = False
press_down = False


# Creamos variables de control
scale_giro = None
scale_recto = None
scale_max_distance = None
scale_min_dinstance = None
check_left = None
check_right = None
check_up = None
check_down = None





# Funcion para detectar los cambios en las escalar y checkbox
def on_scale_angulo(value):
    print("Sacle: ", value)

def on_check_click_left():
    global check_left
    if check_left.get() == 1:
        print("Left: V")
    else:
        print("Left: F")



def press_key(key):
    for i in range(10):
        pyautogui.keyDown(key)
        time.sleep(0.001)
        pyautogui.keyUp(key)

def press_key_l():
    while not press_left: 
        pyautogui.keyDown('left')
        time.sleep(0.001)
        # pyautogui.keyUp('left')

        """ if l == True:
            print("Saliendo: l")
            break """
    pyautogui.keyUp('left')
    

def press_key_r():
    while not press_right:
        pyautogui.keyDown('right')
        time.sleep(0.001)
        # pyautogui.keyUp('right')

        """ if r == True:
            print("Saliendo: r")
            break """
    pyautogui.keyUp('right')
    
        
def press_key_up():
    print("LO INTENTE")
    while not press_up:
        print("presionando")
        pyautogui.keyDown('up')
        time.sleep(0.001)
        pyautogui.keyUp('up')

def press_key_donw():
    print("LO INTENTE down")
    while not press_down:
        print("presionando D")
        pyautogui.keyDown('down')
        time.sleep(0.001)
        pyautogui.keyUp('down')

        


# Proceso para reconocer las manos
def process_detection_hands(sc_value_giro, sc_value_recto, sc_max_distance, sc_min_distance,chc_value_left, chc_value_right, chc_value_up, chc_value_down):
    global press_left, press_right, press_up, press_down
    ejecutando_left = False
    ejecutando_right = False
    ejecutando_up = False
    ejecutando_down = False

    key_right_process = None
    key_left_process = None
    key_up_process = None
    key_down_process = None

    # Creamos nuestra video captura
    cap = cv2.VideoCapture(0)

    # Creamos nuestro reconocedor de manos
    manos = Manos()

    # Ancho y alto de la ventana
    ancho, alto = (600, 600)

    # Bucle principal
    while not terminate_process_hands:
        # Obtenemos la video captura
        ret, frame = cap.read()

        # redimencionamos la imagen
        frame = cv2.resize(frame, (ancho, alto), interpolation=cv2.INTER_AREA)
        # voltemao la imagen
        frame = cv2.flip(frame, 1)

        # Reconocemos las manos
        frame, puntos = manos.reconocer_mano(frame)

        if len(puntos) == 2:
            # print(puntos)
            d = manos.get_distance(puntos[0][0], puntos[0][12], dibujar=True)
            d2 = manos.get_distance(puntos[1][0], puntos[1][12], dibujar=True)

            grados = manos.calcular_angulo(puntos[0][0], puntos[1][0])
            
            # print(d)
            
            print("SCALE: ", chc_value_up)
            print(d < 50 and d2 < 50 and not ejecutando_up and chc_value_up == 1)
            if grados < -sc_value_giro and not ejecutando_left and chc_value_left == 1:
                press_left = False
                press_right = True
                print("Izquierda: -1")
                
                key_left_process = threading.Thread(target=press_key_l)
                key_left_process.start()
                ejecutando_left = True
                ejecutando_right = False
                
            
            elif grados > sc_value_giro and not ejecutando_right and chc_value_right == 1:
                print("Derecha: 1")
                """ if key_left_process:
                    key_left_process.terminate() """
                press_right = False
                press_left = True
                key_right_process = threading.Thread(target=press_key_r)
                key_right_process.start()
                ejecutando_right = True
                ejecutando_left = False
            
            if d < sc_min_distance and d2 < sc_min_distance and not ejecutando_up and chc_value_up == 1:
                print("Acelerar: 2")
                key_up_process = threading.Thread(target=press_key_up)
                key_up_process.start()
                ejecutando_up = True
                ejecutando_down = False
                press_down = True
                press_up = False


              
            
            if (d > sc_max_distance and d2 < sc_min_distance) or (d2 > sc_max_distance and d < sc_min_distance):

                if not ejecutando_down and chc_value_down == 1:
                    print("Retroceder: 3")
                    key_down_process = threading.Thread(target=press_key_donw)
                    key_down_process.start()
                    press_up = True
                    press_down = False
                    ejecutando_down = True
                    ejecutando_up = False

            if d > sc_max_distance and d2 > sc_max_distance:
                print("LO TERMINE")
                press_up = True
                press_down = True
                ejecutando_up = False
                ejecutando_down = False  

            if -sc_value_recto <= grados < sc_value_recto:
                # print("recto: 0")
                ejecutando_left = False
                ejecutando_right = False
                press_right = True
                press_left = True
        
        # Mostramos la imagen
        cv2.imshow("Manos", frame)


        # Salimos
        t = cv2.waitKey(1)
        if t == 27:
            break
    
    # Libreamos la video captura
    cap.release()
    # Cerramos la ventana
    cv2.destroyAllWindows()


# Funcion para iniciar el procesos
def start_process():
    global manos_process, terminate_process_hands, ejecutando_left, ejecutando_right, scale_giro, scale_recto, check_left, check_right, check_up, check_down, scale_max_distance, scale_min_dinstance

    terminate_process_hands = False

    try:
        if not manos_process.is_alive():
            print("------- INICIANDO PROCESOS (PROCESS) ----------")
            manos_process = multiprocessing.Process(target=process_detection_hands, args=(int(scale_giro.get()), int(scale_recto.get()), int(scale_max_distance.get()), int(scale_min_dinstance.get()), check_left.get(), check_right.get(), check_up.get(), check_down.get()))
            manos_process.start()
        else:
            print("El proceso en ejecucion")
    except:
        print("------- INICIANDO PROCESOS (NONE) ----------")
        manos_process = multiprocessing.Process(target=process_detection_hands, args=(int(scale_giro.get()), int(scale_recto.get()), int(scale_max_distance.get()), int(scale_min_dinstance.get()), check_left.get(), check_right.get(), check_up.get(), check_down.get()))
        manos_process.start()


# Funcion para detener los procesos
def end_process():
    global manos_process, terminate_process_hands

    if manos_process is not None:
        print("------- TERMINATE PROCESS HANDS --------")
        manos_process.terminate()
        manos_process.join()
        terminate_process_hands = True
    else:
        print("El proceso no ha sido iniciado")

def cerrar_procesos():
    end_process()
    ventana.destroy()


# Funcion principal para la interfaz de usuario
def start_tkinter():
    global ventana
    # Creamos nuestra ventana
    ventana = Tk()


    button = Button(ventana, text="Ejecutar", command=start_process)
    button.pack()

    stop_button = Button(ventana, text="Detener", command=end_process)
    stop_button.pack()

    ventana.protocol("WM_DELETE_WINDOW", cerrar_procesos)

    ventana.mainloop()

def new_tk():
    global ventana, scale_giro, scale_recto, check_left, check_right, check_up, check_down, scale_max_distance, scale_min_dinstance

    # Crear la ventana principal
    ventana =  Tk()

    scale_giro = StringVar()
    scale_recto = StringVar()
    scale_max_distance = StringVar()
    scale_min_dinstance = StringVar()
    check_left = IntVar()
    check_right = IntVar()
    check_up = IntVar()
    check_down = IntVar()

    check_left.set(1)
    check_right.set(1)
    check_up.set(1)
    check_down.set(1)
    scale_recto.set("10")
    scale_giro.set("50")
    scale_max_distance.set("70")
    scale_min_dinstance.set("50")


    # Crear un frame para agrupar los elementos del título
    title_frame =  Frame(ventana)
    title_frame.pack()

    # Crear el label para el título
    title_label =  Label(title_frame, text="Play handas", font=("Arial", 16, "bold"))
    title_label.pack()

    # Crear un frame para agrupar los elementos de los botones
    buttons_frame =  Frame(ventana)
    buttons_frame.pack()

    # Crear los botones "Iniciar Juego" y "Detener Juego"
    start_button =  Button(buttons_frame, text="Iniciar Juego", command=start_process)
    start_button.grid(row=0, column=0, padx=10, pady=5)

    stop_button =  Button(buttons_frame, text="Detener Juego", command=end_process)
    stop_button.grid(row=0, column=1, padx=10, pady=5)

    # Crear un frame para agrupar los elementos de la sensibilidad y el ángulo
    sensitivity_frame =  Frame(ventana)
    sensitivity_frame.pack()

    # Crear el label "Sensibilidad"
    sensitivity_label =  Label(sensitivity_frame, text="Sensibilidad")
    sensitivity_label.grid(row=0, column=0, padx=10, pady=5)

    # Crear el entry para la sensibilidad
    sensitivity_entry =  Scale(sensitivity_frame, from_=0, to=100, orient=HORIZONTAL, variable=scale_giro, command=on_scale_angulo)
    sensitivity_entry.grid(row=0, column=1, padx=10, pady=5)

    # Crear el label "Angulo"
    angle_label =  Label(sensitivity_frame, text="Angulo")
    angle_label.grid(row=0, column=2, padx=10, pady=5)

    # Crear el entry para el ángulo
    angle_entry =  Scale(sensitivity_frame, from_=0, to=20, orient=HORIZONTAL, variable=scale_recto)
    angle_entry.grid(row=0, column=3, padx=10, pady=5)

    # Crear el label "Sensibilidad"
    sensitivity_max_lbl =  Label(sensitivity_frame, text="Max Distance")
    sensitivity_max_lbl.grid(row=1, column=0, padx=10, pady=5)

    # Crear el entry para la maxima distancia
    sensitivity_max_scale =  Scale(sensitivity_frame, from_=30, to=100, orient=HORIZONTAL, variable=scale_max_distance)
    sensitivity_max_scale.grid(row=1, column=1, padx=10, pady=5)

    # Crear el label "Min Distance"
    sensitivity_min_lbl =  Label(sensitivity_frame, text="Min Distance")
    sensitivity_min_lbl.grid(row=1, column=2, padx=10, pady=5)

    # Crear el entry para la maxima distancia
    sensitivity_min_scale =  Scale(sensitivity_frame, from_=0, to=70, orient=HORIZONTAL, variable=scale_min_dinstance)
    sensitivity_min_scale.grid(row=1, column=3, padx=10, pady=5)

    # Crear un frame para agrupar los elementos de los botones de activación
    activation_buttons_frame =  Frame(ventana)
    activation_buttons_frame.pack()

    # Crear los botones de activación
    left_button =  Checkbutton(activation_buttons_frame, text="left", variable=check_left, command=on_check_click_left)
    left_button.grid(row=0, column=0, padx=10, pady=5)

    right_button =  Checkbutton(activation_buttons_frame, text="Right", variable=check_right)
    right_button.grid(row=0, column=1, padx=10, pady=5)

    up_button =  Checkbutton(activation_buttons_frame, text="Up", variable=check_up)
    up_button.grid(row=0, column=2, padx=10, pady=5)

    down_button =  Checkbutton(activation_buttons_frame, text="Down", variable=check_down)
    down_button.grid(row=0, column=3, padx=10, pady=5)


    ventana.protocol("WM_DELETE_WINDOW", cerrar_procesos)

    # Ejecutar el bucle principal de la aplicación
    ventana.mainloop()


# incio del programa
if __name__ == "__main__":
    # start_tkinter()
    new_tk()
