import cv2
import numpy as np
from time import sleep


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

    # constants
    width_min = 80
    height_min = 80
    offset = 6
    point1 = 550
    delay = 60
    detec = []
    old_detec = []
    positions = []
    counter = caminhoes = 0

    cap = cv2.VideoCapture("video.mp4")
    knn_bg_sub = cv2.createBackgroundSubtractorKNN()

    while True:

        ret, frame1 = cap.read()
        tempo = float(1 / delay)
        sleep(tempo)
        grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(grey, (9,) * 2, 5)

        img_knn_sub = knn_bg_sub.apply(blur)

        dilate_matrix = np.ones((3,) * 2)
        # dilat_knn = cv2.dilate(img_knn_sub, dilate_matrix)

        # erode_knn = cv2.erode(img_knn_sub, dilate_matrix)

        kernel = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE,
            (7,) * 2,
        )
        # dilatada_knn = cv2.morphologyEx(erode_knn, cv2.MORPH_CLOSE, kernel)
        # dilatada_knn = cv2.morphologyEx(dilatada_knn, cv2.MORPH_CLOSE, kernel)
        dilatada_knn = cv2.morphologyEx(img_knn_sub, cv2.MORPH_OPEN, kernel)
        # blur_dilate = cv2.GaussianBlur(dilatada_knn, (9,) * 2, 5)

        # erode
        # erodedata_knn = cv2.morphologyEx(erode_knn, cv2.MORPH_CLOSE, kernel)
        # erodedata_knn = cv2.morphologyEx(erodedata_knn, cv2.MORPH_CLOSE, kernel)

        contours_knn, erode = cv2.findContours(
            dilatada_knn, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )

        # """
        # cv2.line(frame1, (25, point1), (1200, point1), (255, 127, 0), 3)
        for (i, c) in enumerate(contours_knn):
            (x, y, w, h) = cv2.boundingRect(c)
            validar_contours = (w >= width_min) and (h >= height_min)
            if not validar_contours:
                continue

            # cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            center = get_center(x, y, w, h)
            detec.append(center)
            cv2.circle(frame1, center, 4, (0, 0, 255), 13)
        # """

        for (i, cord) in enumerate(zip(detec, old_detec)):
            # diff_x = abs(cord[0]-cord[1])
            # diff_y = abs(cord[0][1]-cord[1][1])
            print(cord)
            # print(diff_y, diff_x)

        print("-" * 10)

        # set_info(detec)
        # show_info(frame1, frame1)

        # cv2.imshow("Video Original", frame1)
        # cv2.imshow("grey", grey)
        # cv2.imshow("dilate", dilatada_knn)
        # cv2.imshow("erode", erode_knn)
        # cv2.imshow("blur", blur)
        # cv2.imshow("img_knn_sub", img_knn_sub)

        if cv2.waitKey(1) in [ord("q"), 27, 13]:
            break

    cv2.destroyAllWindows()
    cap.release()


if __name__ == "__main__":
    main()
