
# 📊 VPS 交易价值计算器 (VPS Value Calculator)

一个极简、现代化的 VPS 剩余价值计算器，专为 VPS 交易设计。
基于 Python Flask + Vue.js 构建，支持 Docker 一键部署。

## ✨ 特性

- **到期日驱动**：输入到期日期，自动计算剩余天数。
- **实时汇率**：自动获取最新汇率，支持手动修正。
- **多种模式**：支持「精确剩余价值」和「折扣/溢价」计算。
- **精美报表**：一键生成 Markdown 交易帖内容，支持生成高清分享图片。
- **完全响应式**：手机、电脑完美适配。

## 🚀 快速部署 (Docker Compose)

Docker Run

docker run -d \
  --name vps_calculator \
  --restart always \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  nimeng1222/vps-calculator:latest


只需创建一个 `docker-compose.yml` 文件：

```yaml
version: '3.8'
services:
  vps-calc:
    image: nimeng1222/vps-calc:latest
    container_name: vps_calculator
    restart: always
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
