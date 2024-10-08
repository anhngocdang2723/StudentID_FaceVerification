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
    let response = await fetch('api/upload-image', {
        method: 'POST',
        body: formData
    });

    let result = await response.json();
    document.getElementById('result').textContent = JSON.stringify(result, null, 4);

    // Liên kết tải file //Bỏ qua
     //document.getElementById('download-txt').href = result.txt_link;
    // document.getElementById('download-csv').href = result.csv_link;
};