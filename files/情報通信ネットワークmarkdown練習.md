## 前半課題10/21〜10/22
- webサーバを作成
- 作業記録をmarkdown形式で記述
- markdownをhtmlに変換(Save as HTML)
- 作成したWebサーバ上で公開する

## 一日目
### ■ AWSアカウント作成
01.sakamakiのGmailアドレスを使いAWSアカウント作成を行った
以下、注意点↓

- クレカの登録必須
- 電話確認必須
- 各自別のネットワーク接続からアカウント作成
  - 同じネットワークからの複数アクセスはAWSから拒否される可能性がある
- 選択するプランは「ベーシック」プラン

### ■ EC2インスタンス作成
- 起動するイメージ: Amazon Linux
- インスタンスの種類: t2.micro
- キーペア名: 01_saka_mau
  - $HOME/.ssh/配下にキーペアファイルを配置
  - `chmod 600 01_saka_mau.pem`して利用者権限の範囲を狭めておく
- セキュリティグループ設定
  - 使用ポートは22, 80
  - とりあえずmau-mitakaからの接続のみ可能としておく

### ■ サーバへの接続
以下のコマンドでssh接続を行う
```
ssh -i ~/.ssh/01_saka_mau.pem ec2-user@ec2-13-114-100-112.ap-northeast-1.compute.amazonaws.com
```

rootユーザになるためには以下のコマンドを入力する
```
sudo -i
```

### ■ サーバセットアップ
WebサーバはNginxを使用する。  
以下、設定手順を示す

#### ◇ Nginxインストール
```
sudo yum install nginx
```

#### ◇ Nginx 起動
```
sudo service nginx start
```

#### ◇ サーバ起動時にNginxを起動するよう指定
```
sudo chkconfig nginx on
```

#### ◇ Nginx 起動確認
AWSマネージメントコンソール＞EC2＞Instances＞Public DNS (IPv4)に書いてあるドメインをコピペしてアクセスする
例)
```
ec2-13-114-100-112.ap-northeast-1.compute.amazonaws.com
```
<img width="1432" alt="2017-10-21 12 29 40" src="https://user-images.githubusercontent.com/649128/31847713-a9f35af8-b65b-11e7-8509-a4f748b5ece0.png">

以下の画面が表示されればおｋ
<img width="1429" alt="2017-10-21 12 31 35" src="https://user-images.githubusercontent.com/649128/31847721-d184ef50-b65b-11e7-8376-6e3f97b2c1c1.png">


### ■ 作成したMarkdownをWebサーバで公開する
#### ◇ MarkdownのHTML保存
##### [アプリ：AtomでのHTML保存]
1. Shift-Cmd-Mを押し、プレビュー表示させておく
2. プレビュー画面で右クリックし、「Save As HTML...」を選択し、指定場所に保存する
![2017-10-21 14 50 14a](https://user-images.githubusercontent.com/649128/31848511-97e40f60-b66f-11e7-9cfa-b7511400a92a.png)

##### [アプリ：QuiverでのHTML保存]
1. [Quiver](http://happenapps.com/)アプリを起動する
2. 新規ノートを作成し、HTMLで保存したMarkdown文書をペーストする
3. File＞Export Note＞As HTMLで保存する

#### ◇ HTMLファイルをサーバへアップロードする
1. 以下のscpコマンドでファイルをアップロードする
例)
```bash
scp -i ~/.ssh/01_saka_mau.pem ~/Desktop/jnet/index.html ec2-user@ec2-13-114-100-112.ap-northeast-1.compute.amazonaws.com:/home/ec2-user/.
```

2. EC2インスタンスにログインし、ファイルがアップロードされたか確認する
```bash
[ec2-user@ip-172-31-25-115 ~]$ ls
index.html
[ec2-user@ip-172-31-25-115 ~]$
```

#### ◇ HTMLファイルの配置
アップロードしたファイルを以下場所(`/usr/share/nginx/html/配下`)に配置する
```
sudo mv index.html /usr/share/nginx/html/.
```

#### ◇ ブラウザでアップロードしたMarkdownを表示
ブラウザのURLバーに以下のURLを入力する  
例)
```
http://ec2-13-114-100-112.ap-northeast-1.compute.amazonaws.com/
```

<img width="1082" alt="2017-10-21 14 45 44" src="https://user-images.githubusercontent.com/649128/31848463-abd3df10-b66e-11e7-90a6-44efea58ce7c.png">

以下の様に表示される
<img width="1433" alt="2017-10-21 14 45 54" src="https://user-images.githubusercontent.com/649128/31848464-abfc7858-b66e-11e7-89ed-5f8e148c601d.png">

## 二日目

### ■ Ansibleのインストール
Macの場合、以下のコマンドを入力してインストールする。  
その際、[homebrew](https://brew.sh/index_ja.html)がインストールされていること。

```bash
brew update
brew install ansible
```

#### ◇ Ansibleのファイル構成
以下のようにファイルを配置する。  
以降、これらのファイルの設定例を示す。

```
$ tree
.
├── files
│   ├── doc.html
│   └── nginx.conf
├── hosts
└── playbook.yml
```

#### ◇ doc.html
Markdownファイル→HTMLファイルとして保存したもの。

#### ◇ nginx.conf
{url}/j2net/doc.htmlにアクセスした際にdoc.htmlの内容を表示させるために独自に編集したもの。  
既存ファイルとの変更内容は以下。
```diff
[ec2-user@ip-172-31-26-213 nginx]$ diff -u nginx.conf.org nginx.conf
--- nginx.conf.org	2017-10-23 06:27:25.115435257 +0000
+++ nginx.conf	2017-10-22 11:56:15.147794000 +0000
@@ -46,6 +46,10 @@
         # Load configuration files for the default server block.
         include /etc/nginx/default.d/*.conf;

+        location /j2net/doc.html {
+            rewrite ^ /doc.html break;
+        }
+
         location / {
         }
```

#### ◇ hosts
sshの接続情報を記載したファイルである。
```
[mau-saka]
13.114.100.112

[mau-saka:vars]
ansible_ssh_port=22
ansible_ssh_user=ec2-user
ansible_ssh_private_key_file=/Users/sakamaki/.ssh/01_saka_mau.pem
```

#### ◇ playbook.yml
作業内容を指定するためにはplaybookを記述する必要がある。  
実際には以下の処理を行っている。

1. Nginxインストール
2. doc.htmlをサーバの/usr/share/nginx/html/配下に配置
3. nginx.confをサーバの/etc/nginx/配下に配置
4. Nginx起動＆サーバ起動時に自動起動に指定

```yaml
- hosts: mau-saka
  become: yes
  become_user: root
  tasks:
    - name: Install nginx
      yum: name=nginx state=latest
      tags:
        - install

    - name: Upload file that doc.html to server
      copy: src=doc.html dest=/usr/share/nginx/html/
      tags:
        - upload_html

    - name: Upload file that nginx.conf to server
      copy: src=nginx.conf dest=/etc/nginx/
      tags:
        - upload_nginx_conf

    - name: Startup Nginx
      service: name=nginx state=started enabled=yes
      tags:
        - startup
```

#### ◇ playbookの実行
hostsファイルとplaybook.ymlファイルと同じ位置で以下のコマンドを実行すると、ブラウザにmarkdownの内容が表示されるまで一気にやってくれる。

```
ansible-playbook -i hosts playbook.yml
```

#### ◇ playbookの実行補足
ansibleはタグ指定することでそのタグに割当てられたタスクが実行できる。  
具体的には以下のように行う。

```
ansible-playbook -i hosts playbook.yml --tags "install"
```

### ■ Amazon Linuxの仮想マシンをMac上にインストール
知らないうちにAmazon LinuxはOSのイメージが提供されるようになったそうだ。  
今回は[vagrant](https://ja.wikipedia.org/wiki/Vagrant_(%E3%82%BD%E3%83%95%E3%83%88%E3%82%A6%E3%82%A7%E3%82%A2)を使ってMacの仮想マシン上（VirtualBox）にAmazon Linuxのインストールを行う。

Macの場合、以下のコマンドを入力してvagrantインストールする。
```
brew install vagrant
```

以下のコマンドでMacの仮想マシン上(VirtualBox)にAmazon Linuxを起動するために必要なVagrantfileが作成される。
```
mkdir alinux && cd alinux
vagrant init mvbcoding/awslinux
```

そのままだと、IPを指定してsshログインできないので、上記の先程のコマンドで作成されたVagrantfileを編集し、以下のように修正する。
```diff
$ diff -u Vagrantfile.org Vagrantfile
--- Vagrantfile.org	2017-10-22 14:52:56.000000000 +0900
+++ Vagrantfile	2017-10-22 14:53:05.000000000 +0900
@@ -26,7 +26,7 @@

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
-  # config.vm.network "private_network", ip: "192.168.33.10"
+  config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
```

以下のコマンドを入力し、Amazon Linuxを起動する。
```
vagrant up
```

起動後、以下のコマンドを入力し、sshするための情報を取得する。
```
vagrant ssh-config
```

すると以下の情報が返され、IdentityFileの場所がわかる。
`/Users/{username}/tmp/alinux/.vagrant/machines/default/virtualbox/private_key` というファイルがsshの秘密鍵でこれを使ってssh接続する
```
$ vagrant ssh-config
Host default
 HostName 127.0.0.1
 User vagrant
 Port 2222
 UserKnownHostsFile /dev/null
 StrictHostKeyChecking no
 PasswordAuthentication no
 IdentityFile /Users/{username}/tmp/alinux/.vagrant/machines/default/virtualbox/private_key
 IdentitiesOnly yes
 LogLevel FATAL
```

#### ◇ hosts
既存のhostsファイルに追記し、sshアクセスするための情報を記載する。
```
[vagrant]
192.168.33.10

[vagrant:vars]
ansible_ssh_port=22
ansible_ssh_user=vagrant
ansible_ssh_private_key_file=/Users/sakamaki/tmp/alinux/.vagrant/machines/default/virtualbox/private_key
```

#### ◇ playbook_local.yml
以下のplaybook: playbook_local.ymlを作成する。  
設定内容は以下。

```yaml
- hosts: vagrant
  become: yes
  become_user: root
  tasks:
    - name: Install nginx
      yum: name=nginx state=latest
      tags:
        - install

    - name: Upload file that doc.html to server
      copy: src=doc.html dest=/usr/share/nginx/html/
      tags:
        - upload_file

    - name: Upload file that nginx.conf to server
      copy: src=nginx.conf dest=/etc/nginx/
      tags:
        - upload_file

    - name: Startup Nginx
      service: name=nginx state=started enabled=yes
      tags:
        - startup
```

以下のようにplaybook_local.ymlが配置されていること。
```
$ tree
.
├── files
│   ├── doc.html
│   └── nginx.conf
├── hosts
├── playbook.yml
└── playbook_local.yml
```

playbookを実行する。
```
ansible-playbook -i hosts playbook_local.yml
```

#### ◇ 参考
- [Ansible で Mac を構成管理するときの勘所](https://qiita.com/kkitta/items/27f8aca89e55b719cb6f)
- [暗号解読〈上〉 (新潮文庫) ](https://www.amazon.co.jp/%E6%9A%97%E5%8F%B7%E8%A7%A3%E8%AA%AD%E3%80%88%E4%B8%8A%E3%80%89-%E6%96%B0%E6%BD%AE%E6%96%87%E5%BA%AB-%E3%82%B5%E3%82%A4%E3%83%A2%E3%83%B3-%E3%82%B7%E3%83%B3/dp/410215972X)


##  Tips
以下のファイルを監視すると外部からのアクセス形跡を確認できる。

```
tail -f /var/log/secure
```

## 中間提出
このMarkdownをHTML化して、サーバーにホストしたものをFacebookグループに報告する。  
その際、{url}/j2net/doc.hmtlの形でホストすること。

## 三日目
Webサイトのスクレイピングを行い、D3.jsを使って映像表現するところまで進めたい。
まずは、以下の[課題](http://yamakk.com/musabi/network2017/)を終わらせる
```
2017 Yearly Box Office Results - Box Office Mojo
http://www.boxofficemojo.com/yearly/chart/?yr=2017&p=.htm
から2017年の興行収入ランキングをプログラムで1位から100位まで取得し、tsvファイル(タブで区切られたファイル)に書き出す。
```

### Ansibleセットアップ
#### 前提
- OSはAmazon Linuxを使用する
- WebアプリケーションフレームワークはDjango ver1.11.6を使用
- アプリケーションサーバはgunicornを使用する

#### 実行内容
- クローラ:boxoffice.py作成

## 四日目
以下の残タスクを片付ける

- はてなブックマークのホットエントリーをスクレイピングするためのクローラの作成
- D3.jsを使って情報を可視化する。
- Ansibleのplaybookに設定をまとめる

### はてなブックマークのホットエントリーをスクレイピングするためのクローラの作成
### D3.jsを使って情報を可視化する。
### Ansibleのplaybookに設定をまとめる
