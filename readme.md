友善信息库后台。

The backend of 'friendly information database' (uncovermap.com).

部署前需要做的：在 `secret_key.txt` 放置密钥。

What to do before deployment: put your secret key in `secret_key.txt`.

代码质量非常糟糕，欢迎提建议。

The code quality is pretty poor. Suggestions welcomed.

###　部署方式 How to deploy

先迁移：

First make the migrations:

```
python3 manage.py makemigrations
python3 manage.py migrate
```

然后打开 django shell：

Then open the django shell: 

```
python3 manage.py shell
```

然后在 shell 中设置管理员帐号密码：

Then set the admin username and password in shell:

```
>>> from django.contrib.auth.models import User
>>> user = User.objects.create_user('USERNAME', 'MAIL_NO_REQUIRED', 'PASSWORD')
```
