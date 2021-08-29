import cv2
import numpy

def main():
    license_cascade_file = f"{cv2.haarcascades} haarcascade_licence_plate_rus_16stages.xml"
    license_cascade = cv2.CascadeClassifier(license_cascade_file)

    image = cv2.imread("plate.jpg")

if __name__ == "__main__":
    main()