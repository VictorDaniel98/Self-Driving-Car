import cv2
import numpy as np
#import matplotlib.pyplot as plt

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    
    
    def make_coordinates(image, line_parameters):
        if str(type(line_parameters)) == "<class 'numpy.float64'>":
            return np.array([0, 0, 0, 0])
        else:
            slope, intercept = line_parameters
            y1 = image.shape[0]
            y2 = int(y1*(3/5))
            x1 = int((y1 - intercept)/slope)
            x2 = int((y2 - intercept)/slope)
            return np.array([x1, y1, x2, y2])

    def average_slope_intercept(image, lines):
        left_fit = []
        right_fit = []
        
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line.reshape(4)
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
            
            if (np.any(left_line > 1000) or np.any(right_line > 1000)) is True:
                left_line = np.zeros(1, 4)
                right_line = np.zeros(1, 4)

        else:
            left_line = None
            right_line = None
        
        return np.array([left_line, right_line])


    def canny(image):
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        canny = cv2.Canny(blur, 50, 150)
        return canny
    
    def display_lines(image, lines):
        line_image = np.zeros_like(image)
        if lines[0] is not None and lines[1] is not None:
            for x1, y1, x2, y2 in lines:
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
        return line_image
    
    def region_of_interest(image):
        height = image.shape[0]
        width = image.shape[1]
        polygons = np.array([
            [(0, 350), (0, height), (width, height), (width, 350)]
            ])
        mask = np.zeros_like(image)
        cv2.fillPoly(mask, polygons, 255)
        masked_image = cv2.bitwise_and(image, mask)
        return masked_image
    
    lane_image = np.copy(frame)
    canny_image = canny(lane_image)
    cropped_image = region_of_interest(canny_image)
    lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 80, np.array([]), minLineLength=60, maxLineGap=5)
    averaged_lines = average_slope_intercept(lane_image, lines)
    line_image = display_lines(lane_image, averaged_lines)
    combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)
    
    cv2.imshow("Result2", combo_image)
    #cv2.imshow("Frame", frame)
    #cv2.imshow("Canny", canny)
    
    
    key = cv2.waitKey(1)
    if key == 27:
        break
    
cap.release()
cv2.destroyAllWindows()