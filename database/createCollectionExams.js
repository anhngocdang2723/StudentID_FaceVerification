db.createCollection("Exams")
db.Exams.insertMany([
    {
        "exam_id": "INF30033",
        "exam_name": "An toàn thông tin",
        "exam_date": "2024-12-01",
        "rooms": [
            {
                "exam_room": "TTKT304",
                "invigilator_id": "GT101"
            },
            {
                "exam_room": "TTKT305",
                "invigilator_id": "GT103"
            },
            {
                "exam_room": "TTKT306",
                "invigilator_id": "GT105"
            }
        ]
    },
    {
        "exam_id": "INF20141",
        "exam_name": "Thị giác máy tính",
        "exam_date": "2024-12-03",
        "rooms": [
            {
                "exam_room": "TTKT404",
                "invigilator_id": "GT102"
            },
            {
                "exam_room": "TTKT405",
                "invigilator_id": "GT104"
            },
            {
                "exam_room": "TTKT406",
                "invigilator_id": "GT106"
            }
        ]
    },
    {
        "exam_id": "INF20007",
        "exam_name": "Trí tuệ nhân tạo",
        "exam_date": "2024-12-05",
        "rooms": [
            {
                "exam_room": "TTKT504",
                "invigilator_id": "GT107"
            },
            {
                "exam_room": "TTKT505",
                "invigilator_id": "GT108"
            },
            {
                "exam_room": "TTKT506",
                "invigilator_id": "GT109"
            }
        ]
    }
])
