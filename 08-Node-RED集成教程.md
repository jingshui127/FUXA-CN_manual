# 🔌 FUXA 与 Node-RED 集成教程

---

## 📋 概述

FUXA 包含完整的 Node-RED 集成，允许您创建与 SCADA 系统交互的强大自动化流程。

---

## 🚀 安装和配置

### Node-RED 在 FUXA 中

Node-RED 自动包含在 FUXA 中，无需额外安装。通过 FUXA 设置菜单访问。

### 安装 Dashboard 2

如果需要，必须单独安装 Dashboard 2：

1. 打开 Node-RED 编辑器（通过 FUXA 设置）
2. 点击菜单（☰）→ **管理面板**（Manage Palette）
3. 搜索：`@flowfuse/node-red-dashboard`
4. 点击 **安装**（Install）
5. 重启 Node-RED/FUXA

### 所需依赖

- **@flowfuse/node-red-dashboard**：用于创建现代仪表盘
- **node-red-contrib-fuxa**：自动包含（提供 FUXA 集成节点）

### 配置

无需额外配置。Node-RED 自动连接到 FUXA 的运行时环境。

---

## 🎯 访问 Node-RED

### Node-RED 编辑器

通过 FUXA 设置访问 Node-RED 流编辑器：

1. 在 FUXA 中点击 **设置**（Settings）按钮
2. 导航到 **Node-RED** 部分
3. 点击 **打开 Node-RED 编辑器**（Open Node-RED Editor）

这将在新窗口/标签页中打开 Node-RED 流编辑器。

### Dashboard 2

**注意**：Dashboard 2 默认未安装，必须单独安装。

#### 安装步骤
1. 在 Node-RED 中，进入 **菜单 → 管理面板**
2. 搜索并安装：`@flowfuse/node-red-dashboard`
3. 重启 Node-RED/FUXA

#### 访问 Dashboard 2

安装后，查看您的 Node-RED 仪表盘：

**嵌入 FUXA 视图**：向任何 FUXA 视图添加 iframe 组件

#### 在 FUXA 视图中嵌入仪表盘

1. 在编辑器中打开 FUXA 项目
2. 向视图添加 iframe 组件
3. 将 URL 设置为：`/nodered/api/dashboard`
4. 根据需要配置 iframe 大小和属性
5. 如果只想显示单个页面，可以调整仪表盘设置并使用 `/nodered/api/dashboard/page1` 或页面名称

**重要**：在尝试访问 `/nodered/api/dashboard` 之前必须安装 Dashboard 2

---

## 🔧 FUXA 贡献节点

FUXA 贡献包提供用于 SCADA 集成的专用节点，此包设计为仅与 FUXA Node-RED 集成一起使用，在独立的 Node-RED 安装中无法工作

### 标签节点

#### get-tag
**用途**：获取 FUXA 标签的当前值

**参数**：
- **名称**：用于识别的可选节点名称
- **标签**：标签名称（从 FUXA 设备填充的下拉列表）

**输入**：任何消息（触发标签读取）
**输出**：`msg.payload` 包含标签值

**示例输出**：
```json
{
  "payload": 25.3,
  "_msgid": "abc123"
}
```

#### set-tag
**用途**：向 FUXA 标签写入值

**参数**：
- **名称**：用于识别的可选节点名称
- **标签**：标签名称（从 FUXA 设备填充的下拉列表）

**输入**：`msg.payload` 包含要写入的值
**输出**：`msg.payload` 包含写入的值

**示例输入**：
```json
{
  "payload": 50.0
}
```

#### get-tag-change
**用途**：基于设备轮询事件监控 FUXA 标签的值变化

**参数**：
- **名称**：用于识别的可选节点名称
- **标签**：标签名称（从 FUXA 设备填充的下拉列表）

**输入**：无（事件驱动）
**输出**：`msg.payload` 包含新标签值（当它变化时）

**工作原理**：此节点订阅 FUXA 的设备轮询事件。当设备被轮询且标签值自上次轮询以来发生变化时，节点输出包含新值的消息。时间取决于设备的轮询间隔（通常为 1-5 秒）。

**示例输出**：
```json
{
  "payload": 25.3,
  "topic": "temperature",
  "tagId": "device1.temperature",
  "tagName": "temperature",
  "timestamp": "2025-01-01T10:30:00.000Z",
  "previousValue": 24.8
}
```

**注意**：此节点仅在标签值实际变化时输出消息，而不是在每个轮询周期。它高效地监控变化而无需手动轮询。

#### get-tag-id
**用途**：按名称获取标签的内部 ID

**参数**：
- **名称**：用于识别的可选节点名称
- **标签**：标签名称（从 FUXA 设备填充的下拉列表）

**输入**：任何消息
**输出**：`msg.payload` 包含标签 ID

#### get-historical-tags
**用途**：同时检索多个标签的历史标签数据

**参数**：
- **名称**：用于识别的可选节点名称
- **标签**：逗号分隔的标签名称列表（例如 "temp1,temp2,pressure"）
- **开始时间**：历史期间的开始（datetime-local 选择器）
- **结束时间**：历史期间的结束（datetime-local 选择器）

**输入**：任何消息或使用 `msg.tags`、`msg.from`、`msg.to` 覆盖
**输出**：`msg.payload` 包含历史数据数组

**多标签支持**：
- 输入逗号分隔的标签：`temp1,temp2,pressure`
- 每个标签的历史数据在同一时间段内检索
- 结果组合在单个响应中

**示例输入**（逗号分隔）：
```json
{
  "tags": "temp1,temp2,pressure",
  "from": "2025-01-01T08:00",
  "to": "2025-01-01T17:00"
}
```

**示例输入**（数组）：
```json
{
  "tags": ["temp1", "temp2", "pressure"],
  "from": "2025-01-01T08:00",
  "to": "2025-01-01T17:00"
}
```

**示例输出**：
```json
{
  "payload": [
    {
      "tag": "temp1",
      "data": [
        {"timestamp": "2025-01-01T08:00:00Z", "value": 25.3},
        {"timestamp": "2025-01-01T09:00:00Z", "value": 26.1}
      ]
    },
    {
      "tag": "temp2", 
      "data": [
        {"timestamp": "2025-01-01T08:00:00Z", "value": 24.8},
        {"timestamp": "2025-01-01T09:00:00Z", "value": 25.2}
      ]
    }
  ]
}
```

#### get-tag-daq-settings
**用途**：获取标签的 DAQ（数据采集）设置

**参数**：
- **名称**：用于识别的可选节点名称
- **标签**：标签名称（从 FUXA 设备填充的下拉列表）

**输入**：任何消息
**输出**：`msg.payload` 包含 DAQ 设置对象

#### set-tag-daq-settings
**用途**：配置标签的 DAQ（数据采集）设置

**参数**：
- **名称**：用于识别的可选节点名称
- **标签**：标签名称（从 FUXA 设备填充的下拉列表）
- **启用**：复选框以启用/禁用此标签的 DAQ
- **间隔**：采样间隔（毫秒）
- **死区**：数据更新的最小变化阈值

**输入**：任何消息或使用 `msg.tag`、`msg.enabled`、`msg.interval`、`msg.deadband` 覆盖
**输出**：`msg.payload` 包含更新的设置

**DAQ 设置**：
- **启用**：为此标签打开/关闭数据采集
- **间隔**：采样标签的频率（毫秒）
- **死区**：仅报告大于此阈值的更改（防止噪声）

### 设备节点

#### enable-device
**用途**：启用或禁用设备连接

**参数**：
- **名称**：用于识别的可选节点名称
- **设备名称**：设备名称（从 FUXA 设备填充的下拉列表）
- **启用**：复选框以启用/禁用设备

**输入**：任何消息或使用 `msg.deviceName`、`msg.enabled` 覆盖
**输出**：`msg.payload` 包含操作结果

#### get-device
**用途**：获取 FUXA 设备的信息

**参数**：
- **名称**：用于识别的可选节点名称
- **设备名称**：设备名称（从 FUXA 设备填充的下拉列表）
- **包含标签**：复选框以在响应中包含标签信息

**输入**：任何消息或使用 `msg.deviceName`、`msg.includeTags` 覆盖
**输出**：`msg.payload` 包含设备信息对象

**包含标签**：选中时，响应包括与设备关联的所有标签

#### get-device-property
**用途**：从设备获取属性值

**参数**：
- **名称**：用于识别的可选节点名称
- **设备名称**：设备名称（从 FUXA 设备填充的下拉列表）
- **属性**：要检索的属性名称

**输入**：任何消息或使用 `msg.deviceName`、`msg.property` 覆盖
**输出**：`msg.payload` 包含属性值

**属性名称**：常见属性包括 "status"、"connected"、"lastError" 等

#### set-device-property
**用途**：在设备上设置属性值

**参数**：
- **名称**：用于识别的可选节点名称
- **设备名称**：设备名称（从 FUXA 设备填充的下拉列表）
- **属性**：要设置的属性名称
- **值**：为属性设置的值

**输入**：`msg.payload` 包含值或使用 `msg.deviceName`、`msg.property`、`msg.value` 覆盖
**输出**：`msg.payload` 包含设置的值

### 报警节点

#### get-alarms
**用途**：获取当前活动报警

**参数**：
- **名称**：用于识别的可选节点名称

**输入**：任何消息
**输出**：`msg.payload` 包含活动报警数组

**示例输出**：
```json
{
  "payload": [
    {
      "id": "alarm1",
      "name": "High Temperature",
      "status": "active",
      "timestamp": "2025-01-01T10:30:00Z",
      "value": 85.5
    }
  ]
}
```

#### get-history-alarms
**用途**：获取历史报警数据

**参数**：
- **名称**：用于识别的可选节点名称
- **开始时间**：历史期间的开始（datetime-local 选择器）
- **结束时间**：历史期间的结束（datetime-local 选择器）

**输入**：任何消息或使用 `msg.startTime` 和 `msg.endTime` 覆盖
**输出**：`msg.payload` 包含历史报警数组

#### ack-alarm
**用途**：确认 FUXA 中的报警

**参数**：
- **名称**：用于识别的可选节点名称
- **报警名称**：报警名称（从 FUXA 报警填充的下拉列表）
- **类型**：逗号分隔的报警类型（可选）

**输入**：任何消息或使用 `msg.alarmName`、`msg.types` 覆盖
**输出**：`msg.payload` 包含确认结果

**报警类型**：指定报警类型以确认特定报警类别（逗号分隔："warning,error,critical"）

### 视图节点

#### set-view
**用途**：更改 FUXA 中的当前视图

**参数**：
- **名称**：用于识别的可选节点名称
- **视图名称**：视图名称（从 FUXA 视图填充的下拉列表）

**输入**：任何消息或使用 `msg.viewName` 覆盖
**输出**：`msg.payload` 包含操作结果

#### open-card
**用途**：在 FUXA 中打开特定的卡片/对话框

**参数**：
- **名称**：用于识别的可选节点名称
- **卡片**：卡片名称（从 FUXA 卡片填充的下拉列表）

**输入**：任何消息或使用 `msg.cardName` 覆盖
**输出**：`msg.payload` 包含操作结果

### 脚本节点

#### execute-script
**用途**：执行 FUXA 脚本

**参数**：
- **名称**：用于识别的可选节点名称
- **脚本**：脚本名称（从 FUXA 脚本填充的下拉列表）

**输入**：任何消息或使用 `msg.scriptName` 覆盖
**输出**：`msg.payload` 包含执行结果

**示例输出**：
```json
{
  "payload": {
    "success": true,
    "script": "myScript",
    "result": "Script completed successfully",
    "timestamp": "2025-01-01T10:45:00Z"
  }
}
```

### DAQ 节点

#### get-daq
**用途**：获取单个标签的数据采集（DAQ）数据

**参数**：
- **名称**：用于识别的可选节点名称
- **标签**：单个标签名称（从 FUXA 设备填充的下拉列表）
- **开始时间**：DAQ 期间的开始（datetime-local 选择器）
- **结束时间**：DAQ 期间的结束（datetime-local 选择器）

**输入**：任何消息或使用 `msg.from`、`msg.to` 覆盖
**输出**：`msg.payload` 包含单个标签的 DAQ 数据

**仅单个标签**：与 get-historical-tags 不同，此节点一次只处理一个标签。对于多个标签，使用单独的 get-daq 节点或 get-historical-tags。

**示例输出**：
```json
{
  "payload": [
    {"timestamp": "2025-01-01T10:00:00Z", "value": 25.3, "quality": "good"},
    {"timestamp": "2025-01-01T10:01:00Z", "value": 25.8, "quality": "good"}
  ]
}
```

### 事件节点

#### emit-event
**用途**：通过 FUXA 的事件系统发出自定义事件，用于系统间通信和自动化触发

**参数**：
- **名称**：用于识别的可选节点名称
- **事件类型**：自定义事件名称/类型（例如 "machine-fault"、"production-complete"、"maintenance-required"）

**输入**：`msg.payload` 包含事件数据（任何格式：字符串、数字、对象、数组）
**输出**：`msg.payload` 不变（传递）

**事件类型和用法**：

**系统事件**（内置 FUXA 事件）：
- `device-status` - 设备连接状态变化
- `device-property` - 设备属性更新
- `device-values` - 标签值变化
- `alarms-status` - 报警状态变化
- `script-console` - 脚本控制台输出
- `heartbeat` - 系统心跳/存活信号

**自定义事件**（用户定义）：
- `production-start` - 生产线启动
- `production-stop` - 生产线停止
- `quality-alert` - 质量控制警报
- `maintenance-due` - 设备需要维护
- `operator-login` - 操作员认证
- `batch-complete` - 生产批次完成

**事件数据示例**：

**简单字符串事件**：
```json
{
  "payload": "Machine fault detected"
}
```

**结构化事件数据**：
```json
{
  "payload": {
    "eventType": "production-alert",
    "machine": "Line-A",
    "severity": "high",
    "timestamp": "2025-01-01T10:30:00Z",
    "details": {
      "temperature": 85.5,
      "pressure": 2.1,
      "errorCode": "E-202"
    }
  }
}
```

**数组数据事件**：
```json
{
  "payload": [
    {"sensor": "temp1", "value": 75.2},
    {"sensor": "temp2", "value": 76.8},
    {"sensor": "temp3", "value": 74.9}
  ]
}
```

**事件工作原理**：
1. 事件发出到 FUXA 的内部事件系统
2. 其他 FUXA 组件可以监听这些事件
3. 事件可以触发脚本、更新显示或启动自动化序列
4. 事件持续存在直到被消费或系统重启

**常见用例**：
- **设备监控**：当设备进入故障状态时发出事件
- **生产跟踪**：发出生产里程碑或质量问题信号
- **维护警报**：通知何时设备需要服务
- **操作员通知**：向操作员警报系统条件
- **数据集成**：将结构化数据发送到外部系统

#### send-message
**用途**：通过 FUXA 的通知系统发送电子邮件通知或消息

**参数**：
- **名称**：用于识别的可选节点名称
- **地址**：收件人电子邮件地址
- **主题**：电子邮件主题行
- **消息**：默认消息内容（可以覆盖）

**输入**：`msg.payload` 可以包含消息数据或使用 `msg.address`、`msg.subject`、`msg.message` 覆盖
**输出**：`msg.payload` 包含发送结果

**消息格式选项**：

**简单文本消息**（使用配置的地址/主题）：
```json
{
  "payload": "Alert: Temperature exceeded threshold"
}
```

**完整消息覆盖**：
```json
{
  "address": "operator@company.com",
  "subject": "Production Alert",
  "message": "Line A has stopped due to maintenance requirement"
}
```

**多个收件人**：
```json
{
  "address": ["operator1@company.com", "supervisor@company.com"],
  "subject": "Quality Control Alert",
  "message": "Batch #1234 failed quality inspection"
}
```

---

## 📊 数据格式

### 标签值
标签值可以是：
- **数字**：`25.3`、`100`、`0`
- **字符串**：`"Running"`、`"Stopped"`
- **布尔值**：`true`、`false`
- **对象**：复杂数据结构

### 时间戳
所有时间戳使用 ISO 8601 格式：
```json
"2025-01-01T10:30:00.000Z"
```

### 错误处理
所有节点将错误输出到调试选项卡。常见错误模式：
```json
{
  "payload": null,
  "_msgid": "abc123",
  "error": "Tag not found: myTag"
}
```

---

## 🔧 故障排除

### 仪表盘未加载
**问题**：`/nodered/api/dashboard` 显示错误或空白页

**解决方案**：安装 Dashboard 2
1. 打开 Node-RED 编辑器
2. 进入 **管理面板**
3. 安装 `@flowfuse/node-red-dashboard`
4. 重启 Node-RED/FUXA

### FUXA 节点未出现
**问题**：FUXA 贡献节点在面板中不可见

**解决方案**：检查 Node-RED 日志中的错误。当 FUXA 启动 Node-RED 时，节点会自动注册。

### 下拉列表未填充
**问题**：标签/设备下拉列表为空

**解决方案**：确保您在 FUXA 中配置了设备和标签。下拉列表从您的 FUXA 项目数据填充。

### 事件不工作
**问题**：发出的事件未触发预期行为

**解决方案**：检查其他 FUXA 组件（脚本、视图）是否正在监听正确的事件类型。事件区分大小写。

### 电子邮件通知未发送
**问题**：send-message 节点未传递电子邮件

**解决方案**：在 FUXA 服务器配置中配置 SMTP 设置。检查 FUXA 日志中的 SMTP 连接错误。

---

## 💡 最佳实践

### 1️⃣ 使用事件驱动架构

使用 `get-tag-change` 而不是轮询标签，提高效率：

```javascript
// 不推荐：轮询标签
setInterval(() => {
  // 每 100ms 检查标签值
}, 100);

// 推荐：使用事件驱动
// get-tag-change 节点仅在值变化时触发
```

### 2️⃣ 批量处理历史数据

使用 `get-historical-tags` 一次获取多个标签的历史数据：

```json
{
  "tags": ["temp1", "temp2", "pressure"],
  "from": "2025-01-01T08:00",
  "to": "2025-01-01T17:00"
}
```

### 3️⃣ 使用自定义事件进行系统集成

使用 `emit-event` 节点在不同系统之间传递信息：

```json
{
  "payload": {
    "eventType": "production-alert",
    "machine": "Line-A",
    "severity": "high"
  }
}
```

### 4️⃣ 配置 DAQ 设置优化性能

使用 `set-tag-daq-settings` 节点优化数据采集：

- 设置合理的采样间隔
- 使用死区减少噪声
- 仅启用需要的标签

---

## 🎉 总结

通过本教程，您已经学会了：

✅ 安装和配置 Node-RED 集成  
✅ 使用 FUXA 贡献节点  
✅ 配置标签、设备、报警、视图和脚本节点  
✅ 使用事件系统进行系统集成  
✅ 故障排除和最佳实践  

现在您可以创建强大的自动化流程与 FUXA SCADA 系统交互了！

---

> 💡 **提示**：Node-RED 提供了丰富的节点库，可以与 FUXA 结合使用，实现复杂的自动化逻辑。

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

