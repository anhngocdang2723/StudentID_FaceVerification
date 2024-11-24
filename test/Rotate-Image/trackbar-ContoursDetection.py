import cv2
import numpy as np
from stackImages import stackImages as sI

def empty(a):
    pass

def rotateImage(img, angle):
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h))
    return rotated

# Hàm lấy contour và cắt thẻ sinh viên, bao gồm cả tính góc xoay
def getContoursAndAngle(img, imgOriginal):
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    card_img = None
    angle = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
            aspectRatio = w / float(h)

            if len(approx) == 4 and 1.3 < aspectRatio < 2.0:
                # Tìm hình chữ nhật bao quanh và tính toán góc xoay
                rect = cv2.minAreaRect(cnt)
                angle = rect[2]  # Lấy góc xoay từ hình chữ nhật
                box = cv2.boxPoints(rect)
                box = np.intp(box)
                cv2.drawContours(imgOriginal, [box], 0, (0, 255, 0), 2)
                cv2.putText(imgOriginal, "ID Card", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                # Cắt ảnh thẻ sinh viên
                card_img = imgOriginal[y:y + h, x:x + w]
    return card_img, angle

def ensureHorizontalWithAngle(card_img, angle):
    if card_img.shape[0] < card_img.shape[1]:  #xoay nếu h<w
        angle = angle - 90  #đổi góc xoay
    return rotateImage(card_img, angle)


cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640, 240)
cv2.createTrackbar("Canny Lower", "TrackBars", 30, 255, empty)
cv2.createTrackbar("Canny Upper", "TrackBars", 100, 255, empty)
cv2.createTrackbar("Threshold1", "TrackBars", 150, 255, empty)
cv2.createTrackbar("Threshold2", "TrackBars", 255, 255, empty)

img = cv2.imread(r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\Rotate-Image\cropped_2.jpg")
img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)

while True:
    # Lấy giá trị từ trackbars
    canny_lower = cv2.getTrackbarPos("Canny Lower", "TrackBars")
    canny_upper = cv2.getTrackbarPos("Canny Upper", "TrackBars")
    threshold1 = cv2.getTrackbarPos("Threshold1", "TrackBars")
    threshold2 = cv2.getTrackbarPos("Threshold2", "TrackBars")

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)

    # Ngưỡng hóa ảnh
    _, imgThreshold = cv2.threshold(imgGray, threshold1, threshold2, cv2.THRESH_BINARY)

    # Dùng Canny để phát hiện cạnh
    imgCanny = cv2.Canny(imgBlur, canny_lower, canny_upper)

    # Lấy và cắt thẻ sinh viên từ contour, và lấy góc xoay
    imgContour = img.copy()  # Reset lại khung để vẽ khung mỗi lần lặp
    student_card, angle = getContoursAndAngle(imgCanny, imgContour)

    #imgStack = stackImages(0.5, ([img, imgGray, imgThreshold], [imgCanny, imgContour, np.zeros_like(img)]))
    imgStack = sI(0.7, ([img, imgCanny, imgContour]))

    cv2.imshow("Stacked Images", imgStack)

    if student_card is not None:
        # xoay ảnh theo góc
        student_card = ensureHorizontalWithAngle(student_card, angle)
        cv2.imshow("Student ID Card", student_card)
        cv2.imwrite(r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\resultTest\detected_NgocAnhIDCard.jpg", student_card)

    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()