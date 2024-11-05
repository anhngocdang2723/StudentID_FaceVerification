document.addEventListener("DOMContentLoaded", function() {
    // Sự kiện khi thay đổi file để xem trước ảnh thẻ sinh viên
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

    // Sự kiện khi thay đổi file để xem trước ảnh người dùng
    document.getElementById('userFile').addEventListener('change', function() {
        const file = this.files[0];
        const preview = document.getElementById('userImagePreview');

        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                preview.innerHTML = '<img src="' + e.target.result + '" alt="User Image Preview" style="max-width: 100%; height: auto;">';
            }
            reader.readAsDataURL(file);
        } else {
            preview.innerHTML = '';
        }
    });

    // Ẩn vùng kết quả so sánh khuôn mặt ban đầu
    const comparisonResult = document.getElementById("comparison-result");
    comparisonResult.style.display = "none";

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
            document.getElementById('result').textContent = ""; // Xóa thông báo đang xử lý

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
                ocrTable.style.display = "none";
            }

            // Hiển thị ảnh khuôn mặt đã cắt
            const faceImage = document.getElementById('face-image');
            if (result.face_image) {
                faceImage.src = 'data:image/jpeg;base64,' + result.face_image;
                faceImage.style.display = 'block'; // Hiển thị ảnh
            } else {
                faceImage.style.display = 'none'; // Ẩn ảnh nếu không có
            }

            // Hiển thị kết quả so sánh khuôn mặt
            const comparisonText = document.getElementById("comparison-text");
            if (result.comparison) {
                comparisonText.textContent = result.comparison; // Cập nhật nội dung so sánh
                comparisonResult.style.display = "block"; // Hiển thị vùng kết quả so sánh
            } else {
                comparisonText.textContent = "Không có kết quả so sánh."; // Thêm thông báo nếu không có kết quả
                comparisonResult.style.display = "none"; // Ẩn nếu không có kết quả
            }
            console.log('Phản hồi từ API:', result);
            
        } catch (error) {
            document.getElementById('result').textContent = 'Lỗi: ' + error.message;
        }
    };    
});
