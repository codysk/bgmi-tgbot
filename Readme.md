# BGmi-tgbot

![Docker Image CI](https://github.com/codysk/bgmi-tgbot/workflows/Docker%20Image%20CI/badge.svg?branch=master)
![DockerHub](https://images.microbadger.com/badges/version/codysk/bgmi-tgbot.svg)

基于 [aiogram](https://github.com/aiogram/aiogram) 的BGmi Telegram Bot

## 目前实现的功能
+ BGmi 站点的番组出现更新时的QQ通知
+ 管理(增/删)通知发往讨论组/群
+ 其他的还没想好做啥。。(

## 环境要求

+ Docker环境
+ docker-composer (建议，用于编排容器)

## 部署安装

建议使用docker-composer进行容器编排

一个docker-compose.yml的例子
```
version: '3'
services:
  bgmi-tgbot:
    image: codysk/bgmi-tgbot:latest
    environment:
      - api_token=<Telegram Bot TOKEN>
      - admin_user=<Admin UserName>
      - log_level=ERROR
      - bgmi_base_url=<bgmi index api address>
      - error_channel=<@ChannelUserName>
    volumes:
      - ./data:/data

```

有几个环境变量需要在docker-compose配置文件中指定

| 变量名 | 含义 | 必须 | 默认值 |
| ------ | ------ | ------ | ------ |
| api_token | Telegram Bot 的 API TOKEN | * | False |
| admin_user | 管理员Telegram UserName | * | None |
| error_channel | 用于 bot 错误信息输出的 channel (@ChannelUserName) | | None |
| enable_public_command | 公共指令的开放等级(Always总是开放/Subscriber对订阅的群与讨论组开放/Never永不) | | Always |
| log_level | 日志等级(ERROR/WARNING/INFO/DEBUG) |  | ERROR |
| bgmi_base_url | BGmi首页的url |  | http://127.0.0.1 |

做好docker-compose.yml配置文件后
```
docker-compose up -d
```
启动服务 启动时可以通过`docker-compose logs`查看启动日志

## 使用方式

用管理员账号私聊机器人 或在将机器人加入 Channel/Group 均可使用管理指令
### 管理员指令
+ `/set` 将当前 Channel/Group 加入到番组更新的通知列表中
+ `/getlist` 获取当前所有接受通知的 Channel/Group
+ `/remove <channel/group> <id> [<id>...]` 从通知列表中删除 Channel/Group
+ 待更新

### 用户指令
+ `/ping` 返回pong 用来确认机器人程序是否在线
+ `/status` 获取当前订阅的番剧的更新状态
+ 待更新

