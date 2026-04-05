# SnapBuy

SnapBuy 是一個為 LINE 社群代購場景打造的限時電商小助手，目標是把「商品展示、下單、付款、訂單狀態、賣家管理」從混亂的群組訊息中抽離，交由系統處理；同時保留 LINE 作為互動、預告、客服與社群經營的主場。

產品定位不是要取代賣家原本的 LINE 私域，而是補上一層交易基礎建設，讓賣家能更快上架、更準確接單、更省力管理，讓買家能在熟悉的 LINE 生態中直接完成更流暢的購買體驗。

## 專案索引

### 核心文件

- [產品概述 v1](docs/limited_time_proxy_shopping_saas_overview_v1.md)
- [產品概述 v0](docs/limited_time_proxy_shopping_saas_overview_v0.md)
- [Product V1 MVP 規劃](docs/product_v1/product_v1_plan.md)
- [Product V1 系統規格書](docs/product_v1/product_v1_system_spec.md)

### 文件閱讀順序

1. 先讀 [產品概述 v1](docs/limited_time_proxy_shopping_saas_overview_v1.md)，理解產品定位、目標用戶、痛點與商業模式。
2. 再讀 [Product V1 MVP 規劃](docs/product_v1/product_v1_plan.md)，掌握第一版要做哪些功能與體驗。
3. 最後讀 [Product V1 系統規格書](docs/product_v1/product_v1_system_spec.md)，對齊技術架構、模組邊界、頁面規格、API 與資料模型。

## 專案介紹

### 核心問題

目前多數 LINE 代購群組有幾個共通問題：

- 商品資訊與聊天訊息混在一起，容易洗版。
- 下單通常仰賴私訊、喊單、人工確認，流程斷裂。
- 金流與對帳大多仰賴轉帳截圖，賣家管理成本高。
- 傳統電商平台偏向常態商品，不適合限時、短週期、連線式代購。

### SnapBuy 的解法

SnapBuy 把社群代購拆成兩個層次：

- 交易層：由 SnapBuy 提供商品展示、購物車、付款、訂單追蹤、賣家後台。
- 社群層：由 LINE 群組與官方帳號承接預告、互動、客服與通知。

這樣的分工讓賣家不用放棄原本的客群與經營模式，也讓買家不必離開熟悉的 LINE 情境。

### Product V1 範圍

V1 以 mobile-first 的 PWA / LIFF Web App 為核心，聚焦三條主線：

- 買家端沉浸式限動購物體驗
- 賣家端活動、商品、訂單、客服管理後台
- 與 LINE LIFF / Messaging API / Flex Message 的整合

## 規劃中的專案結構

目前 repo 以文件規劃為主，V1 預計採用 monorepo 形式，包含前後端兩個主要應用。

```text
snapbuy-monorepo/
├── frontend/         # React + Vite + Tailwind + shadcn/ui
├── backend/          # FastAPI + SQLAlchemy + PostgreSQL
├── docs/             # 產品規劃、PRD、系統規格、流程文件
└── README.md
```

詳細的目錄規劃、模組責任與技術選型，請參考 [Product V1 系統規格書](docs/product_v1/product_v1_system_spec.md)。

## 當前狀態

目前已建立 Product V1 的第一版可運行骨架：

- `backend/`：FastAPI + SQLAlchemy + 核心資料模型 + API 路由雛形
- `frontend/`：Vite + React + Tailwind + shopper/admin 路由與頁面骨架
- `docs/`：產品概述、MVP 規劃、系統規格書

目前階段屬於 scaffold 實作，核心流程與 UI 結構已落地，但商業邏輯（完整庫存交易、支付 webhooks、LINE 推播任務、權限驗證）仍在後續迭代中。

## 本機啟動

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

- API 文件：`http://127.0.0.1:8000/docs`
- 健康檢查：`http://127.0.0.1:8000/health`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

- 開發站點：`http://127.0.0.1:5173`

## 下一步建議

- 串接前端頁面到後端 API（先打通 `/api/v1/buyer/home` 與 `/api/v1/admin/products`）。
- 補上資料庫 migration（Alembic）與 seed data。
- 導入 JWT 真正簽發與權限驗證 middleware。
- 實作支付 webhook、訂單狀態流轉與 LINE 推播任務。
