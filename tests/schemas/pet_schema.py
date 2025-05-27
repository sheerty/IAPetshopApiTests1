PET_SCHEMA = {
    "type" : "object",
    "properties" : {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "category": {"type": "object",
        "properties" : {
        "id": {"type": "integer"},
        "name": {"type": "string"},},
        "required": ["id", "name"],
        "additionalProperties": False,
        },
        "photoUrls": {"type": "array",
        "items": {"type": "string"}},
        "tags": {"type": "array","items":
            {"type": "object"},
                 "properties": {
                     "tag": {"type": "string"},
                     "id": {"type": "integer"},
                     "name": {"type": "string"}},
                     "required": ["id", "name"],
                     "additionalProperties": False,
                 }
        ,
        "status": {"type": "string", "enum": ["available", 'pending', 'solved']},
    },
    "required": ["id", "name", "photoUrls", "tags"],
    "additionalProperties": False,
    }