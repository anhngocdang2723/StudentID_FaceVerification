import cv2
import numpy as np

# Hàm lấy contour và cắt thẻ sinh viên
def getContours(img, imgOriginal):
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:  # Điều chỉnh ngưỡng area để tìm chính xác hơn
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
            aspectRatio = w / float(h)
            
            # Kiểm tra nếu hình có 4 đỉnh và tỷ lệ khung hình trong phạm vi thẻ sinh viên
            if len(approx) == 4 and 1.3 < aspectRatio < 2.0:  # Mở rộng khoảng tỷ lệ
                cv2.drawContours(imgOriginal, [approx], -1, (0, 255, 0), 2)
                cv2.putText(imgOriginal, "ID Card", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                # Cắt ảnh thẻ sinh viên
                card_img = imgOriginal[y:y+h, x:x+w]
                return card_img
    return None

# Đọc ảnh và xử lý
img = cv2.imread(r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\imgTest\z5903394151288_49235aed016f400877949e1d25163e52.jpg")
img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)  # Resize nhẹ lại để dễ xử lý hơn
imgContour = img.copy()

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
imgCanny = cv2.Canny(imgBlur, 30, 100)  # Điều chỉnh ngưỡng để bắt cạnh tốt hơn

# Lấy thẻ sinh viên từ contour
student_card = getContours(imgCanny, imgContour)

if student_card is not None:
    cv2.imshow("Student ID Card", student_card)
    cv2.imwrite(r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\output\student_card.jpg", student_card)
else:
    print("Không tìm thấy thẻ sinh viên.")

cv2.waitKey(0)
cv2.destroyAllWindows()
