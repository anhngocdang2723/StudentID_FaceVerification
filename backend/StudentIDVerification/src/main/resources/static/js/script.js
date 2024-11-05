document.getElementById('file').addEventListener('change', function() {
    const file = this.files[0];
    const preview = document.getElementById('imagePreview');

    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.innerHTML = '<img src="' + e.target.result + '" alt="Image Preview" style="max-width: 300px; max-height: 300px;">';
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

    let formData = new FormData();
    const fileInput = document.getElementById('file');
    formData.append('file', fileInput.files[0]); // Đảm bảo tên field là 'file'

    // Gửi yêu cầu đến FastAPI
    let response = await fetch('http://127.0.0.1:8000/api/upload-image', {
        method: 'POST',
        body: formData
    });

    if (response.ok) {
        let result = await response.json();
        document.getElementById('result').textContent = JSON.stringify(result, null, 4);

        // Hiển thị kết quả so sánh khuôn mặt
        const comparisonText = document.getElementById("comparison-text");
        const comparisonResult = document.getElementById("comparison-result");

        if (result.comparison) {
            comparisonText.textContent = result.comparison; // Cập nhật nội dung so sánh
            comparisonResult.style.display = "block"; // Hiển thị vùng kết quả so sánh
        } else {
            comparisonText.textContent = "Không có kết quả so sánh."; // Thêm thông báo nếu không có kết quả
            comparisonResult.style.display = "none"; // Ẩn nếu không có kết quả
        }
    } else {
        document.getElementById('result').textContent = "Đã xảy ra lỗi: " + response.statusText;
    }
};
