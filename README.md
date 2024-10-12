```md
# StudentID_FaceVerification

### Mô tả
Đây là một dự án cá nhân sử dụng kỹ thuật nhận dạng và xử lý ảnh (Computer Vision) để trích xuất và xác thực thông tin sinh viên từ thẻ sinh viên, cũng như có thể mở rộng thêm khả năng nhận dạng khuôn mặt.

Dự án này bao gồm việc:
- Xử lý ảnh thẻ sinh viên để trích xuất thông tin như: Tên, MSV (Mã số sinh viên), Ngành học, Khoa/Viện, và Khóa học.
- Hiển thị ảnh đã tải lên và hiển thị kết quả nhận diện.
- Xuất kết quả thành file TXT hoặc CSV để lưu trữ và xử lý thêm.

### Các chức năng chính
1. **Tiền xử lý ảnh**: Ảnh thẻ sinh viên sẽ được xử lý (chuyển sang ảnh xám, áp dụng threshold để loại bỏ nhiễu).
2. **OCR (Optical Character Recognition)**: Nhận dạng văn bản từ ảnh đã tiền xử lý sử dụng PaddleOCR.
3. **Hiển thị ảnh và kết quả trên giao diện web**: Người dùng tải ảnh thẻ sinh viên lên, kết quả nhận diện sẽ được hiển thị trên trang web.
4. **Xuất kết quả dưới dạng file**: Kết quả OCR sẽ được xuất ra dưới dạng file `.txt` hoặc `.csv`.

### Yêu cầu hệ thống
Để chạy được chương trình này, bạn cần các thư viện Python sau:

- `fastapi`: Framework API backend.
- `uvicorn`: Dùng để chạy FastAPI.
- `paddleocr`: Thư viện OCR để trích xuất văn bản từ ảnh.
- `paddlepaddle`: Thư viện học sâu cho PaddleOCR.
- `opencv-python`: Thư viện xử lý ảnh.
- `aiofiles`: Hỗ trợ FastAPI trong việc xử lý file upload.
- `python-multipart`: Xử lý multipart form (upload file) trong FastAPI.

Bạn có thể cài đặt các thư viện này qua tệp `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Hướng dẫn cài đặt và chạy
1. **Clone dự án**:
    ```bash
    git clone https://github.com/your-username/StudentID_FaceVerification.git
    cd StudentID_FaceVerification
    ```

2. **Cài đặt các thư viện yêu cầu**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Chạy ứng dụng FastAPI**:
    ```bash
    uvicorn main:app --reload
    ```

4. **Truy cập ứng dụng**:
   Mở trình duyệt và truy cập `http://127.0.0.1:8000` để sử dụng ứng dụng web.

### Cấu trúc thư mục dự án
```bash
StudentID_FaceVerification/
│
├── main.py                # Code FastAPI chính để xử lý logic backend
├── requirements.txt       # Danh sách các thư viện cần thiết
├── static/                # Thư mục chứa CSS và JS cho frontend
│   ├── style.css
│   └── script.js
├── templates/             # Thư mục chứa HTML template cho frontend
│   └── index.html
├── uploads/               # Thư mục chứa ảnh tải lên
└── results/               # Thư mục chứa kết quả nhận diện được xuất ra file TXT/CSV
```

### Hướng dẫn sử dụng
1. Mở giao diện web qua địa chỉ `http://127.0.0.1:8000`.
2. Tải ảnh thẻ sinh viên lên (định dạng hỗ trợ: `.jpg`, `.png`).
3. Ứng dụng sẽ hiển thị thông tin được nhận diện từ thẻ sinh viên.
4. Nhấn vào liên kết để tải file TXT hoặc CSV chứa kết quả nhận diện.

### Ảnh demo
#![Demo Image](static/demo.png) #ảnh update sau

### Đóng góp
Nếu bạn muốn đóng góp vào dự án, hãy fork dự án và gửi pull request. Hoặc bạn có thể mở các issue để báo cáo lỗi hoặc yêu cầu tính năng mới.

---

### Liên hệ
Nếu có bất kỳ câu hỏi hoặc thắc mắc nào, bạn có thể liên hệ qua email: `anhngocdang27022003@gmail.com`.

---

**License**: MIT

---

Hy vọng dự án này giúp bạn hiểu thêm về cách ứng dụng computer vision trong thực tế.
