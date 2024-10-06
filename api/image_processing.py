import cv2
import numpy as np
import os

PROCESSED_FOLDER = "processed_images"  # Thư mục để lưu ảnh xử lý

def adjust_brightness_contrast(image, brightness=0, contrast=0):
    brightness = np.clip(brightness, -100, 100)
    contrast = np.clip(contrast, -100, 100)

    # Điều chỉnh độ sáng
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow) / 255
        gamma_b = shadow
        image = cv2.addWeighted(image, alpha_b, image, 0, gamma_b)

    # Điều chỉnh độ tương phản
    if contrast != 0:
        f = 131 * (contrast + 127) / (127 * (131 - contrast))
        alpha_c = f
        gamma_c = 127 * (1 - f)
        image = cv2.addWeighted(image, alpha_c, image, 0, gamma_c)

    return image

def preprocess_image(image_path: str) -> str:
    # Đọc ảnh đầu vào
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Phát hiện cạnh để tìm thẻ (dùng Canny)
    edges = cv2.Canny(gray, 50, 150)
    
    # Tìm contour lớn nhất (giả định đây là thẻ)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        # Chọn contour lớn nhất
        largest_contour = max(contours, key=cv2.contourArea)
        rect = cv2.minAreaRect(largest_contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        
        # Xoay ảnh để thẻ nằm ngang
        angle = rect[-1]
        if angle < -45:
            angle += 90
        
        # Tính ma trận xoay và xoay ảnh
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h))
        
        # Cắt phần thẻ ra khỏi ảnh
        x, y, w, h = cv2.boundingRect(largest_contour)
        cropped_card = rotated[y:y+h, x:x+w]
        
        # Điều chỉnh độ sáng và bão hòa
        # Chuyển từ BGR sang HSV để điều chỉnh
        hsv = cv2.cvtColor(cropped_card, cv2.COLOR_BGR2HSV)
        
        # Điều chỉnh độ sáng và bão hòa
        hsv[..., 2] = cv2.add(hsv[..., 2], 50)  # Điều chỉnh độ sáng
        hsv[..., 1] = cv2.add(hsv[..., 1], 30)  # Điều chỉnh bão hòa
        
        adjusted_card = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
        # Lưu ảnh đã xử lý
        processed_image_path = os.path.join(PROCESSED_FOLDER, f"processed_{os.path.basename(image_path)}")
        if not os.path.exists(PROCESSED_FOLDER):
            os.makedirs(PROCESSED_FOLDER)
        cv2.imwrite(processed_image_path, adjusted_card)
        
        return processed_image_path

    return None

###### Cải tiến hàm preprocess_image
# def preprocess_image(image_path: str) -> str:
#     image = cv2.imread(image_path)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

#     processed_image_path = os.path.join(PROCESSED_FOLDER, f"processed_{os.path.basename(image_path)}")
#     cv2.imwrite(processed_image_path, thresh)
#     return processed_image_path