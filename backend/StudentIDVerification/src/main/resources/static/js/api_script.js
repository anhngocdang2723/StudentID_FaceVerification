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
            event.preventDefault(); // Ngừng reload trang khi submit
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
                    console.error("Phản hồi không ok:", response);
                    throw new Error('Có lỗi xảy ra: ' + response.statusText);
                }

                let result = await response.json();
                console.log(result);
                if (ocrResult) ocrResult.textContent = "Kết quả OCR:";

                // Cập nhật bảng OCR
                const ocrTable = document.getElementById("ocr-table");
                if (ocrTable) {
                    const tableBody = ocrTable.querySelector("tbody");
                    tableBody.innerHTML = ""; // Xóa nội dung cũ
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

                // Hiển thị phiếu thi nếu có
                const ticketContainer = document.getElementById("ticket-container");
                const ticketContent = document.getElementById("ticket-content");
                if (ticketContent) {
                    if (result["ticket_info"]) {
                        const ticketData = result["ticket_info"];

                        // In ra console để kiểm tra dữ liệu phiếu thi
                        console.log("Dữ liệu phiếu thi: ", ticketData);

                        // Kiểm tra xem dữ liệu phiếu thi có đầy đủ trường cần thiết không
                        if (ticketData &&
                            ticketData["Tên sinh viên"] &&
                            ticketData["Mã sinh viên"] &&
                            ticketData["Tên môn thi"] &&
                            ticketData["Mã khóa"] &&
                            ticketData["Vị trí ngồi"]) {

                            ticketContainer.style.display = "block";  // Hiển thị div phiếu thi
                            const ticketHtml = `
                                <strong>Phiếu Dự Thi</strong><br><br>
                                <strong>Tên sinh viên:</strong> ${ticketData["Tên sinh viên"]}<br>
                                <strong>Mã sinh viên:</strong> ${ticketData["Mã sinh viên"]}<br>
                                <strong>Tên môn thi:</strong> ${ticketData["Tên môn thi"]}<br>
                                <strong>Mã khóa:</strong> ${ticketData["Mã khóa"]}<br>
                                <strong>Vị trí ngồi:</strong> ${ticketData["Vị trí ngồi"]}<br>
                                <hr>
                            `;
                            ticketContent.innerHTML = ticketHtml;  // Sử dụng innerHTML để chèn HTML
                        } else {
                            console.error("Dữ liệu phiếu thi không đầy đủ.");
                            ticketContainer.style.display = "none"; // Ẩn phiếu thi nếu thiếu dữ liệu
                        }
                    } else {
                        console.log("Không có phiếu thi trong dữ liệu trả về.");
                        ticketContainer.style.display = "none"; // Ẩn phiếu thi nếu không có
                    }
                } else {
                    console.error("Không tìm thấy phần tử với ID 'ticket-content'.");
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

    // Gửi yêu cầu đến FastAPI và hiển thị thông tin sinh viên
    const uploadExcelForm = document.getElementById('uploadExcelForm');
    if (uploadExcelForm) {
        uploadExcelForm.onsubmit = async function(event) {
            event.preventDefault(); // Ngừng reload trang khi submit
            const fileExcelInput = document.getElementById('fileExcel');
            const file = fileExcelInput.files[0];

            if (!file) {
                alert("Vui lòng chọn file Excel trước khi tải lên.");
                return;
            }

            const formData = new FormData();
            formData.append("file", file); // Đảm bảo tên trường trùng với tên trong backend

            try {
                console.log("Bắt đầu tải lên file Excel");
                const response = await fetch("http://127.0.0.1:8000/api/read-excel", {
                    method: "POST",
                    body: formData
                });

                if (!response.ok) {
                    console.error("Phản hồi không ok:", response);
                    throw new Error('Có lỗi xảy ra khi tải lên file Excel: ' + response.statusText);
                }

                const result = await response.json();
                console.log("Kết quả nhận được:", result);

                const studentList = document.getElementById('studentList');
                studentList.innerHTML = ""; // Xóa nội dung cũ để cập nhật

                // Kiểm tra và hiển thị thông tin sinh viên
                if (result.students && result.students.length > 0) {
                    result.students.forEach(student => {
                        const row = document.createElement('tr');

                        // Tách tên và mã sinh viên
                        const studentInfo = student.split(" - "); // Chia chuỗi tại dấu " - "
                        const name = studentInfo[0] || "Chưa có tên"; // Phần trước dấu " - "
                        const msv = studentInfo[1] || "Chưa có mã sinh viên"; // Phần sau dấu " - "

                        // Lấy đường dẫn phiếu thi
                        const examSheetLink = student.exam_sheet_link || "Chưa có"; // Nếu không có đường dẫn thì hiển thị "Chưa có"

                        row.innerHTML = `
                        <td>${name}</td>
                        <td>${msv}</td>
                        <td>
                            <a href="${examSheetLink}" target="_blank">${examSheetLink === "Chưa có" ? "Chưa có" : "Xem phiếu thi"}</a>
                        </td> <!-- Hiển thị đường dẫn phiếu thi -->
                    `;
                        studentList.appendChild(row);
                    });
                } else {
                    alert("Không có thông tin sinh viên trong file Excel.");
                }
            } catch (error) {
                alert("Lỗi: " + error.message);
            }
        };
    }

    // function fetchExamTicket(studentMsv) {
    //     const previewElement = document.getElementById('exam-sheet-preview');
    //     previewElement.textContent = "Đang tải..."; // Hiển thị thông báo khi đang tải
    //
    //     fetch(`http://127.0.0.1:8000/api/serve-ticket/${studentMsv}`)
    //         .then(response => {
    //             if (!response.ok) {
    //                 throw new Error(`HTTP error! Status: ${response.status}`);
    //             }
    //             return response.json();
    //         })
    //         .then(data => {
    //             if (data.ticket_content) {
    //                 previewElement.textContent = data.ticket_content; // Hiển thị nội dung phiếu thi
    //             } else {
    //                 previewElement.textContent = "Không tìm thấy phiếu thi."; // Thông báo nếu không có dữ liệu
    //             }
    //         })
    //         .catch(error => {
    //             console.error('Lỗi:', error);
    //             previewElement.textContent = "Có lỗi xảy ra khi tải phiếu thi."; // Hiển thị lỗi
    //         });
    // }

    // Ví dụ sử dụng MSV để lấy phiếu thi
    // const studentMsv = "215748020110333";  // MSV của sinh viên
    // fetchExamTicket(studentMsv);
});
