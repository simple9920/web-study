# Item Management API

## 概要

FastAPIを使用した商品管理APIです。
ユーザー認証（JWT）と認可機能を実装し、
「ログインユーザーごとにデータを分離」しています。

---

## 機能一覧

### 🔹 認証（Authentication）

* ユーザー登録（POST /users/）
* ログイン POST /login （JWTトークン発行）
* JWTトークンでログインユーザーを特定

---

### 🔹 認可（Authorization）

* ログインユーザーごとにデータを管理
* user_idを使い、自分のデータのみ操作可能に制御
* 他人のデータは操作不可

---

### 🔹 CRUD機能

* Create Item (POST /items/)
* Get My Items (GET /items/) ← 自分のデータのみ取得(ページネーション・検索・並び替え対応)
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
* pytest(テスト)

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

### ④ 一覧取得のオプション

GET /items/ では以下のクエリパラメータが使用できます。

* skip：取得開始位置（例：0）
* limit：取得件数（例：10）
* name：商品名検索（部分一致）
* sort_by：並び替え項目(id / price)
* order：並び替え(asc / desc)

#### 使用例

```text
GET /items/?skip=0&limit=5
```
→ 最初の5件を取得

```text
GET /items/?name=apple
```
→「apple」を含む商品を検索


```text
GET /items/?skip=0&limit=2&name=apple
```
→「apple」を含むデータのうち、最初の2件を取得


```text
GET /items/?sort_by=price&order=desc
```
→ 価格の高い順に並び替え


```text
GET /items/?skip=0&limit=2&name=apple&sort_by=price&order=asc
```
→ 検索+ページネーション+並び替えを組み合わせ

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

### ■ ページネーション

```python
query.offset(skip).limit(limit).all()
```

---

### ■ 検索機能

```python
if name:
    query = query.filter(Item.name.contains(name))
```

---

### ■ 並び替え

```python
query = query.order_by(ItemModel.price.desc())
```

---

### ■ 入力バリデーション

```python
limit: int = Query(10, ge=1, le=50)
```

---

## 今後の改善（予定）

* 管理者権限の追加

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

## テスト

pytestを使用して、APIの動作確認を自動化しています。

* 入力バリデーションテスト(limitの範囲チェック)
* 認可テスト(他人データアクセス時の404確認)
* 認証テスト(未ログイン時の401確認)

---

## プロジェクト構成

```text
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
```

---

## 学習ポイント

* FastAPIによるREST API設計
* JWTを用いた認証処理
* user_idを用いた認可制御
* SQLAlchemyによるDB操作
* レイヤー分割(router / crud / schema)
* ページネーション・検索・並び替え・バリデーション機能の実装
* pytestを用いたAPIテストの実装
* 認証・認可・バリデーションを含むAPIのテスト設計
