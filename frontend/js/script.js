// Sự kiện khi thay đổi file để xem trước ảnh
document.getElementById('file').addEventListener('change', function() {
    const file = this.files[0];
    const preview = document.getElementById('imagePreview');

    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.innerHTML = '<img src="' + e.target.result + '" alt="Image Preview" style="max-width: 100%; height: auto;">';
        }
        reader.readAsDataURL(file);
    } else {
        preview.innerHTML = '';
    }
});

// Gửi ảnh và hiển thị kết quả sau khi xử lý
document.getElementById('uploadForm').onsubmit = async function(event) {
    event.preventDefault();
    document.getElementById('result').textContent = "Đang xử lý...";

    let formData = new FormData(this);

    // Gửi yêu cầu đến API
    try {
        let response = await fetch('http://127.0.0.1:8000/api/upload-image', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Có lỗi xảy ra: ' + response.statusText);
        }

        let result = await response.json();
        document.getElementById('result').textContent = JSON.stringify(result, null, 4);

        // Hiển thị ảnh khuôn mặt nếu có
        const faceImage = document.getElementById('face-image');
        if (result.face_image) { // Sử dụng face_image
            faceImage.src = 'data:image/jpeg;base64,' + result.face_image; // Cập nhật src với chuỗi base64
            faceImage.style.display = 'block'; // Hiện ảnh
        } else {
            // Nếu không có ảnh khuôn mặt, ẩn thẻ img
            faceImage.style.display = 'none';
        }
    } catch (error) {
        document.getElementById('result').textContent = 'Lỗi: ' + error.message;
    }
};
