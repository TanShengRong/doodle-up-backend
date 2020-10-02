# This file is for testing purposes, before we instantiate Firebase
stories = [
    {
        "id": 1,
        "story_title": "Story 1",
        "cover_image": "--imgblob--",
        "stages": [
            {
                "type": 'guessing',
                "image": "--imageblob--",
                "description": "Once upon a time, there was a ___.",
                "options": {
                    "dog": "--audiourl--",
                    "cat": "--audiourl--",
                    "mouse": "--audiourl--",
                    "bird": "--audiourl--",
                },
                "answer": "dog"
            },
            {
                "type": "drawing",
                "image": '--imageblob--',
                "description": 'Draw a bone',
            }
        ]
    }
]

# {
#     "username": "popo",
#     "new_image": file,
#     "content": {
#         "image_url": "www.google.com",
#         "stage_id": 1.1,
#         "status": "completed"
#     }
# }
