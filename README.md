# 狡兔三窟
使用aws s3接口和cf的dns管理接口实现AWS实例IP自动分配，并更新CF的DNS记录，设置定时任务就可以不怕GFW啦。

## 使用说明

```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
RUN_BAT.bat
```

## 如何配置
所有配置都在setting.py文件中，另外boto3的配置可以使用~/.aws/credentials文件的形式来处理


## 计划任务

```cmd
schtasks /create /tn "VPN_DNS_IP_CHANGE" /tr "/c start "" /b {{{{{{\ABS_PATH\RUN_BAT.bat}}}}}} <NUL" /sc hourly /mo 2 /st 00:00
```