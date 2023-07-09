functions = [
    {
        "name": "accountant_batch",
        "description": "记录收入与支出信息，收入与支出可以有多条。",
        "parameters": {
            "type": "object",
            "properties": {
                "list": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "userid": {
                                "type": "string"
                            },
                            "transaction_date": {
                                "type": "string",
                                "description": "transaction date 交易日期 default:today",
                            },
                            # "price": {
                            #     "type": "number",
                            #     "description": "单价 默认值为1",
                            # },
                            # "数量": {
                            #     "type": "number",
                            #     "default": 1,
                            #     "description": "数量 默认值为个",
                            # },
                            "total_amount": {
                                "type": "number",
                                "description": " total amount , total amount = price * quantity 总金额",
                            },
                            "item": {
                                "type": "string",
                                "description": "item or merchandise",
                            },
                            "ttype": {
                                "type": "string",
                                "enum": ["income", "spending"],
                                "description": "income or spending 收入或支出",
                            },
                            "payment": {
                                "type": "string",
                                # "enum": ["cash", "credit"],
                                "description": "payment method, 交易方式",
                            },
                            "remark": {
                                "type": "string"
                            },
                        },
                    },
                },
            },
            "required": ["list"],
        },
    },
    {
        "name": "todolist",
        "description": "记录待办事项",
        "parameters": {
            "type": "object",
            "properties": {
                "userid": {
                    "type": "string"
                },
                "transaction_date": {
                    "type": "string",
                    "description": "办事的日期",
                },
                "item": {
                    "type": "string",
                    "description": "需要办理的事宜 todo",
                }
            },
            "required": ["userid", "transaction_date", "item"]
        },
    },
]
