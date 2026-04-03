[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/5PhkpLhw)
# Wooyoo.Studio — 即時代購交易管理系統

---

## 1. 專案簡介

### 設計動機

現代人生活節奏緊湊，實體購物時間大幅縮減，且受限於跨國價差，代購產業憑藉價格優勢與網路便利性，始終是實體通路強有力的競爭者，而我身為一位資深代購使用者，也觀察到了此領域的運作模式正發生顯著的變革！

過去，代購多採用「先囤貨後販售」的模式，並以蝦皮、Facebook 或品牌官網為主要通路。然而，隨著賣家門檻降低與經營策略轉向，強調低庫存風險的「小資連線模式」逐漸盛行。賣家傾向在 LINE 社群進行即時互動，透過上傳商品照、買家留言「+1」並先行匯款後才下單。雖然此模式極小化了囤貨壓力，卻也對買賣雙方的交易效率與溝通流程帶來了新的痛點與挑戰。

### 核心痛點分析 (Pain Points)

目前的社群代購模式雖然門檻低，但在資訊管理上存在顯著缺陷：

#### 針對賣家 (Seller Side)
* **資訊干擾嚴重**：群組內充斥廣告與詐騙訊息，干擾正常交易流程。
* **狀態更新不及時**：商品照片與聊天訊息混雜，導致買家難以辨識商品是否已結束預訂。
* **報價流程瑣碎**：需反覆回覆買家詢價，資訊不透明且缺乏效率。

#### 針對買家 (Buyer Side)
* **訊息過載與遺失**：在大群組中提問易被洗板，且難以追蹤特定商品的剩餘數量與價格。
* **交易門檻高**：轉帳流程繁瑣，需額外添加好友、手動提供出貨資訊，操作不便。
* **隱私與社交壓力**：部分買家不習慣在公開大群組留言互動。

---

### 解決方案：理想系統願景 (Proposed Solution)

我想開發的理想系統是一個對賣家與買家都友善的平台：賣家可以根據每次代購檔期建立行程、上架商品並設定接單時限；買家可以直接在系統下單、收到即時通知、在商品頁留言，不再依賴混亂的 LINE 群組，為了達成這個目標，以下爲解決方案：

* **結構化管理**：賣家可根據代購檔期建立行程，並設定明確的接單時限。
* **系統化下單**：買家直接在商品頁面下單、留言並接收即時進度通知。
* **去中心化通訊**：擺脫對混亂 LINE 群組的過度依賴。

### v1.0 實作範疇 (Scope of v1.0)

受限於本次開發環境（CLI 範疇），本版本專注於驗證**核心交易流程**。我們以**賣家視角**為出發點，實作以下後端基礎功能：

1. **行程管理**：規劃代購檔期與品牌攤位。
2. **商品維護**：處理商品上架與庫存邏輯。
3. **訂單管理**：追蹤訂單生成與收付狀態。

此 v1.0 成果將作為未來完整 Web/App 系統的商務邏輯基石。

### v1.0 功能概覽

Wooyoo.Studio v1.0 是一套純 CLI 的代購交易後台，支援以下核心操作：

- **Trip（代購行程）**：建立與列出代購檔期
- **Booth（品牌攤位）**：管理行程中依拜訪順序排列的品牌店
- **Item（商品）**：上架商品、設定接單時限、管理庫存與狀態
- **Order（訂單）**：接單、確認付款、取消訂單並自動還原庫存

### 從 v1.0 到 v2.0 的演化摘要

v2.0 基於 v1.0 的架構，針對真實代購場景中浮現的三個痛點進行延伸：

1. **資料後端從 JSON 升級至 SQLite**：v1.0 每次讀寫都載入整份 `data.json`，訂單量一大效能明顯下降。v2.0 引入 `storage_sqlite.py` 作為 drop-in 替換，資料持久化於 `v2/wooyoo.db`，v1.0 原有資料與測試環境不受影響。

2. **新增 `order update`：買家可修改 PENDING 訂單數量**：v1.0 的訂單一旦下出就無法調整，買家要追加數量只能取消重下，導致庫存紀錄混亂。v2.0 加入數量修改指令，並同步調整商品剩餘庫存，PAID 和 CANCELLED 訂單不允許修改。

3. **新增 `trip summary`：跨層行程收款總覽**：賣家過去需逐一查詢每個攤位的每件商品才能掌握整趟行程的收款狀況。v2.0 一次彙整 Trip → Booth → Item → Order 四層資料，輸出 PAID 總金額、PAID 筆數與 PENDING 筆數。

4. **`booth add` 新增選填備註 `--note`**：賣家可在建立攤位時附加簡短備註（如「限量需排隊」），顯示於 `booth list` 輸出，不影響 v1.0 的必填參數行為。

---

## 2. v1.0 設計決策（Design Decisions）

### 2-1. 選擇 `typer` 而非 `argparse`

`argparse` 是標準庫，但擴充性有限，新增子指令群組的語法繁瑣，也不原生支援型別驗證。`typer` 基於 Python type hints，每個指令都是獨立函式，v2.0 新增任何指令群組只需在 `main.py` 新增 `Typer()` 並 `add_typer()`，不會影響現有指令的定義與行為。

我在選 CLI library 之前試寫過 `argparse` 版本，光是定義 `trip create` 和 `booth add` 兩組子指令就已經覺得結構混亂。這個系統的指令天然會按資料層分群，`typer` 的 sub-app 設計剛好對應這個結構，每一層（trip / booth / item / order）是一個獨立的 Typer 群組，加新指令不會碰到其他群組，這對我後來加 `trip summary` 和 `order update` 非常有幫助。

### 2-2. 三層模組分離：`main.py` / `commands.py` / `storage.py`

- `main.py`：純路由，只做 CLI 定義與參數轉發，不含任何業務邏輯
- `commands.py`：業務邏輯驗證與格式化輸出，不直接碰資料
- `storage.py`：唯一的資料存取層，不含業務邏輯

這個分離讓 v2.0 的每種升級都只需動一個檔案：換儲存後端只改 `storage.py`、升級輸出格式只改 `commands.py`、新增指令只改 `main.py`。

這個設計的出發點其實很直接：我知道這個系統未來一定會繼續改，如果三件事混在一起，每次改動都要同時看懂三種邏輯才能下手。三層分離之後，我改輸出格式只需要看 `commands.py`，不需要擔心自己不小心動到資料讀寫邏輯。v2.0 實際開發時確實驗證了這個判斷，加 `trip summary` 的過程中 `main.py` 完全沒有需要理解業務邏輯的時刻。

### 2-3. `storage.py` 作為唯一 I/O 層，預留儲存後端替換空間

`main.py` 與 `commands.py` 完全不知道 `data.json` 的存在，所有資料讀寫都封裝在 `storage.py` 的函式介面後面。v2.0 若需升級至 SQLite 或其他資料庫，只需提供一個同介面的 `storage_sqlite.py` 並替換 import，上層邏輯零修改。

在設計 v1.0 時，我最確定「未來一定會改」的地方就是儲存後端。當訂單量一大，每次讀寫都載入整份 JSON 是說不通的，而我又想讓這個系統未來有機會真正上線，所以才特別把 I/O 完整封裝成一個可抽換的層，而不是讓資料存取散落在各個函式裡。

### 2-4. 所有 dataclass 含 `metadata: dict` 預留欄位

Trip、Booth、Item、Order 四個資料模型都有 `metadata: dict`（預設空字典），因此 v2.0 新增欄位時，可先存入 `metadata`，不破壞現有 JSON 結構，也不需要資料遷移腳本。目前 v1.0 已用此機制儲存 Item 的 `force_closed` 與 `fulfilled` 旗標。

`metadata` 的設計初衷是為了應對我尚未確定的需求。現實中，一個系統要真正上線，勢必需要做市場調查，搜集買賣家的實際使用回饋後才能決定要新增哪些欄位。`metadata` 讓我可以先保留彈性，等到有了真實的問卷或用戶訪談結果，再決定哪些欄位值得升格為正式欄位，而不是現在就猜測所有可能性。

### 2-5. `Item.get_status()` 動態計算，狀態不寫入 JSON

Item 的狀態（`OPEN / EXPIRED / CLOSED / FULFILLED`）不存入 JSON，而是每次讀取時由 `get_status()` 即時計算。這使得：
- `EXPIRED` 狀態完全自動，不需要任何排程或 cron job
- v2.0 新增狀態或修改觸發條件，只需改這一個方法
- JSON 不會因為狀態變更而需要大量更新

這個設計是從代購的真實場景出發的。賣家在現場開放接單的時候，根本不會有時間手動去更新每個商品的狀態，`EXPIRED` 必須是自動發生的。如果把狀態存進去，就意味著需要某個背景程序去定時更新它，但這是一個 CLI 工具，沒有背景服務。動態計算讓時間截止這件事完全由程式負責，賣家不需要做任何額外操作。

### 2-6. Trip → Booth → Item → Order 四層資料模型

資料模型刻意設計成四層關聯，對應代購的真實業務結構：一趟行程（Trip）拜訪多個品牌店（Booth），每個品牌店有多件商品（Item），每件商品收多筆訂單（Order）。這個層級結構天然適合關聯式資料庫，v2.0 升級 SQLite 時可直接對應為四張表，外鍵關係已在資料模型中明確定義。

這四層不是憑空設計的，而是我身為代購用戶實際觀察到的運作方式。賣家每一趟韓國行程會逛好幾個品牌，每個品牌店會有複數商品，每件商品可能同時有多個買家搶著下單。這個層級如果壓扁成三層甚至兩層，就無法精確反映「同一趟行程、不同品牌、不同商品、各自的訂單狀態」這種查詢需求，而 `trip summary` 正是這個設計最直接的受益者。

### 2-7. `buyer_name` / `buyer_phone` 結構化存入 Order

訂單直接儲存買家姓名與電話，而非僅作為文字備註。這為 v2.0 加入買家帳號系統預留空間——屆時可將 `buyer_phone` 作為識別鍵與買家帳號關聯，或新增「查詢某買家的所有訂單」等跨層查詢功能，不需要修改資料模型結構。

v1.0 的範疇刻意只實作賣家端，是因為我認為要先把核心交易流程跑通，再開放買家自助操作才是合理的順序。但我心裡清楚這個系統最終要對買家友善，所以在訂單裡結構化儲存買家資訊，而不是把姓名電話塞成一個備註字串。一旦未來要做買家帳號，`buyer_phone` 直接就可以作為識別鍵，不需要回頭改資料模型。

### 2-8. `--minutes` 而非 `--deadline`

`item add` 接受的是「開放接單幾分鐘」，而不是「幾點截止」。這個選擇是從代購現場的使用情境出發的：賣家在店裡當場上架商品，根本不會先計算好截止時間點再輸入，但他很清楚「這件開放 30 分鐘」。讓賣家輸入分鐘數，系統自動計算 deadline，比讓賣家輸入一個精確的時間字串更符合現場操作的直覺，也避免輸入格式錯誤的問題。

### 2-9. `visit_order` 作為獨立欄位，而非依 id 排序

Booth 有一個獨立的 `visit_order` 欄位決定攤位的拜訪順序，而不是直接用建立時間或 id 排序。原因是賣家規劃行程時，實際的拜訪路線可能和建立順序不一致，或者臨時決定調換兩個品牌的先後順序。如果用 id 排序，要改順序就必須刪掉重建；用獨立欄位，未來只需要更新數字即可，不影響資料完整性。

### 2-10. 輸出關鍵字明確固定

`commands.py` 的每個指令輸出都包含固定的關鍵字（`Created`、`Added`、`Order placed`、`Confirmed`、`Cancelled`、`OPEN`、`PENDING`、`PAID` 等），並在 `sdd_v1.md` 的測試案例中明確記錄。v2.0 升級輸出格式時，只要確保這些關鍵字仍出現在 stdout，向下相容性測試即可通過，不需要維持完全相同的輸出格式。

固定關鍵字這件事我是刻意為之的。我知道 v2.0 的輸出格式可能會調整（例如多一欄 Note），如果測試案例是檢查「整行輸出完全一致」，那每次格式微調都會讓測試失敗，維護成本很高。用關鍵字作為驗收標準，給了輸出格式足夠的調整空間，同時又能確認核心行為沒有被破壞。

---

## 2-11. v1.0 設計如何直接承載 v2.0 需求

收到 v2.0 需求後，我發現 v1.0 的幾個設計選擇幾乎都很好的預測了新需求的到來：

| v1.0 設計決策 | v2.0 對應需求 | 實際影響 |
|---|---|---|
| `storage.py` 作為唯一 I/O 層 | 需求一：將後端從 JSON 換成 SQLite | `commands.py` 只改 1 行 import，`main.py` 零修改 |
| 四層資料模型（外鍵關聯） | 需求三：trip summary 跨層彙整 | 四張 SQLite 表直接對應，聚合邏輯清晰 |
| `metadata: dict` 預留欄位 | 需求四：booth 新增備註欄位 | 選擇新增獨立欄位而非塞進 metadata，說明欄位設計有彈性 |
| `buyer_name` / `buyer_phone` 結構化存入 Order | 未來買家帳號系統 | v2.0 尚未要求，但資料已就位 |
| 輸出關鍵字固定於 SDD | 驗收標準：v1.0 測試案例全數通過 | v2.0 改了輸出格式（多 Note 欄），關鍵字仍在，12 個測試照過 |

v2.0 最耗時的部分其實是 `storage_sqlite.py` 的實作，但這是資料庫本身的工作量，不是架構問題。v1.0 的模組設計讓這個工作量完全局限在一個新檔案裡，沒有向上層滲透。

---

## 3. v2.0 實作說明

### 3-1. 如何閱讀並理解 v2.0 需求

Agent 產生的需求以 PRD 口吻撰寫，描述的是「使用者感受到的痛點」，而非技術規格。我的閱讀方式是將每個痛點映射回現有架構，判斷影響範圍：

- 需求一（SQLite）影響的是 `storage.py` 一個模組，`commands.py` 和 `main.py` 理論上不需動
- 需求二（order update）需要新增一條指令，影響三個檔案各一處（storage 加函式、commands 加業務邏輯、main 加路由）
- 需求三（trip summary）是跨層查詢，需要在 storage 層實作聚合邏輯，commands 層負責格式化輸出
- 需求四（booth --note）是單一欄位新增，影響 Booth dataclass、SQLite schema、以及 booth add / booth list 的輸入輸出

需求裡有一個地方需要我自己做判斷：`trip summary` 的輸出格式需求說「由開發者自行設計，但資訊必須具備可讀性」，還特別說「不可只是把 order list 的輸出全部串接」。我當時決定把輸出設計成「先列攤位與商品狀態，再最後彙總 PAID 金額與 PENDING 筆數」，原因是賣家在現場最常有兩種問題：「這件商品還有幾個可以賣」和「我這趟收了多少錢」，前者需要按商品看，後者需要一個總數，把兩種資訊分區呈現比混在一起更直觀。另外，需求也提到若無訂單應輸出提示而非空白，這個 edge case 我在程式裡也有對應處理。

### 3-2. 實作選擇說明

**drop-in 替換策略**：不修改 `storage.py`，另建 `storage_sqlite.py` 實作完全相同的公開介面（函式名稱、參數、回傳型別），`commands.py` 只改第 9 行的 import。這樣 v1 目錄完全不動，v2 和 v1 可在各自目錄獨立執行互不干擾。

我考慮過直接在 `storage.py` 上面改，但這樣 v1 的測試環境就會被影響。另建一個新模組代表兩個版本可以永遠並存，日後如果真的要切換其他後端（PostgreSQL 或雲端資料庫），一樣只要再提供一個同介面的模組就好，整個設計方向是一致的。

**SQLite schema 設計**：四張表對應四個 dataclass，欄位一對一映射，加上 FOREIGN KEY 確保資料完整性。`metadata` 欄位以 JSON 字串形式存入 TEXT 欄位，保留未來彈性。`Item` 的狀態（OPEN / EXPIRED / CLOSED / FULFILLED）仍不存入資料庫，沿用 `get_status()` 動態計算，邏輯與 v1 完全一致。

`booth` 的備註欄位我考慮過存入 `metadata`（v1 的 Booth dataclass 已有這個欄位），但最後選擇在 SQLite schema 中新增獨立的 `note TEXT` 欄位。原因是 `note` 是一個明確的業務需求，賣家會頻繁讀取它，獨立欄位查詢比每次都解析 JSON 字串更直接。`metadata` 我保留給那些還不確定、可能只是暫時用到的擴充。

**`_init_db()` 在 import 時自動執行**：使用 `CREATE TABLE IF NOT EXISTS`，確保程式啟動時若資料庫不存在會自動建表，若已存在則不清空。符合需求二「SQLite 資料持久化」的驗收標準。

**`order update` 的庫存計算**：以 `delta = new_qty - order.quantity` 計算差值，統一用 `update_item_remaining(item_id, -delta)` 調整庫存。delta 為正（追加）時扣庫存，delta 為負（減少）時還庫存，邏輯與 `order cancel` 的還庫存機制對稱一致。

**`get_trip_summary()` 在 storage 層實作**：跨層聚合邏輯放在 storage 而非 commands，是因為這個函式需要跨四張表做巢狀查詢，讓 commands 只負責格式化輸出，符合三層分離的原則。

---

## 4. 向下相容性實作細節

### 核心策略：drop-in 替換，不動上層

v2.0 向下相容的關鍵在於 v1.0 的三層架構預先將 I/O 完全封裝在 `storage.py` 後面。因此升級儲存後端只需：

1. 新建 `storage_sqlite.py`，實作與 `storage.py` 完全相同的公開函式簽名
2. 將 `commands.py` 第 9 行從 `import storage` 改為 `import storage_sqlite as storage`
3. `main.py` 完全不需修改

`main.py` 對儲存後端的替換毫無感知，這正是 v1.0 設計時預留 `storage.py` 作為唯一 I/O 層的成效。

### CLI 介面凍結原則

v1.0 截止後，所有已定義的指令名稱、參數名稱、輸出關鍵字均不可更動。v2.0 的實際變更如下：

| 變更類型 | 具體內容 |
|---|---|
| 新增指令 | `trip summary`、`order update` |
| 新增選填參數 | `booth add --note`（原必填參數行為不變） |
| 無任何修改 | v1.0 全部 12 個指令的參數與輸出關鍵字完整保留 |

### 輸出關鍵字保留清單

以下關鍵字在 v2.0 中完整保留，確保 sdd_v1.md 測試案例全數通過：

`Created`、`Added`、`Order placed`、`Confirmed`、`Cancelled`、`Closed`、`Fulfilled`、`OPEN`、`PENDING`、`PAID`、`CANCELLED`、`CLOSED`、`FULFILLED`

### 資料目錄分離

v2.0 使用 `v2/wooyoo.db`，v1.0 使用 `v1/data.json`，兩者完全獨立。v1.0 測試環境可在 `v1/` 目錄照常執行，v2.0 在乾淨的 `v2/wooyoo.db` 上執行向下相容測試，互不干擾。

---

## 5. 架構演化比較

| 面向 | v1.0 | v2.0 |
|---|---|---|
| 儲存層 | JSON 檔案（`v1/data.json`） | SQLite（`v2/wooyoo.db`） |
| I/O 模組 | `storage.py` | `storage_sqlite.py`（drop-in 替換） |
| CLI Library | typer | typer（不變） |
| 模組數量 | 3（main / commands / storage） | 3（main / commands / storage_sqlite） |
| 狀態管理 | 動態計算（`get_status()`） | 動態計算（邏輯不變，存於 metadata JSON 欄位） |
| 資料模型 | 4 個 dataclass，Booth 無備註欄位 | 4 個 dataclass，Booth 新增 `note` 欄位 |
| 指令數量 | 12 個指令 | 14 個指令（新增 `trip summary`、`order update`） |
| 跨層查詢 | 不支援 | `get_trip_summary()` 聚合四層資料 |
| 資料持久性 | 程式結束後 JSON 保留 | 程式結束後 SQLite 保留，不在啟動時清空 |
| 測試方式 | 手動執行測試案例（#1–12） | 手動執行測試案例（#1–12 向下相容 + #13–20 新功能） |

---

## 6. 環境需求與執行方式

### 環境需求

- Python 3.10+
- 依賴套件：`typer>=0.9.0`

### v1.0 安裝與執行

```bash
cd v1/
pip install -r requirements.txt
python main.py --help
```

### 常用指令範例

```bash
# 建立代購行程
python main.py trip create --name "首爾春季" --dest "首爾"

# 新增品牌攤位
python main.py booth add --trip-id 1 --name "MARDI MERCREDI" --order 1

# 上架商品（接單時限 30 分鐘）
python main.py item add --booth-id 1 --name "蠟菊針織上衣" --price 2800 --qty 3 --minutes 30

# 買家下單
python main.py order place --item-id 1 --buyer "Rosie" --phone "0912345678" --qty 1

# 確認付款
python main.py order confirm --order-id 1
```

### v2.0 安裝與執行

```bash
cd v2/
pip install -r requirements.txt
python main.py --help
```

### v2.0 常用指令範例

```bash
# 修改 PENDING 訂單數量
python main.py order update --order-id 1 --qty 3

# 查看整趟行程收款總覽
python main.py trip summary --trip-id 1

# 新增有備註的品牌攤位
python main.py booth add --trip-id 1 --name "ADER ERROR" --order 2 --note "限量商品需排隊"
```

### 測試前重置資料庫

```bash
rm -f v2/wooyoo.db
```

---

## 7. 已知限制與未來改進方向

### v1.0 已知限制

- 賣家視角操作：v1.0 所有指令均由賣家執行，買家無法自助下單，仍需透過賣家輸入
- 無併發保護：多人同時操作同一 `data.json` 時可能發生資料競爭
- 無身份驗證：任何人只要有 CLI 存取權限即可執行所有指令

### v2.0 已知限制

- 仍無併發保護：SQLite 支援多讀，但高頻率同時寫入仍可能發生鎖定衝突
- 無資料遷移腳本：v1.0 的 `data.json` 不會自動匯入 `wooyoo.db`，兩個版本的資料相互獨立
- 買家仍無法自助操作：所有指令仍由賣家端執行，買家自助下單需等待 Web 層

### 若有 v3.0 的設計方向

v2.0 確立了完整的四層資料模型（Trip → Booth → Item → Order）與 SQLite 持久化基礎，v3.0 可從以下方向繼續延伸：

**買賣雙方角色分離**
- v2.0 所有指令仍由賣家操作，買家資訊（姓名、電話）由賣家代為輸入
- v3.0 可引入買家帳號系統，讓買家以 `buyer_phone` 作為識別鍵自助下單、查詢自己的訂單
- `order place` 的 `--buyer` 與 `--phone` 參數可升級為帳號登入機制

**Web API 層**
- v2.0 的 `commands.py` 業務邏輯已與 CLI 路由分離，函式介面乾淨，可直接包裝為 FastAPI endpoint
- 提供 Web API 後，前端 App、LINE Bot 或 Instagram 商店頁面均可串接，讓買家不需要安裝 CLI 即可下單

**即時通知**
- v2.0 的 `item add --minutes` 設定了接單截止時間，這個時間點天然適合作為推播觸發條件
- 買家可訂閱特定行程或品牌，商品開始接單或即將截止時收到推播

**`trip summary` 的延伸：匯出與報表**
- v2.0 的 `trip summary` 已能彙整整趟行程的收款狀況，v3.0 可加入匯出 CSV 或 PDF 功能，讓賣家可以直接傳給買家或存檔對帳

**庫存預警**
- 目前 `item list` 需要手動查看剩餘庫存，v3.0 可在 `remaining` 低於門檻時自動標示警告，或在 `trip summary` 輸出中特別標出即將售罄的商品
