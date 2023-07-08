# Importamos la librerias necesarias
import cv2
import mediapipe as mp
import math
import warnings

class Manos():
    """ 
     Clase que nos permite reconocer las manos de los usuario
     Obtener los puntos claves
     Realizar operaciones de distancia
    """

    # Inicializamos nuestra propiedades para reconocer las manos
    def __init__(self, mode=False, maxManos=2, minConfidence=0.5):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=mode, max_num_hands=maxManos, min_detection_confidence=minConfidence)
        
        self.imagen = None


    # Funcion para dibujar los puntos de la mano
    def reconocer_mano(self, frame, dibujar=True):
        # Ancho y alto
        self.ancho = frame.shape[1]
        self.alto = frame.shape[0]
        self.imagen = frame
        self.puntos_manos = list()
        puntos = list()
        # Convertimos la imagen formato RGB
        img_rgb = cv2.cvtColor(frame, cv2.  COLOR_BGR2RGB)

        # Procesamos la imagen de las manos
        self.results = self.hands.process(img_rgb)

        # Verificamos que se hayan reconocido manos
        if self.results.multi_hand_landmarks:
            # print("Se decteo mano")
            for hand_landmarks in self.results.multi_hand_landmarks:
                # Dibujamos las puntos claves de las manos
                if dibujar:
                    self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                # Obtenemos los puntos claves
                for idx, landmark in enumerate(hand_landmarks.landmark):
                    x,y = int(landmark.x*self.ancho), int(landmark.y*self.alto)
                    puntos.append((x,y))
        
                self.puntos_manos.append(puntos)
                puntos = []
        
        return frame, self.puntos_manos
    
    def get_distance(self, ptDedo1, ptDedo2, dibujar=False):
        # Aplicamos la formula de la distancia
        # d = (x2-x1)**2 + (y2-y1)**2
        x1, y1 = ptDedo1
        x2, y2 = ptDedo2

        d = math.sqrt((x2-x1)**2 + (y2-y1)**2)

        if dibujar:
            if self.imagen is not None:
                cv2.line(self.imagen, ptDedo1, ptDedo2, (0,255,0), 2)
            else:
                warnings.warn("No se ha detectado ninguna una mano")
                warnings.warn("NOTA: utiliza primero el metodo reconocer_mano() para obtener los puntos claves")
        return d
    
    def calcular_angulo(self, pt1, pt2):
        try:
            x1, y1 = pt1
            x2, y2 = pt2 
            dx = x2 - x1
            dy = y2 - y1
            angulo_rad = math.atan(dy / dx)
            angulo_deg = math.degrees(angulo_rad)
            return angulo_deg
        except:
            print("Hubo un error en el caluculo")
            return 0