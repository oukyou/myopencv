#### virtualenvをインストール
```
    pip install virtualenv
```

#### 開発用のvirtualenvを用意
```
    virtualenv E:\env
    E:> \E:\env\Scripts\activate
    (env) E:\env>
```

#### djangoモジュールをインストール
```
    # モジュールをインストール
    (env) E:\env>pip install Django==1.11.1

    # Pythonパッケージの一覧
    (env) E:\env>pip freeze -l

    # プロジェクトを新規に作る
    (env) E:\env>python E:\env\Lib\site-packages\django\bin\django-admin.py startproject OpenCV

    # WEBを立ち上げる
    (env) E:\env\OpenCV>python manage.py runserver 192.168.0.1:8000
```

#### モジュールインストール
+ MySQL
```
    (env) E:\env\OpenCV>pip install pymysql
    (env) E:\env\OpenCV>pip install mysqlclient
```

+ Image Upload
```
    (env) E:\env\OpenCV>pip install Pillow
```

#### 新しいAPPを新規する
```
    # APPソース
    (env) E:\env\OpenCV>python manage.py startapp appname

    # マイグレートファイル
    (env) E:\env\OpenCV>python manage.py makemigrations appname

    # SQLプレビュー
    (env) E:\env\OpenCV>python manage.py sqlmigrate appname 0001

    # データベースに反映する
    (env) E:\env\OpenCV>python manage.py migrate
```

#### start web service
```
    python manage.py runserver 192.168.0.1:8000
```


#### rest apiに必要なライブラリ
```
    pip install django
    pip install djangorestframework
    pip install django-filter
```

#### opencvインストール
```
    pip install libs\opencv_python-3.2.0-cp36-cp36m-win_amd64.whl
```

#### numpy インストール
pip install numpy

pip install Django==1.11.1
pip install django-fontawesome
pip install django-bootstrap-form
pip install djangorestframework
pip install django-filter
pip install pymysql
pip install mysqlclient
pip install numpy



```
ALTER TABLE `api_transaction` ADD COLUMN `type` varchar(1) DEFAULT "0";
ALTER TABLE `api_transaction` ALTER COLUMN `type` SET DEFAULT "0";
```



#### pyenv: 複数バージョンのPythonを~/.pyenv以下に配置,これを切り替えて手軽にバージョンを変更




#### python install
$ curl -O https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tgz
$ tar zxf Python-3.6.1.tgz
$ cd Python-3.6.1
$ ./configure --enable-shared --prefix=/usr/local
$ make & make install
> http://www.yoheim.net/blog.php?q=20170206
  http://modwsgi.readthedocs.io/en/develop/user-guides/installation-issues.html#multiple-python-versions


#### modwsgi install
./configure --with-python=/usr/local/bin/python3.6







##### .gitigonore にファイル名を追加

1.  .gitigonore にファイル名を追加
```
    $ vi .gitignore
```
2. キャッシュ削除

```
$ git rm --cached /path/to/file.txt
# 例えば：git rm --cached *cpython-36.pyc
```

3. まとめて commit & push
```
$ git add .gitignore
$ git commit -m "add file to .gitignore"
$ git push origin master
```




##### Windows, apache2.4, mod_wsgi環境構築

1. mod_wsgiをダウンロードする
http://www.lfd.uci.edu/~gohlke/pythonlibs/#mod_wsgi
```
pip install mod_wsgi-4.4.23+ap24vc14-cp35-cp35m-win_amd64.wh
```
Apacheのmod_wsgiモジュールパスは ** "{python_path}\site-packages\mod_wsgi\server\mod_wsgi.cp36-win_amd64.pyd" **

2. Apache conf
```
#-------------------------------------------------
# Django Settings
#-------------------------------------------------
LoadModule wsgi_module "E:\env\Lib\site-packages\mod_wsgi\server\mod_wsgi.cp36-win_amd64.pyd"

WSGIScriptAlias /opencv "E:\source\python\myopencv6\myopencv\wsgi.py"
WSGIPythonHome "E:\env"
WSGIPythonPath "E:\source\python\myopencv6"

<Directory "E:\source\python\myopencv6\myopencv">
	<Files wsgi.py>
		Require all granted
	</Files>
</Directory>

Alias /data/   "E:\source\python\myopencv6\data"
Alias /static/ "E:\source\python\myopencv6\static"

<Directory "E:\source\python\myopencv6\static">
Require all granted
</Directory>

<Directory "E:\source\python\myopencv6\data">
Require all granted
</Directory>
```




### css/jsファイルのディプロイ
# python manage.py collectstatic

```
WSGIScriptAlias /opencv "E:\source\python\myopencv6\myopencv\wsgi.py"
WSGIPythonHome "E:\env"
WSGIPythonPath "E:\source\python\myopencv6"

<VirtualHost *:80>
	ServerName www.example.com

	<Directory "E:\source\python\myopencv6\myopencv">
		Require all granted
	</Directory>

	Alias /opencv/static "E:\source\python\myopencv6\static"
	<Directory "E:\source\python\myopencv6\static">
		Require all granted
	</Directory>

	Alias /opencv/images "E:\source\python\myopencv6\data"
	<Directory "E:\source\python\myopencv6\data">
		Require all granted
	</Directory>

</VirtualHost>
```

