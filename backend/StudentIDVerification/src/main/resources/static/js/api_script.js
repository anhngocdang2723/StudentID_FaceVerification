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
                    console.error("Phản hồi không ok:", response);
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
    
// Gửi yêu cầu đến FastAPI và hiển thị thông tin sinh viên
    const uploadExcelForm = document.getElementById('uploadExcelForm');
    if (uploadExcelForm) {
        uploadExcelForm.onsubmit = async function(event) {
            event.preventDefault();
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

                        row.innerHTML = `
                        <td>${name}</td>
                        <td>${msv}</td>
                        <td>Chưa có</td> <!-- Hiển thị "Chưa có" nếu không có đường dẫn phiếu thi -->
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

// Lấy danh sách sinh viên từ FastAPI
    async function fetchStudentList() {
        try {
            const response = await fetch("http://127.0.0.1:8000/api/students");
            if (!response.ok) {
                throw new Error('Không thể tải danh sách sinh viên.');
            }

            const data = await response.json();
            console.log('Danh sách sinh viên:', data);

            // Thêm sinh viên vào bảng
            const studentList = document.getElementById('studentList');
            studentList.innerHTML = ''; // Xóa nội dung cũ

            if (data && data.students && data.students.length > 0) {
                data.students.forEach(student => {
                    const row = document.createElement('tr');

                    // Tách tên và mã sinh viên từ chuỗi
                    const studentInfo = student.split(" - "); // Chia chuỗi tại dấu " - "
                    const name = studentInfo[0] || "Chưa có tên"; // Phần trước dấu " - "
                    const msv = studentInfo[1] || "Chưa có mã sinh viên"; // Phần sau dấu " - "

                    row.innerHTML = `
                    <td>${name}</td>
                    <td>${msv}</td>
                    <td>Chưa có</td> <!-- Hiển thị "Chưa có" thay vì đường dẫn phiếu thi -->
                `;
                    studentList.appendChild(row);
                });
            } else {
                alert('Không có sinh viên để hiển thị.');
            }

        } catch (error) {
            console.error("Lỗi khi tải danh sách sinh viên:", error);
        }
    }

// Gọi hàm khi trang tải
    document.addEventListener('DOMContentLoaded', function() {
        fetchStudentList(); // Gọi hàm để tải danh sách sinh viên từ FastAPI
    });



    // // Gửi file Excel và hiển thị kết quả
    // const uploadExcelForm = document.getElementById('uploadExcelForm');
    // if (uploadExcelForm) {
    //     uploadExcelForm.onsubmit = async function(event) {
    //         event.preventDefault();
    //         const fileExcelInput = document.getElementById('fileExcel');
    //         const file = fileExcelInput.files[0];
    //
    //         if (!file) {
    //             alert("Vui lòng chọn file Excel trước khi tải lên.");
    //             return;
    //         }
    //
    //         const formData = new FormData();
    //         formData.append("file", file); // Đảm bảo tên trường trùng với tên trong backend
    //
    //         try {
    //             console.log("Bắt đầu tải lên file Excel");
    //             const response = await fetch("http://127.0.0.1:8000/api/read-excel", {
    //                 method: "POST",
    //                 body: formData
    //             });
    //
    //
    //             if (!response.ok) {
    //                 console.error("Phản hồi không ok:", response);
    //                 throw new Error('Có lỗi xảy ra khi tải lên file Excel: ' + response.statusText);
    //             }
    //
    //             const result = await response.json();
    //             console.log("Kết quả nhận được:", result);
    //             const studentList = document.getElementById('studentList');
    //             studentList.innerHTML = ""; // Xóa nội dung cũ
    //
    //             if (result.students && result.students.length > 0) {
    //                 result.students.forEach(student => {
    //                     const row = document.createElement('tr');
    //                     row.innerHTML = `
    //                     <td>${student.name}</td>
    //                     <td>${student.msv}</td>
    //                     <td><a href="${student.examLink || '#'}" target="_blank">Xem phiếu thi</a></td>
    //                 `;
    //                     studentList.appendChild(row);
    //                 });
    //             } else {
    //                 alert("Không có thông tin sinh viên trong file Excel.");
    //             }
    //         } catch (error) {
    //             alert("Lỗi: " + error.message);
    //         }
    //     };
    // }
});
