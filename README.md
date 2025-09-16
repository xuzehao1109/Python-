# Django 登录演示

这是一个基于 Django 的登录示例，集成了谷歌验证器 (TOTP) 的二次验证流程。界面保持简约风格并使用柔和的渐变色，适合企业后台或内部系统作为模板使用。

## 功能亮点

- 使用 Django 认证体系完成用户名 / 密码校验。
- 自研 TOTP 工具与 Google Authenticator 兼容，可在离线环境下使用。
- 登录表单额外要求输入谷歌动态验证码，未通过校验时会阻止登录。
- 登录成功后的控制台页面提供当前密钥并可跳转到安全设置页。
- 安全设置页面展示绑定说明及二维码（通过公共 API 生成，可替换为自建服务）。
- 提供 `create_demo_user` 管理命令快速创建带密钥的演示账号。

## 快速开始

1. **安装依赖**

   ```bash
   pip install django
   ```

   > 如果处于离线环境，请预先准备好 Django 的离线安装包并使用 `pip install --no-index --find-links <dir> django` 安装。

2. **准备数据库并创建迁移表**

   ```bash
   python manage.py migrate
   ```

3. **创建演示账号（可选）**

   ```bash
   python manage.py create_demo_user
   ```

   终端会输出账号、初始密码以及 Google Authenticator 密钥/URI，将其录入手机应用后即可获取动态验证码。

4. **启动开发服务器**

   ```bash
   python manage.py runserver
   ```

   打开浏览器访问 `http://127.0.0.1:8000/accounts/login/`，使用步骤 3 中的账号密码和动态验证码完成登录。

## 项目结构

```
authsite/                # Django 项目目录
├── manage.py
└── authsite/
    ├── settings.py
    ├── urls.py
    ├── asgi.py
    └── wsgi.py
accounts/                # 登录应用与二次验证逻辑
├── templates/accounts   # 登录、控制台、安全设置页面
├── static/accounts      # 页面样式
├── totp.py              # TOTP 生成与校验工具
├── forms.py             # 自定义带 TOTP 的登录表单
├── views.py             # 视图逻辑
└── management/commands  # create_demo_user 演示命令
```

## 设计说明

- 页面采用玻璃质感卡片和渐变背景，突出登录框并兼顾色彩层次。
- 表单控件使用较大的圆角和阴影，提升现代感与可用性。
- TOTP 校验允许一个时间窗口的偏差，减少用户因网络延迟导致的登录失败。
- 如需生成离线二维码，可将安全设置页面中的二维码链接替换为自建二维码服务或直接渲染 SVG。

## 测试

项目内包含基础的单元测试 (`accounts/tests.py`) 用于验证 TOTP 工具。运行方式：

```bash
python manage.py test accounts
```

> 在尚未安装 Django 或缺少依赖的情况下运行命令会失败，请先完成依赖安装。
