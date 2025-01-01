document.addEventListener("DOMContentLoaded", function() {
    // Các yếu tố DOM
    const fileImage = document.getElementById('fileImage');
    const uploadImageForm = document.getElementById('uploadImageForm');
    const ocrResult = document.getElementById('ocrResult');
    const studentListTable = document.getElementById('studentList');
    const continueButton = document.getElementById('continueButton');
    const fileExcelInput = document.getElementById('fileExcel');
    const filePersonalImage = document.getElementById('filePersonalImage');
    const downloadExcelButton = document.getElementById('downloadExcelButton'); // Nút tải xuống Excel

    let studentList = [];
    let ticketInfo = null; // Biến lưu thông tin phiếu thi

    // Xem trước ảnh cá nhân
    if (filePersonalImage) {
        filePersonalImage.addEventListener('change', function(event) {
            const file = event.target.files[0];
            const reader = new FileReader();
            reader.onload = function(e) {
                const personalImagePreview = document.getElementById('personalImagePreview');
                if (personalImagePreview) {
                    personalImagePreview.style.backgroundImage = `url(${e.target.result})`;
                    personalImagePreview.textContent = ''; // Xóa text nếu có
                }
            };
            if (file) {
                reader.readAsDataURL(file);
            }
        });
    }

    // Xem trước ảnh thẻ sinh viên
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

    // Gửi ảnh và hiển thị kết quả OCR và phiếu thi
    if (uploadImageForm) {
        uploadImageForm.onsubmit = async function(event) {
            event.preventDefault();
            if (ocrResult) ocrResult.textContent = "Đang xử lý...";

            const formData = new FormData();
            formData.append('file', fileImage.files[0]);

            try {
                let response = await fetch('http://127.0.0.1:8000/api/upload-image', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    console.error("Phản hồi không ok:", response);
                    throw new Error('Có lỗi xảy ra: ' + response.statusText);
                }

                let result = await response.json();
                displayOCRResult(result);
                displayFaceImage(result);
                displayTicket(result);

                // Lưu thông tin phiếu thi
                if (result["Phiếu thi"] && result["Phiếu thi"]["ticket_info"]) {
                    ticketInfo = result["Phiếu thi"]["ticket_info"]; // Lưu lại thông tin phiếu thi
                }

                // Giả sử bạn nhận được MSV từ kết quả và cập nhật trạng thái của sinh viên
                const msvFromResult = result["Thông tin trích xuất được"]["Mã sinh viên"];
                if (msvFromResult) {
                    updateStudentStatus(msvFromResult); // Cập nhật trạng thái khi có MSV
                }
            } catch (error) {
                if (ocrResult) ocrResult.textContent = 'Lỗi: ' + error.message;
            }
        };
    }

    // Cập nhật bảng sinh viên khi tải lên file Excel
    if (fileExcelInput) {
        fileExcelInput.addEventListener('change', async function(event) {
            const file = fileExcelInput.files[0];
            if (!file) return alert("Vui lòng chọn file Excel trước khi tải lên.");

            const formData = new FormData();
            formData.append("file", file);

            try {
                let response = await fetch("http://127.0.0.1:8000/api/read-excel", {
                    method: "POST",
                    body: formData
                });

                if (!response.ok) {
                    console.error("Phản hồi không ok:", response);
                    throw new Error('Có lỗi xảy ra khi tải lên file Excel: ' + response.statusText);
                }

                const result = await response.json();
                if (result.students && result.students.length > 0) {
                    studentList = result.students.map(student => ({
                        name: student.split(" - ")[0] || "Chưa có tên",
                        msv: student.split(" - ")[1] || "Chưa có mã sinh viên",
                        status: "Chưa có mặt",
                        isAuthenticated: false // Thêm thuộc tính xác thực
                    }));
                    updateStudentTable();
                } else {
                    alert("Không có thông tin sinh viên trong file Excel.");
                }
            } catch (error) {
                alert("Lỗi: " + error.message);
            }
        });
    }

    // Cập nhật bảng sinh viên
    function updateStudentTable() {
        studentListTable.innerHTML = '';
        studentList.forEach(student => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${student.name}</td>
                <td>${student.msv}</td>
                <td>${student.status}</td>
            `;
            studentListTable.appendChild(row);
        });
    }

    // Hiển thị kết quả OCR và cập nhật trạng thái
    function displayOCRResult(result) {
        const ocrTable = document.getElementById("ocr-table");
        const tableBody = ocrTable.querySelector("tbody");
        if (ocrTable) {
            tableBody.innerHTML = "";
            ocrTable.style.display = "table";

            if (result["Thông tin trích xuất được"]) {
                for (const [key, value] of Object.entries(result["Thông tin trích xuất được"])) {
                    const row = document.createElement("tr");
                    row.innerHTML = `<td>${key}</td><td>${value}</td>`;
                    tableBody.appendChild(row);
                }
            } else {
                ocrResult.textContent = "Không có dữ liệu OCR.";
                ocrTable.style.display = "none";
            }
        }
    }

    // Hiển thị ảnh khuôn mặt đã cắt
    function displayFaceImage(result) {
        const faceImage = document.getElementById('face-image');
        if (faceImage) {
            if (result["Hình ảnh khuôn mặt (base64)"]) {
                faceImage.src = 'data:image/jpeg;base64,' + result["Hình ảnh khuôn mặt (base64)"];
                faceImage.style.display = 'block';
            } else {
                faceImage.style.display = 'none';
            }
        }
    }

    // Hiển thị phiếu thi
    function displayTicket(result) {
        const ticketContainer = document.getElementById("ticket-container");
        const ticketContent = document.getElementById("ticket-content");

        if (ticketContent) {
            if (result["Phiếu thi"] && result["Phiếu thi"]["ticket_info"]) {
                const ticketInfo = result["Phiếu thi"]["ticket_info"];
                ticketContainer.style.display = "block";
                ticketContent.innerHTML = `
                    <h3>Phiếu Dự Thi</h3>
                    <div><strong>Tên sinh viên:</strong> ${ticketInfo["Tên sinh viên"]}</div>
                    <div><strong>Mã sinh viên:</strong> ${ticketInfo["Mã sinh viên"]}</div>
                    <div><strong>Tên môn thi:</strong> ${ticketInfo["Tên môn thi"]}</div>
                    <div><strong>Mã khóa:</strong> ${ticketInfo["Mã khóa"]}</div>
                    <div><strong>Vị trí ngồi:</strong> ${ticketInfo["Vị trí ngồi"]}</div>
                    <div><strong>Đường dẫn phiếu thi:</strong>
                        <a href="${result["Phiếu thi"]["file_path"]}" target="_blank">Tải về tại đây</a>
                    </div>
                `;
            } else {
                ticketContainer.style.display = "none";
            }
        }
    }

    // Cập nhật trạng thái của sinh viên khi có MSV đã xác thực
    function updateStudentStatus(msvFromResult) {
        studentList.forEach(student => {
            if (student.msv === msvFromResult) {
                student.status = 'Có mặt'; // Cập nhật trạng thái khi MSV trùng khớp
                student.isAuthenticated = true; // Đánh dấu đã xác thực
            }
        });
        updateStudentTable();
    }

    // Cập nhật trạng thái của sinh viên khi nhấn nút "Tiếp tục"
    if (continueButton) {
        continueButton.addEventListener('click', function() {
            // Lấy MSV từ phiếu thi
            if (ticketInfo && ticketInfo["Mã sinh viên"]) {
                const msvFromTicket = ticketInfo["Mã sinh viên"];

                studentList.forEach(student => {
                    if (student.msv === msvFromTicket) {
                        student.status = 'Có mặt'; // Cập nhật trạng thái thành 'Có mặt'
                        student.isAuthenticated = true; // Đánh dấu đã xác thực
                    }
                });
                updateStudentTable();
                alert('Trạng thái đã được cập nhật!');
            } else {
                alert('Không thể xác định MSV từ phiếu thi.');
            }

            // Làm mới ảnh sau khi xác thực
            resetRightPanel();
            resetImage();
        });

    }

    // Reset lại phần bên phải (Ảnh khuôn mặt, Kết quả OCR, Kết quả so sánh khuôn mặt, Phiếu Dự Thi)
    function resetRightPanel() {
        // Reset ảnh khuôn mặt
        const faceImage = document.getElementById('face-image');
        if (faceImage) faceImage.style.display = 'none';

        // Reset kết quả OCR
        const ocrTable = document.getElementById("ocr-table");
        const tableBody = ocrTable.querySelector("tbody");
        if (ocrTable) {
            tableBody.innerHTML = "";
            ocrResult.textContent = "Kết quả OCR:";
            ocrTable.style.display = "none";
        }

        // Reset kết quả so sánh khuôn mặt
        const comparisonResult = document.getElementById("comparison-result");
        if (comparisonResult) comparisonResult.style.display = "none";
        const comparisonText = document.getElementById("comparison-text");
        if (comparisonText) comparisonText.textContent = "";

        // Reset phiếu dự thi
        const ticketContainer = document.getElementById("ticket-container");
        if (ticketContainer) ticketContainer.style.display = "none";
    }

    // Reset lại ảnh tải lên
    function resetImage() {
        // Làm mới ảnh tải lên
        const imagePreview = document.getElementById('imagePreview');
        const personalImagePreview = document.getElementById('personalImagePreview');
        if (imagePreview) {
            imagePreview.style.backgroundImage = ''; // Xóa ảnh trước
            imagePreview.textContent = 'Chọn ảnh thẻ sinh viên';
        }
        if (personalImagePreview) {
            personalImagePreview.style.backgroundImage = ''; // Xóa ảnh trước
            personalImagePreview.textContent = 'Chọn ảnh cá nhân';
        }
        // Xóa file đã tải lên
        fileImage.value = '';
        filePersonalImage.value = '';
    }

    // Xử lý tải xuống danh sách sinh viên dưới dạng file Excel
    if (downloadExcelButton) {
        downloadExcelButton.addEventListener('click', function() {
            if (studentList.length === 0) {
                alert("Danh sách sinh viên rỗng.");
                return;
            }

            const wb = XLSX.utils.book_new();
            const wsData = studentList.map(student => [
                student.name,
                student.msv,
                student.status
            ]);

            const ws = XLSX.utils.aoa_to_sheet([["Tên sinh viên", "Mã sinh viên", "Trạng thái"], ...wsData]);
            XLSX.utils.book_append_sheet(wb, ws, "Danh sách sinh viên");

            // Tải file Excel về
            XLSX.writeFile(wb, "Danh_sach_sinh_vien.xlsx");
        });
    }

});
