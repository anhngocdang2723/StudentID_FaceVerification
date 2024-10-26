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
    
    // Sử dụng URL FastAPI đang chạy ở http://127.0.0.1:8000
    let response = await fetch('http://127.0.0.1:8000/api/upload-image', {  // Cập nhật URL API FastAPI
        method: 'POST',
        body: formData
    });

    let result = await response.json();
    document.getElementById('result').textContent = JSON.stringify(result, null, 4);
};
