# 使用 Python 官方基底映像檔
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 複製本地檔案到 container 中
COPY app.py .

# 安裝 flask
RUN pip install flask

# 暴露 Flask 使用的預設 port
EXPOSE 5000

# 啟動 Flask 應用
CMD ["python", "app.py"]
