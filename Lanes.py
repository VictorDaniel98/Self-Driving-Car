import cv2
import numpy as np
#import matplotlib.pyplot as plt

def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1*(3/5))
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return np.array([x1,y1,x2,y2])

def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1,y1,x2,y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    left_line = make_coordinates(image, left_fit_average)
    right_line = make_coordinates(image, right_fit_average)
    return np.array([left_line, right_line])
    #print('left', left_fit_average)
    #print('right', right_fit_average)


def canny(image):
    #escala de grises para la copia
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    #Difumar la imagen en escala de grises para remover el ruido generado por
    #la variacion de la intensidad de luz
    #-Este metodo es opcional si se implementa la funcion Canny ya que este
    #detecta Bordes como tal y ya viene incluido una difuminacion Gaussiana
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    #detecta los bordes tras aplicar una escala de grises y difuminacion gaussiana
    # en la misma funcion
    canny=cv2.Canny(blur, 50, 150)
    return canny

def display_lines(image, lines):
    line_image=np.zeros_like(image)
    if lines is not None:
        for x1,y1,x2,y2 in lines:
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)
            return line_image


#metodo implementado para obtener valores unicamente del area encerrada
#con el fin de reducir la cantidad de calculos
def region_of_interest(image):
    height = image.shape[0]
    width = image.shape[1]
    polygon = np.array([[(200, height), (1100, height), (550, 250)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygon, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image
#imagen Para trabajar
image = cv2.imread('road.jpg')
#Copia de imagen
lane_image = np.copy(image)

#canny_image = canny(lane_image)
#cropped_image = region_of_interest(canny_image)
#lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 50, np.array([]), minLineLength = 40, maxLineGap=5)
#averaged_lines = average_slope_intercept(lane_image, lines)
#line_image = display_lines(lane_image, averaged_lines)
#combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)
#mostrar imagen original
#-cv2.imshow('Original', lane_image)
#mostrar imagen en escala de grises
#---cv2.imshow('GrayScale', gray)
#mostrar imagen con la difuminacion Gaussiana
#---cv2.imshow('Blur', blur)
#mostrar image con deteccion de Bordes canny
#cv2.imshow('Canny', combo_image)
#Esperar una tecla para salir
#cv2.waitKey(0)
#altern method
#plt.imshow(canny)
#plt.show()
cap = cv2.VideoCapture("test2.mp4")
while(cap.isOpened()):
    _,frame = cap.read()
    canny_image = canny(frame)
    cropped_image = region_of_interest(canny_image)
    lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength = 40, maxLineGap=5)
    averaged_lines = average_slope_intercept(frame, lines)
    line_image = display_lines(frame, averaged_lines)
    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    cv2.imshow('Canny', combo_image)
    #Esperar una tecla para salir
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
