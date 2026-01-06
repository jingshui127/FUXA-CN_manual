# [FUXA] 使用Node-RED及OPC实现一个完整的SCADA系统

FUXA是一个基于网络的过程可视化（SCADA/HMI/仪表板）软件。通过FUXA，您可以为您的机器创建个性化设计的现代过程可视化和实时数据显示。它支持Modbus RTU/TCP，Siemens S7协议，OPC-UA，BACnet IP，MQTT和其他协议。

本文主要介绍了如何使用FUXA实现SCADA系统。在本文中，FUXA接收来自Node-RED和OPC UA Simulator的数据，并使用图表和圆形量规显示它；同时，它绘制了一系列模式来模拟工业过程。

## 开始使用

在开始此项目之前，您可能需要按照此处所述提前准备硬件和软件。

### 硬件准备

### 软件准备

Python 3.11可能与FUXA不兼容。如果您的Python版本是3.11，请考虑更改为其他Python版本。

## 安装FUXA

您需要安装Node Version 14 || 16 || 18。

```bash
wget https://nodejs.org/dist/v18.20.3/node-v18.20.3-linux-arm64.tar.xz
tar -xf node-v18.20.3-linux-arm64.tar.xz
cd node-v18.20.3-linux-arm64
sudo cp -R * /usr/local/
node -v
npm -v
```

接下来从npm安装FUXA：

```bash
sudo npm install -g --unsafe-perm @frangoteam/fuxa
sudo fuxa
```

## Node-RED数据处理

在Node-RED发布的数据是由函数模块处理的，循环模块用于连续发布。函数模块的代码如下：

```javascript
// On Start
global.set('firstTank', '10000');
global.set('secondTank', '0');
global.set('thirdTank', '0');

// On Message
var firstTank = global.get('firstTank');
var secondTank = global.get('secondTank');
var thirdTank = global.get('thirdTank');

if (firstTank <= 0) {
    global.set('firstTank', 10000);
    global.set('secondTank', 0);
    global.set('thirdTank', 0);
    firstTank = 10000;
    secondTank = 0;
    thirdTank = 0;
}

firstTank = firstTank - 3;
secondTank++;
thirdTank++;
thirdTank++;

global.set('firstTank', firstTank);
global.set('secondTank', secondTank);
global.set('thirdTank', thirdTank);

var data = {
    "firstTank": firstTank,
    "secondTank": secondTank,
    "thirdTank": thirdTank,
};
msg.payload = data;
return msg;
```

需要将firstTank、secondTank和thirdTank封装成JSON格式，然后让mqtt-out模块发布它。

## FUXA配置

### 添加内部设备

点击FUXA右下角的+按钮，输入Name，Type，选择Internal，最后点击OK得到一个新模块。

该模块不具有与外部设备通信的功能，但它允许我们添加自定义标签。这些标签支持boolean、number和string三种数据类型，可以方便我们后续的工作。

### 硬件配置

我们使用以太网电缆将W10 PC和R1000连接到交换机，以确保它们位于同一网段。

## 显示和主要控制介绍

### 图表

FUXA中有曲线图和直方图。以曲线图为例。

图表的属性如图所示。您可以设置图表的名称、字体大小、数据格式、时间格式、X轴和Y轴样式以及其他属性。

最重要的是要显示的Chart，它决定了我们要显示的数据源和行的格式。

我们点击Chart显示，然后选择New Chart，会出现一个新的弹出窗口，点击新弹出窗口右上角的+按钮，输入Name，然后点击OK，就可以成功新建一条线配置了。

然后点击新建的线配置，然后点击Add Line，选择要显示的数据，最后点击OK，就会出现一条新的曲线。可以通过此过程添加多条曲线。最后单击OK完成配置。

我们在这里使用Chart来显示来自Prosys OPC UA Simulation Server的数据。您可以看到数据以图表的形式成功显示。

### Switch 开关

开关的属性如图所示。我们选择一个名为switch_1的布尔数据作为开关状态。

您可以配置开关在打开或关闭时的显示状态，包括颜色配置，文本显示等。

### 形状

FUXA提供了多种形状供用户绘制工业可视化界面。每个形状都有三个属性，即属性、事件和操作。

其中，Property主要用于配置形状的颜色。通过绑定标记，形状将根据标记值的更改显示不同的颜色。您可以点击右上角的+来设置不同的颜色。

这里我们以仓库模式为例，用Property填充它的颜色。

Events主要有两个内容，Type表示事件类型，Action表示事件触发后的动作。

操作需要绑定到一个Tag，以及不同的Tag值可以触发不同的动作。设置值的最小值和最大值，然后在"类型"选项中选择所需的操作。当Tag数据达到Min和Max之间的间隔时，将触发相应的操作。

这里我们以仓库模式为例，通过Actions控制其旋转和停止。

### Pipe 管道

在显示工业流程时，可以使用管道来表示工业物料的流向。

管道的属性如图所示。属性部分可以设置管道的宽度、颜色和其他属性。

动作也需要绑定到一个标签。不同的标记值允许管道具有不同的动作。有四个主要的动作：停止，顺时针旋转，逆时针旋转和隐藏内容。

本文展示了两个操作：停止和顺时针旋转。为了模拟工业过程，我们添加了两个水箱和一些管道等图案。

### Circular Gauge 圆形量规

除了图表外，Circular Gauge还可以真实的实时显示数据。有三种圆形量规可供选择，可以根据需要配置不同的显示样式和数据范围。

---

**技术支持：科控物联**
- QQ: 2492123056
