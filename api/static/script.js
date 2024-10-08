// Hiển thị ảnh xem trước khi người dùng chọn ảnh
document.getElementById('file').addEventListener('change', function() {
    const file = this.files[0];
    const preview = document.getElementById('imagePreview');

    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.innerHTML = '<img src="' + e.target.result + '" alt="Image Preview">';
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

    try {
        let response = await fetch('api/upload-image', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            let result = await response.json();
            document.getElementById('result').textContent = JSON.stringify(result, null, 4);

            // Hiển thị thông tin sinh viên sau khi nhận diện
            document.getElementById('result-name').textContent = result.name || 'Không có thông tin';
            document.getElementById('result-msv').textContent = result.msv || 'Không có thông tin';
            document.getElementById('result-major').textContent = result.major || 'Không có thông tin';
            document.getElementById('result-faculty').textContent = result.faculty || 'Không có thông tin';
            document.getElementById('result-course').textContent = result.course || 'Không có thông tin';
            document.getElementById('result-compare').textContent = result.compare_status || 'Không có kết quả đối chiếu';
        } else {
            document.getElementById('result').textContent = "Có lỗi xảy ra. Vui lòng thử lại.";
        }
    } catch (error) {
        document.getElementById('result').textContent = "Lỗi kết nối hoặc xử lý. Vui lòng thử lại.";
    }
};
