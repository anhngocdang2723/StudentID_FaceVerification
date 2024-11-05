document.addEventListener("DOMContentLoaded", function() {
    // Sự kiện khi thay đổi file để xem trước ảnh thẻ sinh viên
    const fileImage = document.getElementById('fileImage');
    if (fileImage) {
        fileImage.addEventListener('change', function(event) {
            const file = event.target.files[0];
            const reader = new FileReader();
            reader.onload = function(e) {
                const imagePreview = document.getElementById('imagePreview');
                if (imagePreview) {
                    imagePreview.style.backgroundImage = `url(${e.target.result})`;
                    imagePreview.textContent = ''; // Xóa text nếu có
                }
            };
            if (file) {
                reader.readAsDataURL(file);
            }
        });
    }

    // Gửi ảnh và hiển thị kết quả sau khi xử lý
    const uploadImageForm = document.getElementById('uploadImageForm');
    if (uploadImageForm) {
        uploadImageForm.onsubmit = async function(event) {
            event.preventDefault();
            const ocrResult = document.getElementById('ocrResult');
            if (ocrResult) ocrResult.textContent = "Đang xử lý...";

            const formData = new FormData();
            formData.append('file', fileImage.files[0]);

            try {
                let response = await fetch('http://127.0.0.1:8000/api/upload-image', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    throw new Error('Có lỗi xảy ra: ' + response.statusText);
                }

                let result = await response.json();
                if (ocrResult) ocrResult.textContent = "Kết quả OCR:";

                // Cập nhật bảng OCR
                const ocrTable = document.getElementById("ocr-table");
                if (ocrTable) {
                    const tableBody = ocrTable.querySelector("tbody");
                    tableBody.innerHTML = "";
                    ocrTable.style.display = "table";

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
                        ocrResult.textContent = "Không có dữ liệu OCR.";
                        ocrTable.style.display = "none";
                    }
                }

                // Hiển thị ảnh khuôn mặt nếu có
                const faceImage = document.getElementById('face-image');
                if (faceImage) {
                    if (result.face_image) {
                        faceImage.src = 'data:image/jpeg;base64,' + result.face_image;
                        faceImage.style.display = 'block';
                    } else {
                        faceImage.style.display = 'none';
                    }
                }

                // Hiển thị kết quả so sánh khuôn mặt
                const comparisonResult = document.getElementById("comparison-result");
                const comparisonText = document.getElementById("comparison-text");
                if (result.comparison) {
                    comparisonText.textContent = result.comparison;
                    comparisonResult.style.display = "block";
                } else {
                    comparisonText.textContent = "Không có kết quả so sánh.";
                    comparisonResult.style.display = "none";
                }

            } catch (error) {
                if (ocrResult) ocrResult.textContent = 'Lỗi: ' + error.message;
            }
        };
    }

    // Sự kiện xem trước ảnh cá nhân (nếu cần)
    const filePersonalImage = document.getElementById('filePersonalImage');
    if (filePersonalImage) {
        filePersonalImage.addEventListener('change', function(event) {
            const file = event.target.files[0];
            const reader = new FileReader();
            reader.onload = function(e) {
                const personalImagePreview = document.getElementById('personalImagePreview');
                if (personalImagePreview) {
                    personalImagePreview.style.backgroundImage = `url(${e.target.result})`;
                    personalImagePreview.textContent = '';
                }
            };
            if (file) {
                reader.readAsDataURL(file);
            }
        });
    }
});
