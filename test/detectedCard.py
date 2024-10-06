import cv2

def detect_card(image_path):
    # Đọc ảnh gốc
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Áp dụng bộ lọc làm mờ để giảm nhiễu
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Áp dụng phát hiện cạnh với Canny
    edged = cv2.Canny(blurred, 50, 150)

    # Tìm các đường viền (contours)
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Tìm hình chữ nhật lớn nhất (giả sử đó là thẻ sinh viên)
    card_contour = None
    max_area = 0

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:  # Loại bỏ các vùng nhỏ không phải là thẻ
            # Kiểm tra xem có phải là hình dạng gần giống hình chữ nhật không
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            if len(approx) == 4:  # Nếu là hình chữ nhật
                if area > max_area:
                    card_contour = approx
                    max_area = area

    if card_contour is not None:
        # Vẽ đường viền thẻ sinh viên (tuỳ chọn)
        cv2.drawContours(image, [card_contour], -1, (0, 255, 0), 3)

        # Cắt ảnh thẻ dựa trên contour
        x, y, w, h = cv2.boundingRect(card_contour)
        student_card = image[y:y+h, x:x+w]

        # Hiển thị ảnh thẻ đã cắt
        cv2.imshow("Detected Student Card", student_card)
        cv2.waitKey(0)

        # Lưu ảnh thẻ đã cắt
        cv2.imwrite("student_card.jpg", student_card)
    else:
        print("Không tìm thấy thẻ sinh viên trong ảnh.")

# Gọi hàm detect_card
detect_card(r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\imgTest\NgocAnhIDCard.jpg")
