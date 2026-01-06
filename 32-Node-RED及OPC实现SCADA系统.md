我们在node-red发布的数据是由函数模块处理的，循环模块用于连续发布。函数模块的代码如下：

## On Start
  global.set('firstTank', '10000');
  global.set('secondTank', '0');
  global.set('thirdTank', '0');
## On Message
  var firstTank = global.get('firstTank');
  var secondTank = global.get('secondTank');
  var thirdTank = global.get('thirdTank');
  if (firstTank <= 0) {
      global.set('firstTank', 10000);
      global.set('secondTank', 0);
      global.set('thirdTank', 0);
      firstTank=10000;
      secondTank=0;
      thirdTank=0;
  }

  firstTank = firstTank - 3;
  secondTank++;
  thirdTank++;
  thirdTank++;
  global.set('firstTank',firstTank);
  global.set('secondTank',secondTank);
  global.set('thirdTank',thirdTank);
  var data = {
      "firstTank":firstTank,
      "scondTank":secondTank,
      "thirdTank":thirdTank,
  };
  msg.payload = data;
  return msg;
要是将firstTank、secondTank和thirdTank封装成json格式，然后让mqtt-out模块发布它。


点击fuxa右下角的+按钮，输入Name，Type，选择Internal，最后点击OK得到一个新模块。该模块不具有与外部设备通信的功能，但它允许我们添加自定义标签。这些标签支持boolean、number和string三种数据类型，可以方便我们后续的工作。

![添加设备](images/fuxa-device.gif)



  硬件配置
我们使用以太网电缆将W10 PC和R1000连接到交换机，以确保它们位于同一网段。


显示和主要控制介绍
  图表
fuxa中有曲线图和直方图。以曲线图为例。图表的属性如图所示。您可以设置图表的名称、字体大小、数据格式、时间格式、X轴和Y轴样式以及其他属性。最重要的是要显示的Chart，它决定了我们要显示的数据源和行的格式。

![图表属性](images/fuxa-chart.gif)


我们点击Chart显示，然后选择New Chart，会出现一个新的弹出窗口，点击新弹出窗口右上角的+按钮，输入Name，然后点击OK，就可以成功新建一条线配置了。然后点击新建的线配置，然后点击Add Line，选择要显示的数据，最后点击OK，就会出现一条新的曲线。可以通过此过程添加多条曲线。最后单击OK完成配置。


我们在这里使用Chart来显示来自 Prosys OPC UA Simulation Server 的数据。您可以看到数据以图表的形式成功显示。

![图表显示](images/fuxa-chart2.gif)


  
Swich 开关
开关的属性如图所示。我们选择一个名为swich_1的布尔数据作为开关状态。您可以配置开关在打开或关闭时的显示状态，包括颜色配置，文本显示等。

![开关属性](images/fuxa-control.gif)


  形状
Fuxa提供了多种形状供用户绘制工业可视化界面。每个形状都有三个属性，即属性、事件和操作。其中，Property主要用于配置形状的颜色。通过绑定标记，形状将根据标记值的更改显示不同的颜色。您可以点击右上角的+来设置不同的颜色。

![形状属性](images/fuxa-shapes.gif)


这里我们以仓库模式为例，用Property填充它的颜色。


Events主要有两个内容，Type表示事件类型，Action表示事件触发后的动作。


操作需要绑定到一个Tag，以及不同的Tag值 可以触发不同的动作。设置值 的最小值和最大值，然后在“类型”选项中选择所需的操作。当Tag数据达到Min和Max之间的间隔时，将触发相应的操作。


这里我们以仓库模式为例，通过Actions控制其旋转和停止。


Pipe  管
在显示工业流程时，可以使用管道来表示工业物料的流向。管道的属性如图所示。

![管道属性](images/fuxa-pipe.gif)


属性部分可以设置管道的宽度、颜色和其他属性。动作也需要绑定到一个标签。不同的标记值 允许管道具有不同的动作。有四个主要的动作：停止，顺时针旋转，逆时针旋转和隐藏内容。本文展示了两个操作：停止和顺时针旋转。


为了模拟工业过程，我们添加了两个水箱和一些管道等图案。


Circular Gauge  圆形量规
除了图表外，Circular Gauge还可以真实的实时显示数据。有三种圆形量规可用。



使用时，需要通过绑定Tag指定要显示的数据。同时，您需要指定仪器可以显示的最大数据范围。您也可以在仪表板上设置线条等属性，这里我们选择/dev/fromfuxa主题中Tank 1的数据进行显示。



之后，2号和3号罐的数据也通过圆形仪表显示，以指示每个罐的当前容量。


  滑块
使用滑块调整流量、压力等变量，其属性如图所示。您可以设置其颜色和格式。使用时，需要绑定一个Tag。然后，滑块可以真实的调整Tag的值。这里我们绑定一个自定义的Flow control 1标签

![滑块属性](images/fuxa-slider-control.gif)


 报警
在工业生产过程中，某些参数（如压力）过大可能会造成一些危险。这时就需要报警，提醒工作人员这里可能有问题。Fuxa支持实时监控某一数值，当数值达到一定危险范围时触发报警。默认情况下，fuxa的界面不会打开报警栏。你需要设置它来打开警报栏。

![报警设置](images/fuxa-alarms.gif)


打开闹钟栏后，您可以设置闹钟。单击左上角的设置按钮，然后单击警报，然后在新窗口中单击+，显示警报设置窗口。此时需要绑定一个Tag，系统会监控Tag的值。警报有四个级别，即High High、High、Low、Message。您可以为每个级别设置一个Tag值范围，当Tag值达到该范围时，将触发相应级别的警报。


  SCADA演示


