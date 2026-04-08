# Item Management API

## 概要

FastAPIを使用した商品管理APIです。
ユーザー認証（JWT）と認可機能を実装し、
「ログインユーザーごとにデータを分離」しています。

---

## 機能一覧

### 🔹 認証（Authentication）

* ユーザー登録（POST /users/）
* ログイン（POST /login /JWTトークン発行）
* JWTトークンでログインユーザーを特定

---

### 🔹 認可（Authorization）

* ログインユーザーごとにデータを管理
* 自分のデータのみ取得可能
* 他人のデータは操作不可
* user_idを使い、自分のデータのみ操作可能に制御

---

### 🔹 CRUD機能

* Create Item (POST /items/)
* Get My Items (GET /items/) ← 自分のデータのみ
* Get Item by ID (GET /items/{item_id})
* Update Item (PUT /items/{item_id})
* Delete Item (DELETE /items/{item_id})

---

## 技術スタック

* Python
* FastAPI
* SQLAlchemy
* SQLite
* JWT認証

---

## 使い方

### ① サーバー起動

```bash
uvicorn main:app --reload
```

---

### ② Swagger UI

```
http://127.0.0.1:8000/docs
```

---

### ③ 利用手順

1. ユーザー登録
2. ログインしてトークン取得
3. 「Authorize」でトークンを設定
4. APIを実行

---

## 実装のポイント

### ■ user_id によるデータ管理

Itemに user_id を持たせ、ログインユーザーと紐付け

```python
user_id = current_user.id
```

---

### ■ 自分のデータのみ取得

```python
db.query(Item).filter(Item.user_id == current_user.id).all()
```

---

### ■ 他人のデータ操作を防止

```python
.filter(Item.id == item_id, Item.user_id == current_user.id)
```

---

## 今後の改善（予定）

* 管理者権限の追加
* ページネーション対応
* テストコード追加

---

## セキュリティ設計

本APIでは、他人のデータにアクセスした場合でも「存在しないデータ」として扱い、404を返しています。

これにより、
- データの存在有無を第三者に知られない
- 情報漏洩を防ぐ設計としています。

```python
if item is None:
    raise HTTPException(status_code=404, detail="Item not found")
```

---

## プロジェクト構成

web-study/
├── auth.py
├── crud.py
├── database.py
├── dependencies.py
├── main.py
├── models.py
├── schemas.py
└── routers/
    ├── items.py
    └── users.py

---

## 学習ポイント

* FastAPIによるREST API設計
* JWTを用いた認証処理
* user_idを用いた認可制御
* SQLAlchemyによるDB操作
* レイヤー分割(router /crud /schema)