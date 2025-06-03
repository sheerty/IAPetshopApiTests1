INVENTORY_SCHEMA = {"type": "object",
                    "properties": {
                        "approved": {
                            "type": "integer",
                            "description": "Количество одобренных заказов",
                            "minimum": 0
                        },
                        "delivered": {
                            "type": "integer",
                            "description": "Количество доставленных заказов",
                            "minimum": 0
                        }
                    },
                    "required": ["approved", "delivered"],
                    "additionalProperties": False
                    }
