# 資料結構核心能力測驗系統 💻

這是一個基於 Django 開發的線上測驗平台，主要針對資料結構中的「雜湊表 (Hash Tables)」單元進行測驗。

## 🌟 系統特色
* **專業題庫**：內建 20 題雜湊表核心觀念題。
* **隨機抽題機制**：每次測驗隨機抽取 15 題，有效防止背題與作弊。
* **現代化 UI 介面**：採用明亮科技風格，具備玻璃質感卡片與即時互動回饋。
* **成績結算與檢討**：測驗結束後自動計算得分，並統整錯題與正確解答。

## 🛠️ 安裝與執行步驟

請依照以下步驟在本地端環境運行本系統：

**1. 複製專案到本地端**
```bash
git clone https://github.com/kevinfang0219/ds_quiz.git
cd ds_quiz
```

**2. 建立並啟動虛擬環境 (Windows)**
```bash
python -m venv myenv
myenv\Scripts\activate
```

**3. 安裝必要套件**
本專案的依賴套件已記錄於 `requirements.txt`，請執行以下指令安裝：
```bash
pip install -r requirements.txt
```

**4. 啟動伺服器**
```bash
python manage.py runserver
```

**5. 開始使用**
打開瀏覽器，前往 `http://127.0.0.1:8000/` 即可開始測驗！
