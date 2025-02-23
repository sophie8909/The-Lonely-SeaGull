# Database Schema

## 1. users (使用者表)

| Column Name    | Data Type              | Description              |
|----------------|------------------------|--------------------------|
| user_id        | INT PRIMARY KEY        | 使用者唯一 ID            |
| username       | VARCHAR(50) UNIQUE NOT NULL | 使用者帳號名稱      |
| first_name     | VARCHAR(50)            | 名字                     |
| last_name      | VARCHAR(50)            | 姓氏                     |
| email          | VARCHAR(100) UNIQUE NOT NULL | 電子郵件            |
| phone          | VARCHAR(20)            | 手機號碼                 |
| credentials    | INT NOT NULL           | 權限等級 (0: 客戶, 1: Bartender, 2: Owner, 3: VIP) |
| password  | VARCHAR(255) NOT NULL  | 密碼的哈希值             |

## 2. beers (酒品表)

| Column Name            | Data Type              | Description              |
|------------------------|------------------------|--------------------------|
| beer_id                | INT PRIMARY KEY        | 酒品唯一 ID              |
| nr                     | VARCHAR(10)            | 產品編號                 |
| articleid              | VARCHAR(10)            | 文章 ID                  |
| articletype            | VARCHAR(10)            | 文章類型                 |
| name                   | VARCHAR(100) NOT NULL  | 酒品名稱                 |
| name2                  | VARCHAR(100)           | 酒品名稱 2               |
| priceinclvat           | DECIMAL(10,2) NOT NULL | 含稅價格 (單位: SEK)     |
| volumeml               | INT                    | 容量 (毫升)              |
| priceperlitre          | DECIMAL(10,2)          | 每升價格 (單位: SEK)     |
| introduced             | DATE                   | 上市日期                 |
| finaldelivery          | DATE                   | 最後交貨日期             |
| category               | VARCHAR(50)            | 酒類分類 (如 啤酒, 威士忌 等) |
| packaging              | VARCHAR(50)            | 包裝方式 (如 瓶裝, 罐裝) |
| captype                | VARCHAR(50)            | 瓶蓋類型                 |
| countryoforigin        | VARCHAR(100)           | 產地                     |
| countryoforiginlandname| VARCHAR(100)           | 產地國家名稱             |
| producer               | VARCHAR(100)           | 製造商                   |
| provider               | VARCHAR(100)           | 供應商                   |
| productionyear         | VARCHAR(4)             | 生產年份                 |
| testedproductionyear   | VARCHAR(4)             | 測試生產年份             |
| alcoholstrength        | DECIMAL(5,2)           | 酒精濃度 (%)             |
| module                 | VARCHAR(50)            | 模組                     |
| assortment             | VARCHAR(50)            | 品類                     |
| organic                | BOOLEAN DEFAULT FALSE  | 是否有機 (TRUE / FALSE)  |
| kosher                 | BOOLEAN DEFAULT FALSE  | 是否猶太潔食 (TRUE / FALSE) |

## 3. beers_sold (銷售記錄表)

| Column Name   | Data Type              | Description              |
|---------------|------------------------|--------------------------|
| transaction_id| INT PRIMARY KEY        | 交易 ID (唯一)           |
| user_id       | INT NOT NULL           | 購買者 ID (參照 users.user_id) |
| beer_id       | INT NOT NULL           | 購買的酒品 ID (參照 beers.beer_id) |
| timestamp     | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | 購買時間         |
| Foreign Keys  |                        | user_id → users.user_id, beer_id → beers.beer_id |

## 4. payments (付款交易表)

| Column Name   | Data Type              | Description              |
|---------------|------------------------|--------------------------|
| transaction_id| INT PRIMARY KEY        | 付款交易 ID              |
| user_id       | INT NOT NULL           | 付款者 ID (參照 users.user_id) |
| admin_id      | INT NOT NULL           | 管理員 ID (參照 users.user_id) |
| amount        | DECIMAL(10,2) NOT NULL | 付款金額 (負數表示退款)   |
| timestamp     | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | 付款時間         |
| Foreign Keys  |                        | user_id → users.user_id, admin_id → users.user_id |

## 5. vip_customers (VIP 客戶表)

| Column Name   | Data Type              | Description              |
|---------------|------------------------|--------------------------|
| user_id       | INT PRIMARY KEY        | VIP 客戶 ID (參照 users.user_id) |
| credit_limit  | DECIMAL(10,2) NOT NULL | 信用額度 (單位: SEK)     |
| Foreign Keys  |                        | user_id → users.user_id  |

## 6. orders (訂單表)

| Column Name   | Data Type              | Description              |
|---------------|------------------------|--------------------------|
| order_id      | INT PRIMARY KEY AUTO_INCREMENT | 訂單 ID            |
| user_id       | INT NOT NULL           | 下單者 ID (參照 users.user_id) |
| status        | ENUM('pending', 'completed', 'canceled') DEFAULT 'pending' | 訂單狀態 (pending: 未處理, completed: 已完成, canceled: 已取消) |
| created_at    | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | 訂單創建時間      |
| Foreign Keys  |                        | user_id → users.user_id  |

## 7. order_items (訂單明細表)

| Column Name   | Data Type              | Description              |
|---------------|------------------------|--------------------------|
| order_item_id | INT PRIMARY KEY AUTO_INCREMENT | 訂單項目 ID        |
| order_id      | INT NOT NULL           | 訂單 ID (參照 orders.order_id) |
| beer_id       | INT NOT NULL           | 酒品 ID (參照 beers.beer_id) |
| quantity      | INT NOT NULL           | 購買數量                 |
| price         | DECIMAL(10,2) NOT NULL | 單價 (購買當下的價格)    |
| Foreign Keys  |                        | order_id → orders.order_id, beer_id → beers.beer_id |
