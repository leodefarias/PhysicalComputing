from math import dist
import numpy as np
import dlib
import cv2

def happiness_detector(mouth):
    A = dist(mouth[1], mouth[5])
    B = dist(mouth[2], mouth[4])

