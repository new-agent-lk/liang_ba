# liang_ba

## 项目介绍
liang_ba是一个基于Django和Wagtail CMS构建的企业级内容管理系统。它结合了企业信息展示、股票市场数据分析和丰富的内容管理功能，专为需要专业内容管理和金融数据可视化的公司而设计。

## 软件架构
系统采用基于Django框架的现代化分层架构，核心组件包括：
- **前端技术**: HTML/CSS, JavaScript (jQuery, Bootstrap, ECharts)
- **后端框架**: Django 4.2.7 配合 Wagtail 5.2.1 CMS
- **数据库**: MySQL 配合 Redis 缓存
- **API层**: Django REST Framework 提供 RESTful API
- **内容管理**: Wagtail CMS 配置自定义内容页面
- **安全认证**: JWT身份验证和授权

## 功能特点
- **企业信息展示**: 产品中心、新闻动态、工程案例、招聘信息
- **股票市场数据分析**: 实时金融数据可视化和分析
- **动态页面生成**: 由Wagtail CMS驱动，具有内容流功能
- **富文本编辑**: 集成django-ckeditor进行高级内容创作
- **定时任务**: 支持自动日常报告生成的Cron作业
- **响应式设计**: 移动设备友好的界面，使用Bootstrap
- **RESTful API**: 为前端应用程序提供全面的API端点
- **管理面板**: 具有基于角色访问控制的高级管理界面

## 安装教程

### 环境要求
- Python 3.8+
- MySQL 数据库
- Redis 服务器
- Node.js (可选，用于截图工具)

### 安装步骤
1. 克隆仓库:
   ```bash
   git clone https://github.com/your-repo/liang_ba.git
   cd liang_ba
   ```

2. 创建虚拟环境:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows系统: venv\Scripts\activate
   ```

3. 安装Python依赖:
   ```bash
   pip install -r requirements.txt
   ```

4. 配置数据库连接，在[base_settings.py](file:///home/kang/workspace/liang_ba/base_settings.py)中修改（数据库名、用户名、密码）
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'liang_ba',
           'USER': 'your_db_user',
           'PASSWORD': 'your_db_password',
           'HOST': '127.0.0.1',
           'PORT': '3306',
       }
   }
   ```

5. 执行数据库迁移:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. 创建超级用户账户:
   ```bash
   python manage.py createsuperuser
   ```

7. 收集静态文件:
   ```bash
   python manage.py collectstatic
   ```

8. 启动开发服务器:
   ```bash
   python manage.py runserver
   ```

## 使用说明

1. **管理后台**: 访问 `/admin/` 管理用户和内容
2. **Wagtail CMS**: 使用 `/manage/` 的Wagtail界面创建和管理内容页面
3. **API接口**: 通过 `/api/admin/` 访问REST API进行程序化数据操作
4. **公开网站**: 访问主站点 `/` 查看已发布的相关内容

## 主要组件

- **公司信息模块**: 管理公司档案、产品、新闻和招聘
- **Wagtail应用**: 具有动态内容流的自定义内容页面
- **用户管理**: 具有扩展配置文件的自定义用户模型
- **任务调度**: 用于日常内容生成的自动化任务
- **媒体管理**: 配备CKEditor集成的丰富媒体处理

## 参与贡献

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 技术栈

- **后端**: Django 4.2.7, Django REST Framework 3.14.0
- **内容管理**: Wagtail 5.2.1
- **数据库**: MySQL 配合 PyMySQL 连接器
- **缓存**: Redis 配合 django-redis
- **前端**: Bootstrap 5, jQuery, ECharts
- **认证**: JWT 令牌
- **跨域**: CORS 支持
- **定时任务**: django-crontab

## 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件。