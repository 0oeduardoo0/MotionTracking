import numpy as np
import cv2
import time
import serial

def nothing(x):
    pass

s = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)   #esperamos que se inicialize

# Creamos una variable de camara y asigamos la primera camara disponible con "0"
cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)
cap_height = int( cap.get( cv2.cv.CV_CAP_PROP_FRAME_HEIGHT ) )
cap_width = int( cap.get( cv2.cv.CV_CAP_PROP_FRAME_WIDTH ) )
 
print "Connection to: %s" %( s.name )

# Crearemos los controles para indicar el color que seguiremos
cv2.namedWindow('Configuracion') 
cv2.createTrackbar ('H min', 'Configuracion', 22,256,nothing)
cv2.createTrackbar ('H max', 'Configuracion', 30,256,nothing)
cv2.createTrackbar ('S min', 'Configuracion', 90,256,nothing)
cv2.createTrackbar ('S max', 'Configuracion', 221,256,nothing)
cv2.createTrackbar ('V min', 'Configuracion', 0,256,nothing)
cv2.createTrackbar ('V max', 'Configuracion', 237,256,nothing)
cv2.createTrackbar ('Sens',  'Configuracion', 15, 40, nothing)
 
# Iniciamos el bucle de captura, en el que leemos cada frame de la captura

GLOBAL_X = 0
GLOBAL_Y = 0

while(True):
    ret, frame = cap.read()
    ret2, moni = cap2.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #Convertimos imagen a HSV
 
    # Asignamos las variables del rango de color que seguiremos
    Hmin = cv2.getTrackbarPos('H min', 'Configuracion')
    Hmax = cv2.getTrackbarPos('H max', 'Configuracion')
    Smin = cv2.getTrackbarPos('S min', 'Configuracion')
    Smax = cv2.getTrackbarPos('S max', 'Configuracion')
    Vmin = cv2.getTrackbarPos('V min', 'Configuracion')
    Vmax = cv2.getTrackbarPos('V max', 'Configuracion')
    Sens = cv2.getTrackbarPos('Sens', 'Configuracion')
 
    # Aqui mostramos la imagen en blanco o negro segun el rango de colores.
    bn_img = cv2.inRange(hsv, np.array((Hmin,Smin,Vmin)), np.array((Hmax,Vmax,Smax)))
 
    # Limpiamos la imagen de imperfecciones con los filtros erode y dilate
    bn_img = cv2.erode (bn_img,cv2.getStructuringElement(cv2.MORPH_RECT,(3,3)),iterations = 1)
    bn_img = cv2.dilate (bn_img,cv2.getStructuringElement(cv2.MORPH_RECT,(5,5)),iterations = 1)
    # Localizamos la posicion del objeto
    M = cv2.moments(bn_img)
    if M['m00'] > 50000:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        
        #Diferente del valor inicial
        cmd = ""
        if GLOBAL_X != 0 and GLOBAL_Y != 0:
            # Debe de exitir una diferencia de 20px
            steep = cx - GLOBAL_X
            if steep > Sens:
                cmd = cmd + "L"
                s.write("L")
            elif steep < -Sens:
                cmd = cmd + "R"
                s.write("R")
            steep = cy - GLOBAL_Y
            if steep > Sens:
                cmd = cmd + "D"
                s.write("D")
            elif steep < -Sens:
                cmd = cmd + "U"
                s.write("U")

        GLOBAL_X, GLOBAL_Y = cx, cy
    
        # Mostramos un circulo verde en la posicion en la que se encuentra el objeto
        cv2.line ( frame, ( cx, 0 ), ( cx, cap_height ), ( 0, 255, 0 ) )
        cv2.line ( frame, ( 0, cy ), ( cap_width, cy ), ( 0, 255, 0 ) )
    
    else:

        GLOBAL_X, GLOBAL_Y = 0, 0
 
 
    # Creamos las ventanas de salida y configuracion
    cv2.imshow('Scan', frame)
    cv2.imshow('InRange', bn_img)
    cv2.imshow('Monitor', moni)
 
    if cv2.waitKey(1) & 0xFF == ord('q'): # Indicamos que al pulsar "q" el programa se cierre
        break

cap.release()
cv2.destroyAllWindows()
