# 无线认证管理

当前无线认证提供了一个支持 中国移动 CMCC Portal(v1/v2) 协议， Huawei Portal(v1/v2) 协议的引擎。

支持与华为，华三，中兴，锐捷，汉明等支持以上Portal协议的设备实现对接。

## 无线认证域

系统通过认证域来管理接入点，认证域是一个逻辑意义上的分类。每个认证域下可以管理多个接入点。同时，每个认证域提供一套独立的认证模版。

可以通过定义认证域的配置参数来实现个性化的认证。

## 认证域配置参数

- 域编码：每个域有一个唯一的编码
- 模版名：每个域绑定一个模版
- 模版页面标题：模版的标题
- 热点自动注册资费：提供用户自助注册，比如通过短信，微信自动注册。
- 启用密码认证：是否启用系统用户密码认证。
- 启用短信认证：是否启用短信认证，启用后，认证界面会提供短信验证码认证方式
- 启用微信认证：是否启用微信认证，启用后，认证界面会提供微信自动跳转授权认证。
- 启用QQ认证：是否启用QQ开放认证，启用后，认证界面会提供QQ授权认证。
- 启用免费认证：是否启用一键免密码认证模式。
- 自助服务链接：用户自助门户的地址
- 二维码地址：微信二维码图片地址，保留参数
- 页脚版权声明：模版页脚版权声明，保留参数
- 广告图片地址1，模版页面广告图片链接1
- 广告图片地址2，模版页面广告图片链接2
- 广告图片地址3，模版页面广告图片链接3


## 接入点管理

每个接入点可以对应到一个AP或无线路由器，可以通过一个唯一标识或ssid来标记这个接入点。





