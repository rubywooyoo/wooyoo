# SnapBuy Product V1 系統規格書

## 1. 文件目的

本文件定義 SnapBuy Product V1 的系統層級規格，作為前端、後端、資料庫、第三方整合與後續開發拆解的共同基準。

V1 的目標不是一次做完整平台，而是在最短時間內驗證以下假設：

- 買家願意在 LINE 生態中以沉浸式限動方式瀏覽並下單。
- 賣家願意把活動上架、訂單管理與客服導流到 SnapBuy。
- LINE LIFF 與 Messaging API 能支撐低摩擦登入、導購與通知。

## 2. 系統定位與範圍

### 2.1 Product V1 定位

SnapBuy V1 是一個 mobile-first 的 B2B2C Web App / PWA，服務兩種主要角色：

- 買家：瀏覽限時商品、加入購物車、付款、查訂單、發送商品詢問。
- 賣家：建立活動、上架商品、管理規格與庫存、處理訂單、回覆訊息、推送 LINE 通知。

### 2.2 In Scope

- 買家首頁、限動瀏覽、購物車、訂單列表
- 賣家後台首頁、活動管理、商品管理、訂單管理、客服訊息中心
- LINE LIFF 登入與頁面喚起
- LINE Flex Message 商品廣播
- 訂單狀態變更後的 LINE 推播
- 基礎金流串接
- 商品規格、活動、庫存、訂單、訊息等核心資料模型

### 2.3 Out of Scope

- 多語系
- 大型報表與 BI 分析
- 進階會員等級 / 點數 / 優惠券系統
- 多倉儲物流整合
- 平台型公開商城搜尋與推薦演算法
- 跨賣家整合結帳

## 3. 系統架構與技術選型

本專案採用前後端分離架構，並以 monorepo 形式統一管理。

### 3.1 Frontend - 買家 / 賣家 Web App

#### 核心框架

- React.js
- Vite

選擇理由：

- 啟動與建置速度快，適合快速迭代
- 生態成熟，方便整合 PWA、LIFF 與動畫套件
- 適合後續拆分 shopper 與 admin feature modules

#### UI 元件與樣式

- Tailwind CSS
- shadcn/ui

選擇理由：

- 快速建立 mobile-first、可客製化的設計系統
- 容易做出高一致性的表單、對話框、sheet、drawer、toast
- 能配合深色模式與玻璃擬態視覺風格

#### 動畫與手勢操作

- Framer Motion
- Swiper.js

套件分工：

- Framer Motion：處理上滑展開詳情、下滑收合、卡片進出場、底部 CTA 動畫
- Swiper.js：處理活動之間的左右切換、限動畫面滑動容器與 progress 行為

#### 狀態管理

- Zustand

建議 store 切分：

- `authStore`
- `buyerHomeStore`
- `storyStore`
- `cartStore`
- `orderStore`
- `adminCampaignStore`
- `adminProductStore`
- `adminOrderStore`
- `chatStore`

#### LINE 整合

- LINE LIFF SDK

用途：

- 在 LINE App 內啟動 Web App
- 取得使用者登入態與 LINE profile
- 交換後端 JWT，建立 SnapBuy session

### 3.2 Backend - API 伺服器

#### 核心框架

- Python
- FastAPI

選擇理由：

- 非同步支援佳，適合 API 與第三方整合
- 自帶 OpenAPI 文件，利於前後端協作
- 開發效率高，適合新創早期快速迭代

#### ORM / Schema

- SQLAlchemy
- Pydantic

#### 資料庫

- PostgreSQL

選擇理由：

- 適合處理 Campaign、Product、Variant、Order 等關聯資料
- 容易支援交易一致性與庫存扣減
- 未來可擴充全文搜尋、JSONB、審計欄位等能力

#### 背景任務與排程

- Celery
- Redis

用途：

- 訂單狀態異動後發送 LINE 推播
- 未付款訂單逾時自動取消
- 活動倒數狀態同步
- 非同步處理圖片轉檔、縮圖或 Webhook 任務

### 3.3 預期部署形態

V1 建議至少區分以下服務：

- `frontend-web`
- `backend-api`
- `postgres`
- `redis`
- `celery-worker`
- `celery-beat`

## 4. Monorepo 目錄結構

```text
snapbuy-monorepo/
├── frontend/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── features/
│   │   ├── hooks/
│   │   ├── layouts/
│   │   ├── pages/
│   │   ├── router/
│   │   ├── store/
│   │   ├── services/
│   │   ├── types/
│   │   ├── utils/
│   │   └── App.jsx
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── crud/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── tasks/
│   │   └── main.py
│   ├── requirements.txt
│   └── .env
│
├── docs/
│   └── product_v1/
└── README.md
```

### 4.1 前端模組責任

- `components/`：跨功能共用元件
- `features/`：以功能聚合畫面、hooks、api client、state
- `pages/`：路由對應頁面
- `services/`：呼叫 API、LIFF SDK、支付 SDK
- `utils/`：日期、價格、倒數計時、圖片處理等工具

### 4.2 後端模組責任

- `api/`：routers 與 API versioning
- `core/`：設定、JWT、權限、例外處理
- `crud/`：對 DB 的基礎查詢與資料更新
- `services/`：串接 LINE、支付、檔案儲存等外部服務
- `tasks/`：Celery 非同步工作

## 5. 設計系統與 UI/UX 規範

要吸引習慣使用 IG、TikTok 的買家，V1 的 UI 必須降低認知負擔、突出視覺節奏，並且保留明顯的即時感與限時感。

### 5.1 整體視覺風格

- 玻璃擬態（Glassmorphism）
- Dark mode first
- 大圖滿版與層次化半透明遮罩
- 微交互明確但不過度浮誇

### 5.2 色彩配置

- Background: `#121212` / `#1E1E1E`
- Primary Accent: `#8B5CF6` 或 `#F97316`
- Text Primary: `#FFFFFF`
- Text Secondary: `#A1A1AA`
- Success: `#22C55E`
- Warning: `#F59E0B`
- Danger: `#EF4444`

### 5.3 字體配置

- 中文：Noto Sans TC
- 英文 / 數字：Inter 或 Roboto Mono

建議用法：

- 商品名稱：`font-semibold`
- 價格與倒數：數字字重偏重，利於視覺掃描
- 後台資料欄位：以可讀性優先，避免過度裝飾

### 5.4 核心視覺元素

- 邊角圓角：`16px` 或 `24px`
- 限動 bubble 外圈：漸層描邊提示未讀
- 商品主視覺：full-bleed image
- 文字覆蓋區：半透明漸層遮罩 + backdrop blur
- CTA：固定底部、保持拇指可達範圍

### 5.5 互動原則

- 重要操作最多兩步內完成
- 上滑看詳情、下滑返回的狀態必須被保留
- 倒數、庫存、活動狀態必須清楚可見
- 付款、加入購物車、客服詢問需隨時可達

## 6. 角色與權限模型

### 6.1 主要角色

- `buyer`
- `seller`
- `admin`（平台內部管理用途，非 V1 核心畫面）

### 6.2 權限原則

- 買家只能讀取公開販售資料與自己的訂單 / 訊息
- 賣家只能操作自己名下 Seller / Campaign / Product / Order / Message
- 所有管理 API 需驗證 seller 身份與資源 ownership

## 7. 功能模組與頁面規劃

## 7.1 買家端 (Frontend - PWA / LIFF)

### 買家首頁 (Hub)

- Route: `/`
- 功能：
- 頂部限動圈圈水平滑動列
- 網格總覽商品與活動
- 倒數計時與活動狀態展示
- 底部導覽列：首頁、我的訂單、購物車、聊聊

實作重點：

- 首屏效能要好，避免首頁載入過慢
- 圖片採 lazy loading
- 首頁資料由單一聚合 API 回傳，減少多次往返

### 沉浸式限動視圖 (Cube UI)

- Route: `/story/:campaignId`

功能：

- 左右點擊切換同活動中的商品
- 左右滑動切換活動
- 上滑開啟商品詳情
- 底部固定 CTA：回覆、收藏、購買

實作重點：

- 保留商品索引與瀏覽進度
- 詳情展開時不丟失當前 story 狀態
- 需支援暫停自動播放或手動控制

### 購物車與結帳

- Route: `/cart`

功能：

- 顯示品項、規格、單價、數量、小計
- 顯示運費與訂單總額
- 選擇付款方式
- 建立訂單與導向支付流程

實作重點：

- 規格缺貨需即時阻擋
- 下單前再次驗證價格與庫存
- 付款失敗需可回到購物車重試

### 買家訂單管理

- Route: `/orders`

功能：

- Tab 切換：處理中、待付款、已出貨、已完成、已取消
- 顯示訂單編號、建立時間、總額、狀態
- 顯示物流單號或取貨資訊

### 聊聊 / 客服對話

- Route: `/chat`

功能：

- 依 seller / 商品串接對話脈絡
- 帶商品卡片引用送出訊息
- 查看賣家回覆與系統通知

## 7.2 賣家端 (Frontend - Admin Dashboard)

### 營運總覽

- Route: `/admin`

功能：

- 今日營收
- 待付款訂單數
- 待出貨訂單數
- 熱銷商品排行
- 活動進行中 / 即將結束提醒

### 活動與商品管理

- Routes:
- `/admin/campaigns`
- `/admin/products`

功能：

- 建立活動與設定時間區間
- 商品建檔
- 上傳主圖 / 副圖
- 管理商品分類、價格、規格、庫存
- 將商品關聯至多個活動

實作重點：

- 建立商品與活動的 many-to-many 關聯
- 規格表單需支援多組 option values
- 上傳圖片後可預覽主圖與詳情圖

### 訂單管理 (Kanban)

- Route: `/admin/orders`

功能：

- 看板欄位：待付款、已付款、待出貨、已出貨、已完成、已取消
- 可拖曳更新狀態
- 支援搜尋、篩選與批次操作

實作重點：

- 拖曳更新後需 optimistic update + rollback
- 狀態異動需寫入 audit trail
- 狀態變更會觸發通知工作

### 客服訊息中心

- Route: `/admin/chat`

功能：

- 左側顯示對話列表
- 右側顯示訊息內容
- 對話上方顯示商品引用卡片

## 8. 核心使用流程

### 8.1 買家購買流程

1. 買家在 LINE 群組看到 Flex Message。
2. 點擊後以 LIFF 開啟 SnapBuy 對應頁面。
3. 系統完成 LIFF 初始化與 JWT 登入交換。
4. 買家瀏覽活動 / 商品，選規格後加入購物車。
5. 進入結帳頁，建立訂單並導向金流。
6. 支付完成後，後端更新訂單狀態並推播通知。

### 8.2 賣家上架流程

1. 賣家登入後台建立 Campaign。
2. 建立 Product 與 Product Variants。
3. 將商品掛入一個或多個 Campaign。
4. 系統生成可分享的頁面與 LINE Flex Message。
5. 賣家將內容推送到 LINE 群組。

### 8.3 訂單履約流程

1. 買家完成付款。
2. 訂單狀態轉為 `paid`。
3. 賣家於後台出貨並更新狀態為 `shipped`。
4. 背景任務推送 LINE 通知給買家。
5. 訂單完成後可進入 `completed`。

## 9. 核心資料模型

## 9.1 主要資料表

### Users

欄位建議：

- `id`
- `line_user_id`
- `display_name`
- `avatar_url`
- `role`
- `last_login_at`
- `created_at`
- `updated_at`

### Sellers

- `id`
- `owner_user_id`
- `name`
- `slug`
- `description`
- `announcement`
- `logo_url`
- `cover_url`
- `is_active`
- `created_at`
- `updated_at`

### Seller_Filters

- `id`
- `seller_id`
- `name`
- `sort_order`

用途：

- 給買家作為商品分類篩選依據，例如美妝、服飾、保健

### Campaigns

- `id`
- `seller_id`
- `name`
- `description`
- `start_at`
- `end_at`
- `status`
- `cover_image_url`
- `sort_order`
- `created_at`
- `updated_at`

狀態建議：

- `draft`
- `scheduled`
- `active`
- `ended`
- `archived`

### Products

- `id`
- `seller_id`
- `title`
- `description`
- `base_price`
- `main_image_url`
- `status`
- `filter_id`
- `created_at`
- `updated_at`

### Product_Images

- `id`
- `product_id`
- `image_url`
- `image_type`
- `sort_order`

`image_type` 建議值：

- `main`
- `detail`

### Product_Variants

- `id`
- `product_id`
- `sku`
- `option_value_1`
- `option_value_2`
- `option_value_3`
- `price_override`
- `stock`
- `reserved_stock`
- `status`

### Campaign_Product_Link

- `id`
- `campaign_id`
- `product_id`
- `story_sort_order`
- `is_featured`
- `created_at`

### Carts

- `id`
- `buyer_user_id`
- `seller_id`
- `status`
- `created_at`
- `updated_at`

### Cart_Items

- `id`
- `cart_id`
- `product_id`
- `variant_id`
- `quantity`
- `unit_price`

### Orders

- `id`
- `order_no`
- `buyer_user_id`
- `seller_id`
- `subtotal_amount`
- `shipping_amount`
- `discount_amount`
- `total_amount`
- `payment_status`
- `fulfillment_status`
- `payment_method`
- `shipping_method`
- `receiver_name`
- `receiver_phone`
- `receiver_address`
- `remark`
- `created_at`
- `updated_at`

### Order_Items

- `id`
- `order_id`
- `product_id`
- `variant_id`
- `product_title_snapshot`
- `variant_snapshot`
- `unit_price`
- `quantity`
- `subtotal_amount`

### Messages

- `id`
- `seller_id`
- `buyer_user_id`
- `product_id`
- `order_id`
- `sender_type`
- `message_type`
- `content`
- `created_at`

### Line_Message_Logs

- `id`
- `target_type`
- `target_id`
- `message_category`
- `status`
- `request_payload`
- `response_payload`
- `created_at`

## 9.2 資料一致性原則

- 建立訂單時必須再次驗證 variant 庫存
- 扣庫存應以 transaction 處理
- 已付款訂單若取消，需明確區分退款與回補庫存流程
- 商品標題、價格、規格應 snapshot 到 `Order_Items`

## 10. API 規格

所有 API 以 `/api/v1` 為前綴。

## 10.1 Auth & LIFF

### `POST /api/v1/auth/liff-login`

用途：

- 接收 LINE access token 或 LIFF context
- 驗證使用者身份
- 建立或更新本地 `Users`
- 回傳 SnapBuy JWT 與使用者基本資料

### `GET /api/v1/auth/me`

用途：

- 取得目前登入者資訊與角色

## 10.2 Buyer APIs

### `GET /api/v1/buyer/home`

回傳內容建議：

- seller 基本資訊
- story bubbles
- active campaigns
- grid products
- cart summary
- announcement

### `GET /api/v1/buyer/campaigns/{campaign_id}/story`

回傳內容建議：

- campaign 資訊
- story product sequence
- 每個商品的主圖、倒數、價格、最小規格資訊
- 前後活動導覽資訊

### `GET /api/v1/buyer/products/{product_id}`

用途：

- 取得商品詳情、規格、圖片、庫存與可下單狀態

### `GET /api/v1/buyer/orders`

用途：

- 取得買家自己的訂單列表

## 10.3 Cart & Orders APIs

### `POST /api/v1/cart/items`

用途：

- 加入購物車

### `PATCH /api/v1/cart/items/{item_id}`

用途：

- 更新數量或規格

### `DELETE /api/v1/cart/items/{item_id}`

用途：

- 移除購物車項目

### `GET /api/v1/cart`

用途：

- 取得目前購物車內容

### `POST /api/v1/orders/checkout`

用途：

- 建立訂單
- 保留或扣減庫存
- 建立支付請求
- 回傳付款 URL 或 token

### `POST /api/v1/payments/webhook`

用途：

- 接收第三方金流支付結果
- 更新訂單付款狀態

## 10.4 Seller Admin APIs

### `POST /api/v1/admin/campaigns`

用途：

- 建立活動

### `GET /api/v1/admin/campaigns`

用途：

- 取得賣家活動列表

### `POST /api/v1/admin/products`

用途：

- 建立商品與規格

### `PATCH /api/v1/admin/products/{product_id}`

用途：

- 更新商品資料、圖片、規格、關聯活動

### `GET /api/v1/admin/orders`

用途：

- 取得訂單看板資料

### `PATCH /api/v1/admin/orders/{order_id}/status`

用途：

- 更新付款或履約狀態
- 觸發背景任務發送 LINE 推播

### `GET /api/v1/admin/messages`

用途：

- 取得訊息列表與對話摘要

### `POST /api/v1/admin/messages`

用途：

- 回覆買家訊息

## 11. LINE 整合規格

## 11.1 LIFF

- 將 shopper web app 註冊為 LIFF App
- 在 app 啟動時執行 `liff.init()`
- 若使用者已登入 LINE，直接取得 profile 與 access token
- 將 token 傳給後端交換 JWT

必要能力：

- deep link 到指定 Campaign / Product / Order
- 從 Flex Message 直接開啟對應頁面

## 11.2 Messaging API

### 商品廣播

- 賣家發布活動或商品後可一鍵發送 Flex Message
- 卡片需包含主圖、商品名稱、活動剩餘時間、CTA

### 訂單通知

- 待付款提醒
- 已付款確認
- 已出貨通知
- 例外狀態通知

## 11.3 Flex Message 結構建議

- Header：活動名稱 / 限時標籤
- Hero：商品主圖
- Body：商品名、價格、倒數
- Footer：立即查看 / 立即搶購按鈕

## 12. 支付與訂單狀態設計

### 12.1 支付方式

V1 可先規劃以下支付整合：

- 信用卡
- LINE Pay
- 虛擬帳號

### 12.2 訂單狀態拆分

建議不要只用單一欄位表示訂單狀態，應拆為：

- `payment_status`
- `fulfillment_status`

`payment_status` 建議值：

- `unpaid`
- `paid`
- `failed`
- `refunded`

`fulfillment_status` 建議值：

- `pending`
- `processing`
- `shipped`
- `completed`
- `cancelled`

## 13. 非功能需求

### 13.1 效能

- 首頁 API 在正常資料量下應維持可接受響應時間
- 圖片需壓縮與 lazy load
- 限動畫面切換需避免明顯掉幀

### 13.2 安全

- JWT 驗證與 refresh 策略
- API 權限檢查
- Webhook 驗簽
- 敏感資料避免明文紀錄

### 13.3 可觀測性

- API request logging
- 第三方整合失敗紀錄
- 任務佇列失敗重試機制
- 關鍵事件審計紀錄

### 13.4 維運性

- `.env` 管理外部金鑰
- 分離 dev / staging / production 環境
- 預留 migration 機制

## 14. 風險與待確認事項

- LINE 群組場景下的實際導購轉換率仍需驗證
- 不同金流在 LIFF 內嵌瀏覽器中的相容性需測試
- 訂單逾時取消與回補庫存的規則需再細化
- 客服訊息中心是否需要即時通訊能力，V1 可先以準即時輪詢實作
- 賣家是否需要多人協作後台，V1 可先不納入

## 15. 建議後續文件

- `prd.md`：需求、user stories、acceptance criteria
- `api_contract.md`：request / response payload 實例
- `erd.md`：資料表關聯圖
- `user_flows.md`：買家與賣家主要操作流程圖
