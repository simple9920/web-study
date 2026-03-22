# Item Management API

## 概要
FastAPIを使用したシンプルな商品管理APIです。
CRUD(作成・取得・更新・削除)機能を実装しています。

## 機能一覧
- Create Item (POST /items/)
- Get Items (GET /items/)
- Get Item by ID (GET /items/{item_id})
- Update Item (PUT /items/{item_id})
- Delete Item (DELETE /items/{item_id})

## 技術スタック
- Python
- FastAPI

## 使い方
1. サーバー起動
```bash
uvicorn main:app --reload
```
2. Swaggerで確認
```text
http://127.0.0.1:8000/docs
```
