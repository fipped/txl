# by 通讯录

### 概述

用 Django 框架实现的简易通讯录

- [x] 前端
- [x] 用户系统
    - [x] 登录
    - [x] 注册
    - [ ] 修改密码
    - [ ] 找回密码
    - [ ] 记住密码  
- [x] 通讯录功能
    - [x] 添加
    - [x] 删除
    - [x] 修改
    - [ ] 翻页
    - [ ] 导入  
    - [ ] 导出

### 部署

```shell
# 数据库迁移(如果是 python2.x 就去掉3)
python3 manage.py makemigrations
python3 manage.py migrate 

# 运行服务器
python3 manage.py runserver

# 访问 http://localhost:8000/
```

### 生产环境

若在 `txl/txl/setting.py` 中将 `DEBUG` 设置为 `True`, 需要:

配置 Nginx 或 Apache :

```conf
# 这个 static 目录是之后收集静态文件用的
<Directory "~/PyCharmProjects/txl/static">
Require all granted
</Directory>
```

在 `txl/txl/setting.py` 中加上:

```python
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
```

执行:
```shell
# 将静态文件收集到 STATIC_ROOT
python3 manage.py collectstatic 
```

然后再部署.