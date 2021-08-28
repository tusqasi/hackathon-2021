import cv2
import dlib
import time
import math


carCascade = cv2.CascadeClassifier("vech.xml")
video_file_name = "video.mp4"
video = cv2.VideoCapture(video_file_name)

WIDTH = 1280
HEIGHT = 720

speed_limit = 30


def warn_show(image, speed, x1, y1, w1, h1):
    cv2.putText(
        image,
        f"WARNING",
        (int(x1 + w1 / 2), int(y1 - 15)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (0, 0, 100),
        4,
    )
    cv2.putText(
        image,
        f"{speed} km/h",
        (int(x1 + w1 / 2), int(y1 - 5)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (0, 0, 100),
        2,
    )


def estimateSpeed(location1, location2):
    d_pixels = math.sqrt(
        math.pow(location2[0] - location1[0], 2)
        + math.pow(location2[1] - location1[1], 2)
    )
    # ppm = location2[2] / carWidht
    ppm = 8
    d_meters = d_pixels / ppm
    fps = 29
    speed = d_meters * fps * 3.6
    return speed


def trackMultipleObjects():
    rectangleColor = (0, 255, 0)
    frameCounter = 0
    currentCarID = 0
    fps = 0

    carTracker = {}
    carNumbers = {}
    carLocation1 = {}
    carLocation2 = {}
    speed = [None] * 100

    while True:
        start_time = time.time()
        rc, image = video.read()
        if type(image) == type(None):
            break
        resultImage = image.copy()

        frameCounter = frameCounter + 1
        carIDtoDelete = []

        for carID in carTracker.keys():
            trackingQuality = carTracker[carID].update(image)

            if trackingQuality < 7:
                carIDtoDelete.append(carID)

        for carID in carIDtoDelete:

            carTracker.pop(carID, None)
            carLocation1.pop(carID, None)
            carLocation2.pop(carID, None)

        if not (frameCounter % 10):
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cars = carCascade.detectMultiScale(gray, 1.1, 13, 18, (24, 24))

            for (_x, _y, _w, _h) in cars:
                x = int(_x)
                y = int(_y)
                w = int(_w)
                h = int(_h)

                x_bar = x + 0.5 * w
                y_bar = y + 0.5 * h

                matchCarID = None

                for carID in carTracker.keys():
                    trackedPosition = carTracker[carID].get_position()

                    t_x = int(trackedPosition.left())
                    t_y = int(trackedPosition.top())
                    t_w = int(trackedPosition.width())
                    t_h = int(trackedPosition.height())

                    t_x_bar = t_x + 0.5 * t_w
                    t_y_bar = t_y + 0.5 * t_h

                    if (
                        (t_x <= x_bar <= (t_x + t_w))
                        and (t_y <= y_bar <= (t_y + t_h))
                        and (x <= t_x_bar <= (x + w))
                        and (y <= t_y_bar <= (y + h))
                    ):
                        matchCarID = carID

                if matchCarID is None:
                    tracker = dlib.correlation_tracker()
                    tracker.start_track(image, dlib.rectangle(x, y, x + w, y + h))

                    carTracker[currentCarID] = tracker
                    carLocation1[currentCarID] = [x, y, w, h]

                    currentCarID = currentCarID + 1

        for carID in carTracker.keys():
            trackedPosition = carTracker[carID].get_position()

            t_x = int(trackedPosition.left())
            t_y = int(trackedPosition.top())
            t_w = int(trackedPosition.width())
            t_h = int(trackedPosition.height())

            cv2.rectangle(
                resultImage, (t_x, t_y), (t_x + t_w, t_y + t_h), rectangleColor, 4
            )

            carLocation2[carID] = [t_x, t_y, t_w, t_h]

        end_time = time.time()

        if not (end_time == start_time):
            fps = 1 / (end_time - start_time)

        for i in carLocation1.keys():
            if frameCounter % 1 == 0:
                [x1, y1, w1, h1] = carLocation1[i]
                [x2, y2, w2, h2] = carLocation2[i]

                carLocation1[i] = [x2, y2, w2, h2]

                if [x1, y1, w1, h1] != [x2, y2, w2, h2]:
                    if (
                        speed[i] == None or speed[i] == 0
                    ):  # and y1 >= 275 and y1 <= 285:
                        speed[i] = estimateSpeed(
                            [
                                x1,
                                y1,
                            ],
                            [
                                x1,
                                y2,
                            ],
                        )

                    if speed[i] >= speed_limit:
                        (int(x1 + w1 / 2), int(y1 - 5)),
                    elif speed[i] != None:
                        cv2.putText(
                            resultImage,
                            str(int(speed[i])) + "km/h",
                            (int(x1 + w1 / 2), int(y1 - 5)),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.75,
                            (0, 0, 100),
                            2,
                        )
        cv2.imshow("result", resultImage)

        # out.write(resultImage)

        if cv2.waitKey(1) == ord("q"):
            break

    cv2.destroyAllWindows()
    # out.release()


if __name__ == "__main__":
    trackMultipleObjects()