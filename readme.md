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


