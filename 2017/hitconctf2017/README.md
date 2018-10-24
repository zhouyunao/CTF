# HITCON CTF 2017
## secret server

## 特徴&解き方
* AES-CBC
* proof-of-workあり
* 暗号化の際のIVは既知
* 復号の際のIVは任意に送れる
* unpad は脆弱（長さ判定、paddingの中身判定ともに無し）
* padding oracle
* http://kyuri.hatenablog.jp/entry/2017/11/08/161403