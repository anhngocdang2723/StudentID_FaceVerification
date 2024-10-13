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

### Bổ sung: các model ở folder models nếu pull về chưa có thì lấy tại
1. https://github.com/GuoQuanhao/68_points/blob/master/shape_predictor_68_face_landmarks.dat
2. https://github.com/ageitgey/face_recognition_models/blob/master/face_recognition_models/models/dlib_face_recognition_resnet_model_v1.dat
Tải 2 file *.dat về và thêm vào folder models

### cài đặt thêm Git LFS để có thể tải lên file vượt quá 50mb:
    git lfs install
    git lfs track "*.dat" 
    git add .gitattributes
    git add api/models/shape_predictor_68_face_landmarks.dat
    git add api/models/dlib_face_recognition_resnet_model_v1.dat
    git commit -m "Add models using Git LFS"
    git push origin main
