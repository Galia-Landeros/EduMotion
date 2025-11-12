import cv2 as cv

cap = cv.VideoCapture(1)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    ok, frame = cap.read()
    if not ok:
        break
    frame = cv.flip(frame, 1)  # espejo
    cv.imshow("Cam Sanity", frame)
    if cv.waitKey(1) & 0xFF == 27:  # ESC para salir
        break

cap.release()
cv.destroyAllWindows()
