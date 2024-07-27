# driver_app_api

## 專案架構

> 所有的 .py 檔應建立在 app 資料夾底下

```bash
.
├── app
│   ├── config # 專案設定檔, 基本會有logging設定及database連線設定
│   ├── logic # 專案邏輯
│   │   ├── core # 底層核心
│   │   └── utilities # 共用模組或有循環參考的func
│   ├── model # sqlalchemy models
│   ├── router # API endpoint
│   ├── schema # pydantic schema
│   └── __init__.py # Global Module
├── .flake8
├── .gitignore
.
.
.
└── startup.sh
```

## 專案啟動步驟

1. 依照`env_sample`檔案配置`.env`
   ```bash
   # MySQL
   DB_CONN=
   ...
   ```
2. 建立並進入虛擬環境
   ```bash
   python -m venv venv
   source venv/bin/activate # Mac & Linux
   或 venv\Scripts\activate.bat # Windows
   ```
3. 安裝開發套件
   ```bash
   pip install -r requirements.txt
   ```
4. 運行開發伺服器
   ```bash
   # fastapi 0.111.0版可以用FastAPI CLI
   fastapi dev main.py
   或
   # fastapi 0.111.0以前的版本用uvicorn啟動，兩者是等價的
   uvicorn main:app --reload
   ```
5. (option)運行生產伺服器
   ```bash
   # fastapi 0.111.0版可以用FastAPI CLI
   fastapi run main.py
   或
   # fastapi 0.111.0以前的版本用uvicorn啟動，兩者是等價的
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## Coding Style 檢核

PEP8, 變數型態, 安全性等 靜態源碼掃描套件獨立在`requirements-dev.txt`, 可以另外安裝後在本地運行

> 在 Bitbucket 上透過 Pipelines 也會進行相同的項目檢核

### 安裝套件

```bash
pip install -r requirements-dev.txt
```

### Black 代碼格式化

```bash
python -m black .
```

### Flake8 代碼風格檢查

```bash
# 根據 .flake8 設定條件
flake8 ./app
```

### Mypy 型態檢查

```bash
# 根據 mypy.ini 設定條件
mypy --install-types --non-interactive ./app
```

### Bandit 安全性檢查

```bash
bandit -r ./app -iii -lll
```

## API Response 規範

API 回傳結果, 請固定以 `schema/base_api_response.py` 為主, 接收端可以很明顯知道每次所回傳的資料結構,
主要內容如下:

```json
{
  "success": false, // 是否成功
  "message": "", // 回傳訊息
  "data": [], // 回傳資料(option)
  "total": 1, // 總計
  "error_code": "400" // 錯誤代碼(option)
}
```
