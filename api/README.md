## API được viết bằng FastAPI sử dụng ngôn ngữ python

### Note:
- Code chính, vận hành được lưu trữ ở main.py 
- Các module lưu trữ các hàm xử lý các chức năng như đọc excel, cắt ảnh, đọc khuôn mặt được viết ở ngoài để tiện vận hành và bảo dưỡng

### Mô tả API //update sau


### Cách vận hành
1. Lấy ảnh sinh viên và thẻ sinh viên.
2. Hệ thống sẽ sử dụng mô-đun YOLO để phát hiện và cắt ảnh thẻ.
3. Module 'image_processing' và 'face_extraction' sẽ được dùng để tiền xử lý và nhận diện khuôn mặt.
4. FastAPI xử lý kết quả nhận diện, và gửi đến backend Spring Boot để lưu vào MongoDB.
5. Các thông tin về danh tính và bài thi được quản lý qua backend và lưu trữ an toàn.
