FROM python:3.10-slim

# 工作目录
WORKDIR /app

# 安装依赖
RUN pip install --no-cache-dir numpy matplotlib

# 复制源码
COPY . .

# 运行demo
CMD ["python", "demo.py"]
