import cv2
import numpy as np
from time import sleep
from constantes import *


def get_center(x, y, width, height):
    return (width // 2 + x, height // 2 + y)


def set_info(detec):
    global counter
    for (x, y) in detec:
        if (point1 + offset) > y > (point1 - offset):
            counter += 1
            cv2.line(frame1, (25, point1), (1200, point1), (0, 127, 255), 3)
            detec.remove((x, y))
            print("counting the number of car: " + str(counter))


def show_info(frame1, dilatada):
    text = f"Counter: {counter}"
    cv2.putText(
        frame1,
        text,
        (450, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (0, 0, 255),
        5,
    )
    cv2.imshow("Video Original", frame1)
    cv2.imshow("Detectar", dilatada)


global counter
counter = 0


def main():
    counter = caminhoes = 0
    cap = cv2.VideoCapture("video.mp4")
    knn_bg_sub = cv2.createBackgroundSubtractorKNN()
    mog2_bg_sub = cv2.createBackgroundSubtractorMOG2()
    while True:
        ret, frame1 = cap.read()

        tempo = float(1 / delay)
        sleep(3.0)

        grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(grey, (3,) * 2, 5)

        img_knn_sub = knn_bg_sub.apply(blur)

        dilate_matrix = np.ones((3,) * 2)
        dilat_knn = cv2.dilate(img_knn_sub, dilate_matrix)

        kernel = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE,
            (3,) * 2,
        )
        dilatada_knn = cv2.morphologyEx(dilat_knn, cv2.MORPH_CLOSE, kernel)
        dilatada_knn = cv2.morphologyEx(dilatada_knn, cv2.MORPH_CLOSE, kernel)

        contours_knn, img_knn = cv2.findContours(
            dilatada_knn, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )
        print(contours_knn)

        # """
        # cv2.line(frame1, (25, point1), (1200, point1), (255, 127, 0), 3)
        for (i, c) in enumerate(contours_knn):
            (x, y, w, h) = cv2.boundingRect(c)
            validar_contours = (w >= width_min) and (h >= height_min)
            if not validar_contours:
                continue

            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            center = get_center(x, y, w, h)
            detec.append(center)
            cv2.circle(frame1, center, 4, (0, 0, 255), -1)
        # """

        # set_info(detec)
        # show_info(frame1, frame1)

        # cv2.imshow("Video Original", frame1)
        # cv2.imshow("grey", grey)
        # cv2.imshow("knn_dilata", dilatada_knn)
        # cv2.imshow("blur", blur)
        # cv2.imshow("img_knn_sub", img_knn_sub)

        if cv2.waitKey(1) == ord("q"):
            break

    cv2.destroyAllWindows()
    cap.release()


if __name__ == "__main__":
    main()
