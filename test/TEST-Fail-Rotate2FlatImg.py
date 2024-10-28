import cv2
import numpy as np

def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]  # Điểm trên bên trái
    rect[2] = pts[np.argmax(s)]  # Điểm dưới bên phải
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  # Điểm trên bên phải
    rect[3] = pts[np.argmax(diff)]  # Điểm dưới bên trái
    return rect

def get_warped_image(image, approx):
    # Sắp xếp các điểm
    rect = order_points(approx.reshape(4, 2))

    # Tính toán chiều cao và chiều rộng mới
    width_a = np.linalg.norm(rect[0] - rect[1])
    width_b = np.linalg.norm(rect[2] - rect[3])
    max_width = int(max(width_a, width_b))

    height_a = np.linalg.norm(rect[0] - rect[3])
    height_b = np.linalg.norm(rect[1] - rect[2])
    max_height = int(max(height_a, height_b))

    # Tạo điểm cho phép biến đổi
    dst = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]
    ], dtype="float32")

    # Tính ma trận biến đổi và thực hiện biến đổi
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (max_width, max_height))

    return warped

def update(val):
    # Cập nhật các điểm dựa trên giá trị từ thanh trackbar
    for i in range(4):
        approx[i][0][0] = cv2.getTrackbarPos(f'x{i}', 'Trackbar')
        approx[i][0][1] = cv2.getTrackbarPos(f'y{i}', 'Trackbar')
    warped_image = get_warped_image(image, approx)
    cv2.imshow("Warped Image", warped_image)

# Đường dẫn đến ảnh của bạn
image_path = r'D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\output\best_detected_object_20241028124447.jpg'  # Thay bằng đường dẫn của bạn
image = cv2.imread(image_path)

if image is None:
    raise ValueError("Không thể đọc ảnh từ đường dẫn: {}".format(image_path))

# Chuyển đổi sang ảnh đen trắng
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Làm mờ ảnh và phát hiện cạnh
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(blurred, 50, 150)

# Tìm contours
contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Tìm contour lớn nhất
largest_contour = max(contours, key=cv2.contourArea)

# Lấy bốn góc của contour lớn nhất
epsilon = 0.02 * cv2.arcLength(largest_contour, True)
approx = cv2.approxPolyDP(largest_contour, epsilon, True)

# Đảm bảo có đúng 4 góc
if len(approx) != 4:
    raise ValueError("Không tìm thấy 4 góc chính xác.")

# Khởi tạo cửa sổ và thanh trackbar
cv2.namedWindow("Trackbar")
for i in range(4):
    cv2.createTrackbar(f'x{i}', 'Trackbar', int(approx[i][0][0]), image.shape[1], update)
    cv2.createTrackbar(f'y{i}', 'Trackbar', int(approx[i][0][1]), image.shape[0], update)

# Hiển thị ảnh ban đầu và ảnh đã biến đổi lần đầu
cv2.imshow("Original Image", image)
warped_image = get_warped_image(image, approx)
cv2.imshow("Warped Image", warped_image)

cv2.waitKey(0)
cv2.destroyAllWindows()
