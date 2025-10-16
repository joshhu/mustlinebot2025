FROM python:3.11-slim

WORKDIR /app

# 複製 requirements 並安裝所有套件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製所有程式碼檔案
COPY . .

# 開放 Flask port
EXPOSE 5000

# 執行主程式，假設是 app.py
CMD ["python", "app.py"]
