# 🔌 FUXA WebSocket 通信教程

---

## 📋 概述

WebSocket 是一种在单个 TCP 连接上进行全双工通信的协议，它提供了一种简单高效的方式与 Node-RED 等 Web 应用程序进行通信。FUXA 支持直接在脚本中使用 WebSocket 实现双向数据传输。

---

## 🎯 应用场景

- **实时数据交换**：与 Node-RED、自定义 Web 应用程序交换实时数据
- **跨平台集成**：连接不同平台和系统
- **事件驱动**：基于事件的数据推送和接收
- **远程控制**：通过 WebSocket 实现远程设备控制

---

## 🔧 WebSocket 模式

### 客户端模式（推荐）

FUXA 作为 WebSocket 客户端连接到外部 WebSocket 服务器。

**优势**：
- 简单易用
- 适合与现有服务器集成
- 支持自动重连

**适用场景**：
- 连接到 Node-RED WebSocket 服务器
- 连接到自定义 WebSocket 服务
- 与第三方系统集成

---

### 服务器模式

FUXA 作为 WebSocket 服务器，外部客户端连接到 FUXA。

**优势**：
- 完全控制连接
- 适合作为数据源

**适用场景**：
- FUXA 作为数据源
- 多个客户端连接到 FUXA

---

## 💻 完整示例代码

### 双向数据传输示例

以下是一个完整的双向数据传输示例，我们将所有 FUXA 标签和值封装到一个包含时间戳和有效载荷的 JSON 数据对象中。

**重要提示**：
- 此脚本必须是**服务器端脚本**
- 设置为**启动时运行**
- 需要有一个**正在运行的 WebSocket 服务器**（以下代码用于 WebSocket 客户端）

```javascript
// 引入 WebSocket 模块
const WebSocket = require('/usr/src/app/FUXA/server/node_modules/ws');

// 全局声明 WebSocket 以管理连接
let ws;

// WebSocket 服务器 URL
const WebSocketUrl = 'ws://127.0.0.1:1880';

// PLC/FUXA 标签列表
const tagNames = [
    'yourTagName1', 
    'yourTagName2', 
    'yourTagName3', 
    'yourTagName4', 
    'yourTagName5'
];

// 获取标签值并创建 JSON 有效载荷的函数
async function createPayload() {
    let payload = {};

    // 遍历所有标签并获取当前值
    for (const tagName of tagNames) {
        let tag = await $getTag($getTagId(tagName));
        payload[tagName] = tag;
    }

    // 返回包含时间戳和有效载荷的数据对象
    return {
        data: {
            timestamp: new Date().toISOString(),
            payload: payload
        }
    };
}

// 向 WebSocket 服务器发送数据的函数
function sendData() {
    createPayload().then((payload) => {
        // 检查连接状态
        if (ws && ws.readyState === WebSocket.OPEN) {
            // 发送 JSON 数据
            ws.send(JSON.stringify(payload));
        } else {
            console.log('WebSocket 未打开。跳过发送数据。');
        }
    });
}

// 打开 WebSocket 连接
function openWebSocketConnection() {
    // 创建 WebSocket 客户端连接
    ws = new WebSocket(WebSocketUrl);

    // 连接打开事件
    ws.on('open', () => {
        console.log('WebSocket 连接已建立');
    });

    // 接收消息事件
    ws.on('message', (message) => {
        try {
            // 解析接收到的 JSON 消息
            let receivedData = JSON.parse(message);
            
            // 检查数据结构
            if (receivedData.data && receivedData.data.payload) {
                // 遍历接收到的标签值
                for (const tagName in receivedData.data.payload) {
                    // 只更新已定义的标签
                    if (tagNames.includes(tagName)) {
                        $setTag($getTagId(tagName), receivedData.data.payload[tagName]);
                    }
                }
            }
        } catch (error) {
            console.error('解析 WebSocket 服务器消息时出错:', error);
        }
    });

    // 错误处理事件
    ws.on('error', (error) => {
        console.error('WebSocket 错误:', error);
    });

    // 连接关闭事件
    ws.on('close', () => {
        console.log('WebSocket 连接已关闭');
        // 如果连接关闭，尝试延迟重新连接
        setTimeout(openWebSocketConnection, 5000); 
    });
}

// 启动 WebSocket 连接
openWebSocketConnection();

// 设置定时器，每 500ms 发送一次数据
if (typeof globalThis.myTimer === 'undefined') globalThis.myTimer = null;

if (!globalThis.myTimer) globalThis.myTimer = setInterval(myTimerFunction, 500);

async function myTimerFunction() {
    sendData();
}
```

---

## 📊 数据格式说明

### 发送数据格式

```json
{
  "data": {
    "timestamp": "2026-01-06T12:00:00.000Z",
    "payload": {
      "yourTagName1": 25.3,
      "yourTagName2": true,
      "yourTagName3": "Hello",
      "yourTagName4": 100,
      "yourTagName5": 0.5
    }
  }
}
```

### 接收数据格式

```json
{
  "data": {
    "timestamp": "2026-01-06T12:00:00.500Z",
    "payload": {
      "yourTagName1": 30.5,
      "yourTagName2": false,
      "yourTagName3": "World",
      "yourTagName4": 200,
      "yourTagName5": 0.8
    }
  }
}
```

---

## 🔌 与 Node-RED 集成

### Node-RED 端配置

在 Node-RED 中创建 WebSocket 服务器节点：

```javascript
// Node-RED 流程示例
[
    {
        "id": "websocket-in",
        "type": "websocket in",
        "name": "FUXA Input",
        "server": "server-config",
        "clientType": "server",
        "x": 150,
        "y": 100,
        "wires": [
            [
                "process-data"
            ]
        ]
    },
    {
        "id": "process-data",
        "type": "function",
        "name": "Process Data",
        "func": "msg.payload = msg.data.payload;\nreturn msg;",
        "outputs": 1,
        "x": 350,
        "y": 100,
        "wires": [
            [
                "websocket-out"
            ]
        ]
    },
    {
        "id": "websocket-out",
        "type": "websocket out",
        "name": "FUXA Output",
        "server": "server-config",
        "clientType": "server",
        "x": 550,
        "y": 100,
        "wires": []
    },
    {
        "id": "server-config",
        "type": "websocket-listener",
        "path": "/ws",
        "wholemsg": "false"
    }
]
```

---

## 💡 高级用法

### 1️⃣ 连接状态监控

```javascript
// 添加连接状态监控
function monitorConnection() {
    setInterval(() => {
        if (ws && ws.readyState === WebSocket.OPEN) {
            console.log('WebSocket 连接正常');
        } else {
            console.log('WebSocket 连接异常');
        }
    }, 10000);
}

monitorConnection();
```

### 2️⃣ 心跳机制

```javascript
// 添加心跳机制
function startHeartbeat() {
    setInterval(() => {
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ type: 'heartbeat', timestamp: new Date().toISOString() }));
        }
    }, 30000); // 每 30 秒发送一次心跳
}

startHeartbeat();
```

### 3️⃣ 数据压缩

```javascript
// 对于大量数据，可以使用压缩
const zlib = require('zlib');

function sendCompressedData(data) {
    if (ws && ws.readyState === WebSocket.OPEN) {
        const json = JSON.stringify(data);
        const compressed = zlib.gzipSync(json);
        ws.send(compressed, { binary: true });
    }
}
```

### 4️⃣ 错误重试机制

```javascript
// 增强的重试机制
let retryCount = 0;
const maxRetries = 5;

function openWebSocketConnection() {
    ws = new WebSocket(WebSocketUrl);

    ws.on('open', () => {
        console.log('WebSocket 连接已建立');
        retryCount = 0; // 重置重试计数
    });

    ws.on('close', () => {
        console.log('WebSocket 连接已关闭');
        
        if (retryCount < maxRetries) {
            retryCount++;
            const delay = Math.min(1000 * Math.pow(2, retryCount), 30000);
            console.log(`尝试重新连接 (${retryCount}/${maxRetries})，延迟 ${delay}ms`);
            setTimeout(openWebSocketConnection, delay);
        } else {
            console.error('达到最大重试次数，停止重试');
        }
    });
}
```

---

## 🔧 故障排除

### 常见问题

#### ❓ 连接失败

**可能原因**：
- WebSocket 服务器未运行
- URL 配置错误
- 防火墙阻止连接
- 端口被占用

**解决方案**：
1. 确认 WebSocket 服务器正在运行
2. 检查 WebSocket URL 是否正确
3. 检查防火墙设置
4. 确认端口未被其他程序占用

---

#### ❓ 数据未发送

**可能原因**：
- 连接未建立
- 标签 ID 错误
- 数据格式错误

**解决方案**：
1. 检查连接状态
2. 验证标签 ID 是否正确
3. 检查 JSON 数据格式

---

#### ❓ 数据未接收

**可能原因**：
- 消息格式不匹配
- 标签名称不匹配
- 解析错误

**解决方案**：
1. 检查消息格式是否符合预期
2. 验证标签名称是否在 tagNames 列表中
3. 查看错误日志

---

#### ❓ 频繁断开连接

**可能原因**：
- 网络不稳定
- 服务器超时
- 心跳机制缺失

**解决方案**：
1. 添加心跳机制
2. 增加重连延迟
3. 检查网络稳定性

---

## 📚 最佳实践

### 1️⃣ 错误处理

始终添加完整的错误处理：

```javascript
try {
    // WebSocket 操作
} catch (error) {
    console.error('WebSocket 操作失败:', error);
    // 执行恢复操作
}
```

### 2️⃣ 连接管理

使用全局变量管理连接状态：

```javascript
let ws = null;
let isConnected = false;

function updateConnectionStatus(status) {
    isConnected = status;
    $setTag($getTagId('wsConnected'), status);
}
```

### 3️⃣ 数据验证

验证接收到的数据：

```javascript
function validateData(data) {
    if (!data || !data.data || !data.data.payload) {
        console.error('无效的数据格式');
        return false;
    }
    return true;
}
```

### 4️⃣ 性能优化

避免过于频繁的数据发送：

```javascript
// 使用节流函数
let lastSendTime = 0;
const minSendInterval = 100; // 最小发送间隔 100ms

function throttledSend() {
    const now = Date.now();
    if (now - lastSendTime >= minSendInterval) {
        sendData();
        lastSendTime = now;
    }
}
```

---

## 🎉 总结

通过本教程，您已经学会了：

✅ WebSocket 的基本概念  
✅ 创建 WebSocket 客户端连接  
✅ 实现双向数据传输  
✅ 与 Node-RED 集成  
✅ 高级用法和技巧  
✅ 故障排除  
✅ 最佳实践  

现在您可以在 FUXA 中使用 WebSocket 实现实时通信了！

---

## 📚 快速参考

### WebSocket 连接状态

| 状态 | 值 | 说明 |
|------|------|------|
| **CONNECTING** | 0 | 正在连接 |
| **OPEN** | 1 | 连接已打开 |
| **CLOSING** | 2 | 正在关闭 |
| **CLOSED** | 3 | 连接已关闭 |

### 常用 WebSocket 方法

| 方法 | 说明 |
|------|------|
| **ws.send(data)** | 发送数据 |
| **ws.close()** | 关闭连接 |
| **ws.on('open', callback)** | 连接打开事件 |
| **ws.on('message', callback)** | 接收消息事件 |
| **ws.on('error', callback)** | 错误事件 |
| **ws.on('close', callback)** | 连接关闭事件 |

---

> 💡 **提示**：建议在生产环境中添加完善的日志记录和监控机制，以便及时发现和解决问题。

---

**关注我们，获取更多工业自动化技术干货！** 🎯

<div style="display: flex; justify-content: center; align-items: center; gap: 40px; margin: 30px 0;">
    <div style="text-align: center;">
        <img src="images/微信公众号.jpg" alt="微信公众号" style="width: 200px; height: 200px; object-fit: contain;">
        <p style="margin: 10px 0 0 0; font-size: 14px; color: #666;">微信公众号</p>
    </div>
    <div style="text-align: center;">
        <img src="images/单人二维码.png" alt="技术支持" style="width: 200px; height: 200px; object-fit: contain;">
        <p style="margin: 10px 0 0 0; font-size: 14px; color: #666;">技术支持</p>
    </div>
</div>

