document.addEventListener("DOMContentLoaded", function() {
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
            // Xóa nội dung của phần tử result để ẩn thông báo "Đang xử lý..."
            document.getElementById('result').textContent = ""; // Ẩn thông báo sau khi nhận được kết quả

            // Cập nhật bảng OCR
            const ocrTable = document.getElementById("ocr-table");
            const tableBody = ocrTable.querySelector("tbody");
            tableBody.innerHTML = ""; // Xóa dữ liệu cũ trong bảng
            ocrTable.style.display = "table"; // Hiển thị bảng

            if (result["Thông tin trích xuất được"]) {
                for (const [key, value] of Object.entries(result["Thông tin trích xuất được"])) {
                    const row = document.createElement("tr");
                    const cellKey = document.createElement("td");
                    cellKey.textContent = key;
                    const cellValue = document.createElement("td");
                    cellValue.textContent = value;
                    row.appendChild(cellKey);
                    row.appendChild(cellValue);
                    tableBody.appendChild(row);
                }
            } else {
                document.getElementById('result').textContent = "Không có dữ liệu OCR.";
                ocrTable.style.display = "none"; // Ẩn bảng nếu không có dữ liệu
            }

            // Hiển thị ảnh khuôn mặt nếu có
            const faceImage = document.getElementById('face-image');
            if (result.face_image) {
                faceImage.src = 'data:image/jpeg;base64,' + result.face_image;
                faceImage.style.display = 'block';
            } else {
                faceImage.style.display = 'none';
            }
        } catch (error) {
            document.getElementById('result').textContent = 'Lỗi: ' + error.message;
        }
    };
});
