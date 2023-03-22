進入到互動文件檢視：
http://127.0.0.1:8000/supps/
http://127.0.0.1:8000/docs->POST Request body
# 請求 Postman->POST body raw JSON->SEND
{
    "taxid": "22099131",
    "name": "台灣積體電路製造股份有限公司"
}
# 響應
{
    "taxid": 22099131,
    "name": "台灣積體電路製造股份有限公司",
    "products": []
}

http://127.0.0.1:8000/supp/22099131
# 響應 Postman->GET
{
    "taxid": 22099131,
    "name": "台灣積體電路製造股份有限公司",
    "products": []
}
# 請求 Postman->PATCH = 請求
{
    "taxid": "22099131",
    "name": "台灣積體電路製造股份有限公司II"
}
# 響應 Postman->DELETE
true

http://127.0.0.1:8000/supp/22099131/prod
# 請求 POST
{
  "port_number": "1001001",
  "name": "Wifi IC"
}
# 響應
{
    "id": 1,
    "supplier_taxid": 22099131,
    "port_number": 1001001,
    "name": "Wifi IC"
}

http://127.0.0.1:8000/supp/22099131/prod/1001001
# 響應 GET
{
    "id": 1,
    "supplier_taxid": 22099131,
    "port_number": 1001001,
    "name": "Wifi IC"
}

http://127.0.0.1:8000/pos
# 請求 POST
{
    "product_pn": 1001001,
    "cost_price": 200,
    "amount": 33
}
# 響應
{
    "cost_price": 200,
    "amount": 33,
    "id": 3,
    "time": "2023-03-20T11:22:29",
    "order_id": 20230311.2229,
    "supplier_taxid": 22099131,
    "supplier_name": "台灣積體電路製造股份有限公司",
    "product_pn": 1001001,
    "product_id": 3,
    "product_name": "Wifi IC",
    "total_price": 6600
}
# 請求 Postman->PATCH = 請求
{
    "product_pn": 1001001,
    "cost_price": 300,
    "amount": 44
}

http://127.0.0.1:8000/custs/
# 請求 POST = 響應
{
    "taxid": "00000022",
    "name": "泰煜建材股份有限公司"
}

# 請求 POST body raw "Text"->SEND
{
    "taxid": "00000022",
    "name": "泰煜建材股份有限公司"
}
# 響應 body格式錯誤
{
    "detail": [
        {
            "loc": [
                "body"
            ],
            "msg": "value is not a valid dict",
            "type": "type_error.dict"
        }
    ]
}
