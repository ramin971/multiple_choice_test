from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, OpenApiResponse, OpenApiExample


question_parameters=[
            OpenApiParameter(
                name='tag',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='list of questions by tag_name',
                required=True
            )
        ]


submit_exam_response = OpenApiResponse(
    response=OpenApiTypes.OBJECT,
    description="Score by correct answer",
    examples=[
        OpenApiExample(
            'Response Example',
            value={
                "tag": "test1",
                "total_questions": 10,
                "correct_answers": 8,
                "score_percent": 80.0
            },
            response_only=True
        )
    ]
)

