# Right-click on python.exe, Properties, Compatibility, High DPI Settings
# Check "Override high DPI scaling behavior."

# Edit time_bound to contain the (X1, Y1, X2, Y2) coordinates of date/time.

import pyscreenshot
import pytesseract
import cv2
import numpy
import argparse

def main():
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

    parser = argparse.ArgumentParser()
    # parser.add_argument('-s', action='store', dest='hostname', help='host IP address', default='0.0.0.0' )
    parser.add_argument('--health', action='store_true', dest='_health', help='health test flag', default='False')
    parser.add_argument('--time', action='store_true', dest='_time', help='time test flag', default='False')
    options = vars(parser.parse_args())

    # Load a color image in gray scale
    # Reads health bar as white text on gray background ...
    # ... or reads date/time as white text on black background
    # Use binary-threshold to color as white on black
    # Invert colors (black on white background)

    if options['_health'] == True:
        getHealth()
    if options['_time'] == True:
        getTime()

def getHealth():
    health_bar = cv2.imread('Screenshot_3.png', cv2.IMREAD_GRAYSCALE)
    retval, health_bar = cv2.threshold(health_bar, 250, 255, cv2.THRESH_BINARY)
    health_bar = cv2.bitwise_not(health_bar)
    cv2.imshow('image', health_bar)
    strRead = pytesseract.image_to_string(health_bar, config='--psm 6')
    health = float(strRead)
    print(health)
    cv2.waitKey(0)

def getTime():
    time_bound = (1740,1020,1838,1076)
    dt = pyscreenshot.grab(bbox=time_bound) # Local time on task bar.
    dt = numpy.array(dt) # or you can save the file with: im.save('img.png'), and then open it in grayscale
    retval, dt = cv2.threshold(dt, 200, 255, cv2.THRESH_BINARY)
    dt = cv2.bitwise_not(dt)
    cv2.imshow('image', dt)
    strRead = pytesseract.image_to_string(dt, config='--psm 6')
    print(strRead)
    cv2.waitKey(0)

if __name__ == '__main__':
    main()

    