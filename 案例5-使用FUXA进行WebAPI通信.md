# 使用 FUXA 进行 WebAPI 通信

Postman 是一个支持 http 协议的接口调试和测试工具。其主要特点是功能强大、使用简单、易于使用，常用于 WebAPI 的接口调试。

本文主要介绍如何使用 FUXA 进行 WebAPI 通信。现阶段，FUXA 仅支持 GET 功能，数据包采用 Json 格式。我们将使用 FUXA 的 GET 功能来获取 Postman 的数据报。

## 硬件准备

| reComputer R1000 |
|-----------------|

![reComputer R1000](案例5图片/01.png) |

## WebAPI 通信步骤

### 步骤 1：连接到 WebAPI

点击 FUXA 界面右下角的 + 号，输入 Name，Type 选择 WebAPI，Method 选择 GET，Format 选择 JSON。然后在 URL 处输入 https://postman-echo.com/get，最后点击 OK。您可以看到 FUXA 能够成功与 Postman 建立连接。

![连接WebAPI](案例5图片/connect_webapi.gif)

### 步骤 2：读取 WebAPI 数据

进入设置界面，点击左上角或右下角的 + 按钮，您可以看到通过 GET 功能从 Postman 获取的数据，我们选择每个数据并创建一个标签，最后点击 OK，这样就可以通过 GET 功能实时读取 Postman 数据。

![读取WebAPI数据](案例5图片/display_webapi_get_data.gif)
