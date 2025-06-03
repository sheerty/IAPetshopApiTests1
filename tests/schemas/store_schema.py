STORE_SCHEMA = {"type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "description": "Уникальный идентификатор заказа",
                        "minimum": 1
                    },
                    "petId": {
                        "type": "integer",
                        "description": "Идентификатор питомца",
                        "minimum": 1
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "Количество единиц",
                        "minimum": 0
                    },
                    "status": {
                        "type": "string",
                        "description": "Статус заказа",
                        "enum": ["placed", "approved", "delivered", "canceled"]
                    },
                    "complete": {
                        "type": "boolean",
                        "description": "Флаг завершенности заказа"
                    }
                },
                "required": ["id", "petId", "quantity", "status", "complete"],
                "additionalProperties": False
                }
