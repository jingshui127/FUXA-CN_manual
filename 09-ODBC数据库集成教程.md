# 🗄️ FUXA ODBC 数据库集成教程

---

## 📋 概述

ODBC（Open Database Connectivity）允许 FUXA 与各种数据库系统进行交互，实现数据存储、查询和管理。

---

## 🚀 快速开始

### 推荐使用 Docker 版本

要开始使用 ODBC，建议使用 Docker 版本，因为 ODBC 驱动程序已预安装并准备就绪。

---

## 🔧 安装 ODBC 驱动

### 可用驱动

可用的驱动程序及其定义名称可以在以下位置找到：[ODBC Driver ini](https://github.com/frangoteam/FUXA/blob/master/odbc/odbcinst.ini)

### 在 Debian Linux 系统上安装

如果您在基于 Debian 的 Linux 系统上通过 NPM 安装，可以尝试使用以下步骤手动为您的系统安装 ODBC 驱动：

**步骤 1：** 安装 unixODBC
```bash
sudo apt-get update && sudo apt-get install -y unixodbc unixodbc-dev
```

**步骤 2：** 从 [ODBC Driver Files](https://github.com/frangoteam/FUXA/tree/master/odbc) 复制两个文件到您的系统

**步骤 3：** 进入下载文件的目录，使脚本可执行并安装和配置 ini 文件
```bash
sudo chmod +x install_odbc_drivers.sh
sudo ./install_odbc_drivers.sh
sudo cp odbcinst.ini /etc/odbcinst.ini
```

**步骤 4：** 测试安装的驱动，您可以使用 unixODBC 连接，更改连接字符串以适应您的数据库

```bash
# 测试 MySQL 连接
sudo myodbc-installer -s -a -c2 -n "test" -t "DRIVER=MySQL;SERVER=YourIP;PORT=3306;DATABASE=testDB;UID=User;PWD=MyPass"

# 测试连接
sudo isql test
```

---

## 💾 如何使用 ODBC

### 创建数据库连接

首先，您需要通过在 FUXA 中添加设备并选择 ODBC 来创建与数据库的连接。

如果您使用的是已定义的 DSN，可以输入它，或者只需在同一字段中添加完整的连接字符串，如下所示：

![ODBC 连接配置](https://github.com/user-attachments/assets/aacaae07-eb2f-4e78-878e-eaa9fa66bb43)

### 不同数据库的连接字符串

以下是不同数据库的连接字符串示例：

**PostgreSQL**
```
DRIVER=PostgreSQL;SERVER=Your_DB_IP;PORT=5432;DATABASE=testDB
```

**MySQL**
```
DRIVER=MySQL;SERVER=Your_DB_IP;PORT=3306;DATABASE=testDB;SSLMODE=DISABLED
```

⚠️ **注意**：MySQL 可能由于 SSLMODE 导致连接问题，请尝试在连接字符串中不使用 SSLMODE，并尝试启用和禁用。

- `SSLMODE=ENABLE`
- `SSLMODE=DISABLED`

将 `testDB` 替换为您的实际数据库名称。

---

## 📝 创建测试脚本

创建服务器端脚本进行测试，您可以使用测试选项卡和控制台来显示结果。

### 初始化设备

首先，您需要通过设备获取 ODBC 连接，在示例中，它被命名为 `postgreSQL`，如上图所示：

```javascript
// 初始化设备，名称与连接相同
let myDevice = await $getDevice('postgreSQL', true);
```

### 从数据库读取数据

```javascript
let result = await myDevice.pool.query(`SELECT * FROM "testTable"`);
console.log(JSON.stringify(result));
```

---

## ⚠️ 重要注意事项

### 表名格式

根据您的数据库，您可能需要将引号 `"testTable"` 移除为 `testTable` 或添加架构 `"DB_Schema"."testTable"`

### 连接名称唯一性

如果您需要在另一个脚本中使用 ODBC，则不能使用相同的连接名称：

**脚本 1**
```javascript
let myDevice1 = await $getDevice('postgreSQL', true);
```

**脚本 2**
```javascript
let myDevice2 = await $getDevice('postgreSQL', true);
```

---

## 🎯 完整示例

此示例还每 100ms 轮询标签，并使用触发器执行 SQL 查询，请注意不要使用此方法使系统过载，未来的理想解决方案是为标签创建事件监听器，我们可以使用简单的 addEventListener 方法而无需轮询。

还有一个 1 秒循环，从数据库更新值并将它们推送到 FUXA UI 中的表格。

还有一个名为查询管理器的函数，它处理触发器和执行的一次性操作。

**注意**：您可能需要重启 FUXA 才能使其正常工作，每次修改脚本时，有时修改脚本没问题，有时需要重启，因此如果您有任何奇怪的问题，请在创建问题之前尝试重启。

### 创建服务器端脚本并设置为启动时运行

```javascript
// 查询管理器，提供基于触发器事件的一次性函数
async function createQueryManager(device) {
    let lastTriggerState = false;
    return async function(trigger, sqlQuery) {
        if (trigger && trigger !== lastTriggerState) {
            try {
                const result = await device.pool.query(sqlQuery);
                lastTriggerState = trigger;
                return result;
            } catch (error) {
                return 'Error executing query';
            }
        }
        lastTriggerState = trigger;
    };
}

// 初始化设备，名称与连接相同
let myDevice = await $getDevice('postgreSQL', true);

// 为每种查询类型创建查询管理器，保留查询数据
let executeInsertQuery = await createQueryManager(myDevice); // 插入实例
let executeSelectQuery = await createQueryManager(myDevice); // 选择实例

// 全局变量以保留数据
let selResult;

// 100ms 循环捕获标签事件
let myLoop100ms = setInterval(loop100ms, 100);

async function loop100ms() {
  
    let customerName     = $getTag($getTagId('customerName'));
    let customerPhone    = $getTag($getTagId('customerPhone'));
    let customerEmail    = $getTag($getTagId('customerEmail'));
    let customerAge      = $getTag($getTagId('customerAge'));
    let execSaveCustomer = $getTag($getTagId('execSaveCustomer'));
  
    // 每 100ms 调用查询管理器实例函数，第一个参数是触发器，用于一次性执行查询
    await executeInsertQuery(
        execSaveCustomer,
        `INSERT INTO "testData"."Customer" ("Name", "Phone", "Email", "Age") VALUES ('${customerName}', '${customerPhone}', '${customerEmail}', ${customerAge})`
    );
  
    // 测试调用相同函数类型的第二个实例
    //selResult = await executeSelectQuery(
    //    execSaveCustomer,
    //    'SELECT * FROM "testData"."Customer"'
    //);
    //
    //$setTag($getTagId('customerDataArray'), JSON.stringify(selResult));
}

// 1 秒循环从数据库更新数据
let myLoop1sec = setInterval(loop1sec, 1000);

async function loop1sec() {
  // 在这里不需要使用查询管理器，因为我们每 1 秒从数据库读取以更新表格的数据
  selResult = await myDevice.pool.query('SELECT * FROM "testData"."Customer"');
  $setTag($getTagId('customerDataArray'), JSON.stringify(selResult));
}
```

### 创建客户端脚本

创建一个间隔为 1 秒的客户端脚本，此脚本将数据放入表格：

```javascript
let customerData = JSON.parse($getTag($getTagId('customerDataArray')));

// 列 ID 必须与数据库列匹配
var tableData = {
  columns: [{
    id: 'Name',
    label: 'Name'
    }, {
    id: 'Phone',    
    label: 'Phone'
    }, {
    id: 'Email',    
    label: 'Email'
    }, {
    id: 'Age',    
    label: 'Age'
  }],
  rows: customerData
};

// FUXA 中使用的表格名称
$invokeObject('customerTable', 'setTableAndData', tableData);
```

---

## 📊 常见数据库连接字符串

### PostgreSQL
```
DRIVER=PostgreSQL;SERVER=localhost;PORT=5432;DATABASE=mydb;UID=user;PWD=password
```

### MySQL
```
DRIVER=MySQL;SERVER=localhost;PORT=3306;DATABASE=mydb;UID=user;PWD=password;SSLMODE=DISABLED
```

### SQL Server
```
DRIVER=ODBC Driver 17 for SQL Server;SERVER=localhost;PORT=1433;DATABASE=mydb;UID=user;PWD=password
```

### Oracle
```
DRIVER=Oracle in OraClient18Home1;DBQ=localhost:1521/ORCL;UID=user;PWD=password
```

### SQLite
```
DRIVER=SQLite3;Database=/path/to/database.db
```

---

## 💡 最佳实践

### 1️⃣ 使用连接池

ODBC 连接使用连接池，避免频繁创建和销毁连接：

```javascript
// 好的做法：重用连接
let myDevice = await $getDevice('postgreSQL', true);

// 不好的做法：每次查询都创建新连接
// let myDevice = await $getDevice('postgreSQL', true);
// let result = await myDevice.pool.query(...);
```

### 2️⃣ 使用参数化查询

防止 SQL 注入攻击：

```javascript
// 好的做法：使用参数化查询
let name = $getTag($getTagId('customerName'));
let result = await myDevice.pool.query(
    'SELECT * FROM "Customer" WHERE "Name" = $1',
    [name]
);

// 不好的做法：字符串拼接
let name = $getTag($getTagId('customerName'));
let result = await myDevice.pool.query(
    `SELECT * FROM "Customer" WHERE "Name" = '${name}'`
);
```

### 3️⃣ 错误处理

始终处理查询错误：

```javascript
try {
    let result = await myDevice.pool.query('SELECT * FROM "testTable"');
    console.log(JSON.stringify(result));
} catch (error) {
    console.error('Query failed:', error);
}
```

### 4️⃣ 限制查询频率

避免过于频繁的查询导致数据库过载：

```javascript
// 好的做法：合理的查询间隔
let myLoop1sec = setInterval(loop1sec, 1000);

// 不好的做法：过于频繁的查询
// let myLoop10ms = setInterval(loop10ms, 10);
```

---

## 🔧 故障排除

### ❓ 连接失败

**可能原因**：
1. 连接字符串错误
2. 数据库服务器未运行
3. 防火墙阻止连接
4. 驱动程序未正确安装

**解决方案**：
1. 检查连接字符串格式
2. 确认数据库服务器正在运行
3. 检查防火墙设置
4. 重新安装 ODBC 驱动

### ❓ 查询超时

**可能原因**：
1. 查询过于复杂
2. 数据库负载过高
3. 网络延迟

**解决方案**：
1. 优化查询语句
2. 添加适当的索引
3. 增加超时时间

### ❓ SSL 连接问题（MySQL）

**可能原因**：
1. SSLMODE 配置不正确
2. 证书问题

**解决方案**：
```javascript
// 尝试不同的 SSLMODE 设置
// SSLMODE=DISABLED
// SSLMODE=REQUIRED
// SSLMODE=PREFERRED
```

### ❓ 表名或列名错误

**可能原因**：
1. 引号使用不当
2. 架构名称不正确

**解决方案**：
```javascript
// 尝试不同的表名格式
// "testTable"
// testTable
// "schema"."testTable"
```

---

## 🎉 总结

通过本教程，您已经学会了：

✅ 安装和配置 ODBC 驱动  
✅ 创建数据库连接  
✅ 执行 SQL 查询  
✅ 在 FUXA UI 中显示数据  
✅ 遵循最佳实践  
✅ 故障排除  

现在您可以在 FUXA 中集成各种数据库了！

---

> 💡 **提示**：建议在生产环境中使用连接池和参数化查询，以提高性能和安全性。

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

