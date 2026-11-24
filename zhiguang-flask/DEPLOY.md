# 织光平台 - Flask 动态网站部署指南

## 部署包说明

这个部署包包含完整的 Flask 动态网站：
- ✅ 用户注册/登录/登出
- ✅ 四维思维测评（40 题）
- ✅ 雷达图可视化
- ✅ 思维训练模块（8 个）
- ✅ 成长报告
- ✅ 后台管理

## 推荐部署平台：Render

Render 是部署 Flask 应用最简单的平台，有免费层。

### 步骤 1：注册 Render

1. 访问 https://render.com
2. 点击 "Get Started for Free"
3. 选择 "Sign up with GitHub"（推荐）或邮箱注册

### 步骤 2：创建 GitHub 仓库

```bash
# 解压部署包
tar -xzf zhiguang-flask.tar.gz
cd zhiguang-flask

# 初始化 Git
git init
git add .
git commit -m "Initial commit: 织光平台"

# 创建 GitHub 仓库并推送
git remote add origin https://github.com/你的用户名/zhiguang-flask.git
git branch -M main
git push -u origin main
```

### 步骤 3：在 Render 部署

1. 登录 https://render.com
2. 点击 "New +" → "Web Service"
3. 点击 "Connect a repository"
4. 选择你的 `zhiguang-flask` 仓库
5. 配置应用：
   - **Name**: `zhiguang-platform`
   - **Region**: `Oregon` (美国) 或 `Frankfurt` (欧洲)
   - **Branch**: `main`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
6. 点击 "Create Web Service"
7. 等待部署完成（约 2-3 分钟）

### 步骤 4：获得永久地址

部署完成后，Render 会给你一个地址：
```
https://zhiguang-platform.onrender.com
```

这个地址是**永久有效**的！

### 步骤 5：访问应用

1. 打开 https://zhiguang-platform.onrender.com
2. 使用管理员账户登录：
   - 用户名: `admin`
   - 密码: `admin123`

---

## 其他部署平台

### Railway (https://railway.app)

1. 登录 Railway
2. 点击 "New Project" → "Deploy from GitHub repo"
3. 选择 `zhiguang-flask` 仓库
4. Railway 自动检测 Python 应用
5. 点击 "Deploy"
6. 获得地址：`https://zhiguang-flask.up.railway.app`

### PythonAnywhere (https://pythonanywhere.com)

1. 注册账号（有免费层）
2. 创建 Web App
3. 选择 "Flask" 框架
4. 上传代码文件
5. 配置 WSGI 文件指向 `app.py`
6. 获得地址：`https://你的用户名.pythonanywhere.com`

---

## 本地运行

```bash
# 解压部署包
tar -xzf zhiguang-flask.tar.gz
cd zhiguang-flask

# 安装依赖
pip install -r requirements.txt

# 运行应用
python app.py

# 访问 http://localhost:5000
```

---

## 部署包文件说明

```
zhiguang-flask/
├── app.py              # Flask 主应用
├── config.py           # 配置文件
├── extensions.py       # 数据库扩展
├── models.py           # 数据模型
├── seed.py             # 种子数据
├── utils.py            # 工具函数
├── requirements.txt    # Python 依赖
├── Procfile            # 启动命令（Render 用）
├── render.yaml         # Render 配置
├── routes/             # 路由模块
│   ├── __init__.py
│   ├── admin.py        # 后台管理
│   ├── assessment.py   # 测评模块
│   ├── auth.py         # 认证模块
│   ├── dashboard.py    # 仪表盘
│   └── report.py       # 报告模块
├── templates/          # HTML 模板
├── static/             # 静态资源
└── instance/           # 数据库目录
```

---

## 常见问题

### Q: 部署后访问很慢？
A: Render 免费层有休眠机制，首次访问需要等待 30 秒左右。

### Q: 数据库数据会丢失吗？
A: Render 免费层的文件系统是临时的，重启后数据会丢失。建议使用外部数据库（如 PostgreSQL）。

### Q: 如何绑定自定义域名？
A: Render 支持自定义域名，在应用设置中添加即可。

### Q: 如何查看日志？
A: 在 Render 应用页面点击 "Logs" 标签查看实时日志。

---

## 管理员账户

- 用户名: `admin`
- 密码: `admin123`

---

## 技术支持

如有问题，请查看：
- Render 文档：https://render.com/docs
- Flask 文档：https://flask.palletsprojects.com/
