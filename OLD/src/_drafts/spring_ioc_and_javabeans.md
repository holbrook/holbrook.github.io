javabean: 实现了一个接口规范

接口可以多态，规范也可以实现多态


javabean， EJB， OSGI， Spring， 。。。 。。。

“标准接口”是人类解决复杂问题的一种有效方式


# 总线与标准接口

总线技术大概是计算机发展过程中一个里程碑式的技术。从1970年DEC公司PDP-11小型计算机首次采用总线技术以来，微型计算机一直采用总线结构。

总线定义了一系列的标准，包括各引线的信号、时序、电气盒机械特性等，从而形成了标准的信息通路，使得符合总线标准的芯片、板卡以及外设具备兼容性。

![](/images/2013/spring/hierarchy-bus.png)


对于计算机硬件系统来说，总线是一个独立的部件；对于板卡及I/O设备来说，其与计算机的接口就是与总线的接口。

![](/images/2013/spring/mainboard.jpg)

如上图，微机主板上看到的内存插槽、PCI插槽、AGP插槽等，其实是内存总线、PCI总线、AGP总线暴露的标准接口。

更常见的接口是USB接口，广泛用于各种外设。


# 容器、组件和插件

总线技术不仅仅用于计算机，现在工业控制中“现场总线”技术的应用也十分广泛。在软件技术中，也借鉴了总线的设计思想。

比如：容器、插件、组件等。


## 容器的作用

管理bean的生命周期——创建，销毁（对象创建模式）
管理对象的关联和依赖，(生成器模式？)
——通过容器，可以不构件相关的对象；由容器统一管理


## 对象之间的关系和依赖管理


3.1.1  ; 依赖和依赖注入
       传统应用程序设计中所说的依赖一般指“类之间的关系”，那先让我们复习一下类之间的关系：
     泛化：表示类与类之间的继承关系、接口与接口之间的继承关系；
     实现：表示类对接口的实现；
     依赖：当类与类之间有使用关系时就属于依赖关系，不同于关联关系，依赖不具有“拥有关系”，而是一种“相识关系”，只在某个特定地方（比如某个方法体内）才有关系。
     关联：表示类与类或类与接口之间的依赖关系，表现为“拥有关系”；具体到代码可以用实例变量来表示；
     聚合：属于是关联的特殊情况，体现部分-整体关系，是一种弱拥有关系；整体和部分可以有不一样的生命周期；是一种弱关联；
     组合：属于是关联的特殊情况，也体现了体现部分-整体关系，是一种强“拥有关系”；整体与部分有相同的生命周期，是一种强关联；

Spring IoC容器的依赖有两层含义：Bean依赖容器和容器注入Bean的依赖资源：
     Bean依赖容器：也就是说Bean要依赖于容器，这里的依赖是指容器负责创建Bean并管理Bean的生命周期，正是由于由容器来控制创建Bean并注入依赖，也就是控制权被反转了，这也正是IoC名字的由来，此处的有依赖是指Bean和容器之间的依赖关系。
     容器注入Bean的依赖资源：容器负责注入Bean的依赖资源，依赖资源可以是Bean、外部文件、常量数据等，在Java中都反映为对象，并且由容器负责组装Bean之间的依赖关系，此处的依赖是指Bean之间的依赖关系，可以认为是传统类与类之间的“关联”、“聚合”、“组合”关系。
为什么要应用依赖注入，应用依赖注入能给我们带来哪些好处呢？
     动态替换Bean依赖对象，程序更灵活：替换Bean依赖对象，无需修改源文件：应用依赖注入后，由于可以采用配置文件方式实现，从而能随时动态的替换Bean的依赖对象，无需修改java源文件；

     更好实践面向接口编程，代码更清晰：在Bean中只需指定依赖对象的接口，接口定义依赖对象完成的功能，通过容器注入依赖实现；

     更好实践优先使用对象组合，而不是类继承：因为IoC容器采用注入依赖，也就是组合对象，从而更好的实践对象组合。

   * 采用对象组合，Bean的功能可能由几个依赖Bean的功能组合而成，其Bean本身可能只提供少许功能或根本无任何功能，全部委托给依赖Bean，对象组合具有动态性，能更方便的替换掉依赖Bean，从而改变Bean功能；
   * 而如果采用类继承，Bean没有依赖Bean，而是采用继承方式添加新功能，，而且功能是在编译时就确定了，不具有动态性，而且采用类继承导致Bean与子Bean之间高度耦合，难以复用。

     增加Bean可复用性：依赖于对象组合，Bean更可复用且复用更简单；

     降低Bean之间耦合：由于我们完全采用面向接口编程，在代码中没有直接引用Bean依赖实现，全部引用接口，而且不会出现显示的创建依赖对象代码，而且这些依赖是由容器来注入，很容易替换依赖实现类，从而降低Bean与依赖之间耦合；

     代码结构更清晰：要应用依赖注入，代码结构要按照规约方式进行书写，从而更好的应用一些最佳实践，因此代码结构更清晰。

从以上我们可以看出，其实依赖注入只是一种装配对象的手段，设计的类结构才是基础，如果设计的类结构不支持依赖注入，Spring IoC容器也注入不了任何东西，从而从根本上说“如何设计好类结构才是关键，依赖注入只是一种装配对象手段”。

前边IoC一章我们已经了解了Bean依赖容器，那容器如何注入Bean的依赖资源，Spring IoC容器注入依赖资源主要有以下两种基本实现方式：

     构造器注入：就是容器实例化Bean时注入那些依赖，通过在在Bean定义中指定构造器参数进行注入依赖，包括实例工厂方法参数注入依赖，但静态工厂方法参数不允许注入依赖；

     setter注入：通过setter方法进行注入依赖；

     方法注入：能通过配置方式替换掉Bean方法，也就是通过配置改变Bean方法 功能。

我们已经知道注入实现方式了，接下来让我们来看看具体配置吧。



## Spring不仅仅是IoC容器
其他公共功能：
通用日志记录、性能统计、安全控制、异常处理等面向切面的能力


数据库事务，本身提供了一套简单的JDBC访问实现，提供与第三方数据访问框架集成（如Hibernate、JPA），与各种Java EE技术整合（如Java Mail、任务调度等等），提供一套自己的web层框架Spring MVC、而且还能非常简单的与第三方web框架集成。


Spring框架除了帮我们管理对象及其依赖关系，还提供像，还能帮我管理最头疼的从这里我们可以认为Spring是一个超级粘合平台，除了自己提供功能外，还提供粘合其他技术和框架的能力，从而使我们可以更自由的选择到底使用什么技术进行开发。而且不管是JAVA SE（C/S架构）应用程序还是JAVA EE（B/S架构）应用程序都可以使用这个平台进行开发。让我们来深入看一下Spring到底能帮我们做些什么？



# JavaBean

JavaBean可分为两种
一种是有用户界面（UI，User Interface）的JavaBean
还有一种是没有用户界面，主要负责处理事务（如数据运算，操纵数据库）的JavaBean
我们用的JSP通常用的就是后一种JavaBean

JavaBean说白了就是一个Java类
只是他加了getter和setter方法，将属性暴露在外面




JavaBeans是Java开发语言中一个可以重复使用的软件组件，实质上是许多对象类封装成一个单一的对象（Bean）。特点是序列化机制，有无参构造器，每个属性都被使用private修饰，访问属性时需使用被public修饰的getter和setter方法。
优点[编辑]

JavaBeans是“一次编写，到处运行”理念的Java组件。
一个bean暴露到另一个应用程序的属性，事件和方法是可控的。
一个bean可以接收来自其他对象的事件，也可以产生事件并发送到其他对象中。
有帮助设置Bean的软件。
Bean类可以被保存在持久性存储器中，以供日后重用。




介绍

最初，JavaBean的目的是为了将可以重复使用的软件代码打包标准。特别是用于帮助厂家开发在综合开发环境（IDE）下使用的java软件部件。这些包括如Grid控件，用户可以将该部件拖放到开发环境中。从此，JavaBean就可以扩展为一个java web 应用的标准部件，并且JavaBean部件框架已经扩展为企业版的 Bean（EJB）。
JavaBean 和 Server Bean（通常称为 Enterprise JavaBean (EJB)）有一些基本相同之处。它们都是用一组特性创建，以执行其特定任务的对象或组件。它们还有从当前所驻留服务器上的容器获得其它特性的能力。这使得 bean 的行为根据特定任务和所在环境的不同而有所不同。
2Enterprise Bean 与 JavaBean 不同

JavaBean 是使用 java.beans 包开发的，它是 Java 2 标准版的一部分。JavaBean 是一台机器上同一个地址空间中运行的组件。JavaBean 是进程内组件。Enterprise Bean 是使用 javax.ejb 包开发的，它是标准 JDK 的扩展，是 Java 2 Enterprise Edition 的一部分。Enterprise Bean 是在多台机器上跨几个地址空间运行的组件。因此 Enterprise Bean 是进程间组件。JavaBean 通常用作 GUI 窗口小部件，而 Enterprise Bean 则用作分布式商业对象。
JavaBean 是一种JAVA语言写成的可重用组件。为写成JavaBean，类必须是具体的和公共的，并且具有无参数的构造器。JavaBeans 通过提供符合一致性设计模式的公共方法将内部域暴露成为属性。众所周知，属性名称符合这种模式，其他Java 类可以通过自省机制发现和操作这些JavaBean 属性。
用户可以使用JavaBean将功能、处理、值、数据库访问和其他任何可以用java代码创造的对象进行打包，并且其他的开发者可以通过内部的JSP页面、Servlet、其他JavaBean、applet程序或者应用来使用这些对象。用户可以认为JavaBean提供了一种随时随地的复制和粘贴的功能，而不用关心任何改变。
JavaBean是Sun微系统的一个面向对象的编程接口，它可以让你建可重用应用程序或能在网络中任何主流操作系统平台上配置的程序块，称作组件。像Java applet一样，JavaBeans组件(或“Beans”)能够给予万维网页面交互的能力，例如：计算感兴趣的比率或是根据用户或浏览器的特性改变页面内容。
从用户的观点来看，一个组件可以是一个与你交互的按钮或是一个当你按下按钮它便开始的小计算程序。从一个开发者的观点来看，那个按钮组件和计算器组件是分别被创建的，并且它们可以一起使用或是在不同的应用程序或情况下和不同的组件产生不同的组合来使用。
当组件或Beans在使用过程中，Bean的性质(比如，一个窗口的背景色)对于其他Bean来说是可见的，并且，之前没“碰到”过的Bean也可以动态地获悉彼此的特性并从而进行交互。　
Bean是随Sun的Bean开发包(BDK)开发出来的，并且能在任何主流操作系统平台的许多应用程序环境(人们所说的“容器”，container)中运行，包括浏览器、文字处理软件、以及一些其他应用。　
要想用JavaBean建一个组件，你必须用Sun的Java编程语言来写程序，并且在程序中包括描述组件特性的JavaBean语句，这些组件特性例如：用户接口的特性，以及触发一个bean和在同一个容器中或网络其他地方的其他的bean交流的事件。
JavaBean给Java应用程序提供了OpenDoc和ActiveX接口已提供的这种复合文档的能力。
3JavaBean的任务

“Write once, run anywhere, reuse everywhere”，即“一次性编写，任何地方执行，任何地方重用”。这个任何实际上就是要解决困扰软件工业的日益增加的复杂性，提供一个简单的、紧凑的和优秀的问题解决方案。
1. 一个开发良好的软件组件应该是一次性地编写，而不需要再重新编写代码以增强或完善功能。因此，JavaBean应该提供一个实际的方法来增强现有代码的利用率，而不再需要在原有代码上重新进行编程。除了在节约开发资源方面的意义外，一次性地编写JavaBean组件也可以在版本控制方面起到非常好的作用。开发者可以不断地对组件进行改进，而不必从头开始编写代码。这样就可以在原有基础上不断提高组件功能，而不会犯相同的错误。
2. JavaBean组件在任意地方运行是指组件可以在任何环境和平台上使用，这可以满足各种交互式平台的需求。由于JavaBean是基于Java的，所以它可以很容易地得到交互式平台的支持。JavaBean组件在任意地方执行不仅是指组件可以在不同的操作平台上运行，还包括在分布式网络环境中运行。
3.JavaBean组件在任意地方的重用说的是它能够在包括应用程序、其他组件、文档、Web站点和应用程序构造器工具的多种方案中再利用。这也许是JavaBean组件的最为重要的任务了，因为它正是JavaBean组件区别于Java程序的特点之一。Java程序的任务就是JavaBean组件所具有的前两个任务，而这第3个任务却是JavaBean组件独有的。
4JavaBean是可复用的平台独立的软件组件

开发者可以在软件构造器工具中其直接进行可视化操作。
软件构造器工具可以是Web页面构造器、可视化应用程序构造器、GUI设计构造器或服务器应用程序构造器。有时，构造器工具也可以是一个包含了一些bean的复合文档的文档编辑器。
5JavaBean可以是简单的GUI要素

如按钮或滚动条；也可以是复杂的可视化软件组件，如数据库视图，有些JavaBean是没有GUI表现形式的，但这些JavaBean仍然可以使用应用程序构造器可视化地进行组合。
一个JavaBean和一个Javaapplet相似，是一个非常简单的遵循某种严格协议的Java类。每个JavaBean的功能都可能不一样，但它们都必须支持以下特征。一个bean没有必须继承的特定的基类或接口。可视化的bean必须继承的类是java.awt.Component，这样它们才能添加到可视化容器中去，非可视化bean则不需要继承这个类。有许多bean，无论是在应用程序构造器工具中，还是在最后创建好的应用程序中，都具有很强的可视化特征，但这并非每个bean必须的特征。
6使用Java编程

在使用Java编程时，并不是所有软件模块都需要转换成bean。Bean比较适合于那些具有可视化操作和定制特性的软件组件。从基本上说，JavaBean可以看成是一个黑盒子，即只需要知道其功能而不必管其内部结构的软件设备。黑盒子只介绍和定义其外部特征和与其他部分的接口，如按钮、窗口、颜色、形状、句柄等。
通过将系统看成使用黑盒子关联起来的通讯网络，我们可以忽略黑盒子内部的系统细节，从而有效地控制系统的整体性能。作为一个黑盒子的模型，JavaBean有3个接口面，可以独立进行开发。
7特点

1. JavaBean可以调用的方法。
2. JavaBean提供的可读写的属性。
3. JavaBean向外部发送的或从外部接收的事件。
8JavaBean设计注意事项

1.不要试图在JavaBean返回的HTML中放置任何字体尺寸。
并不是所有的浏览器都相同。很多浏览器无法处理完整的字体尺寸。
2.不要试图在JavaBean返回的HTML中放置任何脚本或者DHTML。
向页面直接输出脚本或者DHTML相当于自我毁灭，因为某些浏览器版本在处理不正确的脚本时会崩溃（非常少但是有）。如果用户的JavaBean在运行时是动态的推出复杂的HTML语言，用户将陷入调试的噩梦。另外，复杂的HTML将限制JavaBean的寿命和灵活性。
3.不要提供任何的选择。







JavaBean 是一种JAVA语言写成的可重用组件。为写成JavaBean，类必须是具体的和公共的，并且具有无参数的构造器。JavaBeans 通过提供符合一致性设计模式的公共方法将内部域暴露称为属性。众所周知，属性名称符合这种模式，其他Java 类可以通过自省机制发现和操作这些JavaBean 属性。
编辑摘要
用户可以使用JavaBean将功能、处理、值、数据库访问和其他任何可以用java代码创造的对象进行打包，并且其他的开发者可以通过内部的JSP页面、Servlet、其他JavaBean、applet程序或者应用来使用这些对象。用户可以认为JavaBean提供了一种随时随地的复制和粘贴的功能，而不用关心任何改变。
      JavaBean是Sun微系统的一个面向对象的编程接口，它可以让你建可重用应用程序或能在网络中任何主流操作系统平台上配置的程序块，称作组件。像Java applet一样，JavaBeans组件(或“Beans”)能够给予万维网页面交互的能力，例如：计算感兴趣的比率或是根据用户或浏览器的特性改变页面内容。
      从用户的观点来看，一个组件可以是一个与你交互的按钮或是一个当你按下按钮它便开始的小计算程序。从一个开发者的观点来看，那个按钮组件和计算器组件是分别被创建的，并且他们可以一起使用或是在不同的应用程序或情况下和不同的组件产生不同的组合来使用。
      当组件或Beans在使用过程中，Bean的性质(比如，一个窗口的背景色)对于其他Bean来说是可见的，并且，之前没“碰到”过的Bean也可以动态地获悉彼此的特性并从而进行交互。　
      Bean是随Sun的Bean开发包(BDK)开发出来的，并且能在任何主流操作系统平台的许多应用程序环境(人们所说的“容器”，container)中运行，包括浏览器，文字处理软件，以及一些其他应用。　
      要想用JavaBeans建一个组件，你必须用Sun的Java编程语言来写程序，并且在程序中包括描述组件特性的JavaBeans语句，这些组件特性例如：用户接口的特性，以及触发一个bean和在同一个容器中或网络其他地方的其他的bean交流的事件。　　
      Bean也有持续性，持续性就是一种把一个组件的状态存在一个安全处的机制。有了这种持续性，它能使，比如说，一个组件(bean)“记住”某个特定用户在早些时候的用户对话中所输入的数据。　
      JavaBeans给Java应用程序提供了OpenDoc和ActiveX接口已提供的这种复合文档的能力。
一、JavaBean的历史
      最初，JavaBean的目的是为了将可以重复使用的软件代码打包标准。特别是用与帮助厂家开发在综合开发环境（IDE）下使用的java软件部件。这些包括如Grid控件，用户可以将该部件拖放到开发环境中。从此，JavaBean就可以扩展为一个java web 应用的标准部件，并且JavaBean部件框架已经扩展为企业版的 Bean（EJB）。
二、JavaBean和企业Bean的区别
      JavaBean 和 Server Bean（通常称为 Enterprise JavaBean (EJB)）有一些基本相同之处。它们都是用一组特性创建，以执行其特定任务的对??获得其它特性的能力。这使得 bean 的行为根据特定任务和所在环境的不同而有所不同。
      Enterprise Bean 与 JavaBean 不同。JavaBean 是使用 java.beans 包开发的，它是 Java 2 标准版的一部分。JavaBean 是一台机器上同一个地址空间中运行的组件。JavaBean 是进程内组件。Enterprise Bean 是使用 javax.ejb 包开发的，它是标准 JDK 的扩展，是 Java 2 Enterprise Edition 的一部分。Enterprise Bean 是在多台机器上跨几个地址空间运行的组件。因此 Enterprise Bean 是进程间组件。JavaBean 通常用作 GUI 窗口小部件，而 Enterprise Bean 则用作分布式商业对象.

三、JavaBean 的发展
      最初，JavaBean的目的是为了将可以重复使用的软件代码打包标准。特别是用与帮助厂家开发在综合开发环境（IDE）下使用的java软件部件。这些包括如Grid控件，用户可以将该部件拖放到开发环境中。从此，JavaBean就可以扩展为一个java web 应用的标准部件，并且JavaBean部件框架已经扩展为企业版的 Bean（EJB）。
四、JavaBean需求
      avaBean是java类，属于某些特定的译码知道方针，并且扩展了适应性和范围，允许用户访问内部的属性和方法。通过这些，JavaBean类可以用于下列方法：
      1．在IDE中，JavaBean的功能允许应用开发者浏览其中的方法，即使JavaBean是被编译的，并且无法利用原始的源文件。
      2．在 Remote Method Invocation(RMI) 的分布式风格中，这项功能听起来并不让人兴奋，但是在未来的包含企业版的JavaBean后，将改变这种情况。
      3．为了JavaBean的属性值和状态可以保存到磁盘上。
      这里说的有些简单，如果想了解更多的东西，可以查阅一些资料。

五、JavaBean设计注意事项
      实际应用中，在表现对象或者处理前扩展JavaBean的设计非常有用。通常认为如果提供信息，web开发者将在功能上满足拥护对JavaBean的需求。例如： HTML中显示敏感的数据时，用户可以屏蔽的条目，如密码、电话号码等。
      良好规划设计的JavaBean是值得信赖的。
      Java 中的 null 不同于 SQL 中的 null
      看这样一道测试程序：
public class NullTest
{
public static void main(String【】 args)
{
int I = 0;
// int I = null； // not a valid initialization 
String str = null;
String strZeroOutValue = “”;
StringBuffer sb = new StringBuffer(“Null test: String initialized as null = “);
sb.append(str);
sb.append(“n String representing a Zero Out Value:”);
sb.append(strZeroOutValue);
System.out.println(sb.toString());
}
}
      这个程序将产生下面的结果：
Null test: String initialized as null = null
String representing a Zero Out Value:
      在JavaBean中， 我们将 I 变量声明为一个 int， 我们必须处理与该变量相关的值，因为I 默认的没有值，int 类型无法初始化为 null， 如果int 值没有进行明确的初始化，编译器将提示错误。 
执行 NullTest 程序，将验证在文本中空字符串是空值的替代，用于显示 SQL 的插入和更新。如果我们需要删除一些信息，通过删除表单区域的文本，需要将数据库发送长度为0的字符串。
尽管大多数数据库将空字符串作为空值进行操作，如果我们使用的数据库不支持处理空字符串的话，我们必须写入附加的java代码，来创建自己的SQL插入声明。
例如：
if(test.length==0)
{
sb.append(“null”);
}
else
{
sb.append(test);
}
      JavaBean 的范围：

      JavaBean 的范围。 Scope 是一个具有生命时间的变量。JavaBean的范围在
标志中右边进行表示。将产生一个JavaBean的快捷参考。
      说明：jsp服务器引擎将剥离
      存在下面四种范围： 页面、 请求、 对话、 应用。

      对话范围：
      对话范围的JavaBean 主要应用与跨多个页面和时间段： 例如填充 用户信息。 添加信息并且接受回馈，保存用户最近执行页面的轨迹。对话范围JavaBean保留一些和用户对话 ID 相关的信息。这些信息来自临时的对话cookie，并在当用户关闭浏览器时，这个cookie将从客户端和服务器删除。

      页面/请求范围：
      页面和请求范围的JavaBean有时类似表单 的bean ， 这是因为 他们大豆用与处理表单。表单需要很长的时间来处理用户的输入??外页面和请求范围的bean可以用于减少大型站点服务器上的负载，如果使用对话bean，耽搁的处理就可能会消耗掉很多资源。

      应用：
      应用范围通常应用于服务器的部件，例如 JDBC 连接池、应用监视、拥护计数和其他参与用户行为的类。

      在Bean中限制HTML的产生：
      理论上，JavaBean 将不会产生任何HTML，因为这是jsp层负责的工作；然而，为了动态消息提供一些预先准备的格式是非常有用的。产生的HTML将被标注的 JavaBean方法返回。
      这里有一些非常重要的事情：
      1.不要试图在JavaBean返回的HTML中放置任何字体尺寸。
      并不是所有的浏览器都相同。很多浏览器无法处理完整的字体尺寸。 
      2.不要试图在JavaBean返回的HTML中放置任何脚本或者DHTML。
      向页面直接输出脚本或者DHTML相当于自我毁灭，因为某些浏览器版本在处理不正确的脚本时会崩溃（非常少但是有）。如果用户的JavaBean在运行时是动态的推出复杂的HTML语言，用户将陷入调试的噩梦。另外，复杂的HTML将限制JavaBean的寿命和灵活性。
      3.不要提供任何的选择。
      如果用户使用不同的系统浏览页面，可以提供一种可以替换的方法。
六、JavaBean的任务
      JavaBean的任务就是: “Write once, run anywhere, reuse everywhere”，即“一次性编写，任何地方执行，任何地方重用”。这个任何实际上就是要解决困扰软件工业的日益增加的复杂性，提供一个简单的、紧凑的和优秀的问题解决方案。
      1. 一个开发良好的软件组件应该是一次性地编写，而不需要再重新编写代码以增强或完善功能。因此，JavaBean应该提供一个实际的方法来增强现有代码的利用率，而不再需要在原有代码上重新进行编程。除了在节约开发资源方面的意义外，一次性地编写JavaBean组件也可以在版本控制方面起到非常好的作用。开发者可以不断地对组件进行改进，而不必从头开始编写代码。这样就可以在原有基础上不断提高组件功能，而不会犯相同的错误。
      2. JavaBean组件在任意地方运行是指组件可以在任何环境和平台上使用，这可以满足各种交互式平台的需求。由于JavaBean是基于Java的，所以它可以很容易地得到交互式平台的支持。JavaBean组件在任意地方执行不仅是指组件可以在不同的操作平台上运行，还包括在分布式网络环境中运行。
      3.JavaBean组件在任意地方的重用说的是它能够在包括应用程序、其他组件、文档、Web站点和应用程序构造器工具的多种方案中再利用。这也许是JavaBean组件的最为重要的任务了，因为它正是JavaBean组件区别于Java程序的特点之一。Java程序的任务就是JavaBean组件所具有的前两个任务，而这第3个任务却是JavaBean组件独有的。

七、JavaBean的设计目标及其如何被实现
      现在我们来看一实现JavaBean的一些具体的主要设计目标:
      1.紧凑而方便的创建和使用
      JavaBean紧凑性的需求是基于JavaBean组件常常用于分布式计算环境中，这使得JavaBean组件常常需要在有限的带宽连接环境下进行传输。显然，为了适应传送的效率和速度，JavaBean组件必须是越紧凑越好。另外，为了更好地创建和使用组件，就应该使其越简单越好。通常为了提高组件的简易性和紧凑性，设计过程需要投入相对较大的功夫。
      现在已有的组件软件技术通常是使用复杂的API，这常常搞得开发者在创建组件时晕头转向。因此，JavaBean组件必须不仅容易使用，而且必须便于开发。这对于组件开发者而言是至关重要的，因为这可以使得开发者不必花大量功夫在使用API进行程序设计上，从而更好地对组件进行润饰，提高组件的可观赏性。
      JavaBean组件大部分是基于已有的传统Java编程的类结构上的，这对于那些已经可以熟练地使用Java语言的开发者非常有利。而且这可以使得JavaBean组件更加紧凑，因为Java语言在编程上吸收了以前的编程语言中的大量优点，已经使开发出来的程序变得相当有效率。
      2.完全的可移植性
      JavaBean API与操作基础的独立于平台的Java系统相结合，提供了独立于平台的组件解决方案。因此，组件开发者就可以不必再为带有Java applet平台特有的类库而担心了。最终的结果都将是计算机界共享可重复使用的组件，并在任何支持Java的系统中无需修改地执行。
      3.继承Java的强大功能
      现有的Java结构已经提供了多种易于应用于组件的功能。其中一个比较重要的是Java本身的内置类发现功能，它可以使得对象在运行时彼此动态地交互作用，这样对象就可以从开发系统或其开发历史中独立出来。
      对于JavaBean而言，由于它是基于Java语言的，所以它就自然地继承了这个对于组件技术而言非常重要的功能，而不再需要任何额外开销来支持它。
      JavaBean继承在现有Java功能中还有一个重要的方面，就是持久性，它保存对象并获得对象的内部状态。通过Java提供的序列化(serialization)机制，持久性可以由JavaBean自动进行处理。当然，在需要的时候，开发者也可以自己建立定制的持久性方案。
      4.应用程序构造器支持
      JavaBean的另一个设计目标是设计环境的问题和开发者如何使用JavaBean创建应用程序。JavaBean体系结构支持指定设计环境属性和编辑机制以便于JavaBean组件的可视化编辑。这样开发者可以使用可视化应用程序构造器无缝地组装和修改JavaBean组件。就像Windows平台上的可视化开发工具VBX或OCX控件处理组件一样。通过这种方法，组件开发者可以指定在开发环境中使用和操作组件的方法。
      5.分布式计算支持
      支持分布式计算虽然不是JavaBean体系结构中的核心元素，但也是JavaBean中的一个主要问题。
      JavaBean使得开发者可以在任何时候使用分布式计算机制，但不使用分布式计算的核心支持来给自己增加额外负担。这正是出于JavaBean组件的紧凑性考虑的，无疑分布式计算需要大量的额外开销。

八、JavaBean和Java
      虽然JavaBean和Java之间已经有了明确的界限，但在某些方面JavaBean和Java之间仍然存在着非常明显的混淆。Java确实是能够为用户创建可重用的对象，但它却没有管理这些对象相互作用的规则或标准。JavaBean通过指定定义对象之间交互作用的机制，以及大部分对象需要支持的常用行为，如持久性和实际处理等，建立了自己需要的组件模型。
      虽然当前的Java组件模型也可以运行得很好，但在传送真正的可重用性和交互操作性上仍然非常有限，Java用户需要做的最多的一件事就是创建applet并使得它们在Web 页面上相互通讯，这并非易事。JavaBean提供了一个框架包，使用这个包进行通讯就容易得多了。
      JavaBean组件能够通过定义好的标准属性改进性能。总体而言，JavaBean充分发展了Java applet的功能，并结合了Java AWT组件的紧凑性和可重用性。

九、JavaBean组件的基本概念
      JavaBean是可复用的平台独立的软件组件，开发者可以在软件构造器工具中其直接进行可视化操作。
      软件构造器工具可以是Web页面构造器、可视化应用程序构造器、CUI设计构造器或服务器应用程序构造器。有时，构造器工具也可以是一个包含子一些bean的复合文档的文档编辑器。
      JavaBean可以是简单的CUI要素，如按钮或滚动条；也可以是复杂的可视化软件组件，如数据库视图，有些JavaBean是没有GUI表现形式的，但这些JavaBean仍然可以使用应用程序构造器可视化地进行组合。
      一个JavaBean和一个Javaapplet相似，是一个非常简单的遵循某种严格协议的Java类。每个JavaBean的功能都可能不一样，但它们都必须支持以下特征。
      一个bean没有必须继承的特定的基类或接口。可视化的bean必须继承的类是java.awt.Component，这样它们才能添加到可视化容器中去，非可视化bean则不需要继承这个类。有许多bean，无论是在应用程序构造器工具中，还是在最后创建好的应用程序中，都具有很强的可视化特征，但这并非每个bean必须的特征。
      在使用Java编程时，并不是所有软件模块都需要转换成bean。Bean比较适合于那些具有可视化操作和定制特性的软件组件。
      从基本上说，JavaBean可以看成是一个黑盒子，即只需要知道其功能而不必管其内部结构的软件设备。黑盒子只介绍和定义其外部特征和与其他部分的接口，如按钮、窗口、颜色、形状、句柄等。
      通过将系统看成使用黑盒子关联起来的通讯网络，我们可以忽略黑盒子内部的系统细节，从而有效地控制系统的整体性能。作为一个黑盒子的模型，JavaBean有3个接口面，可以独立进行开发。
      1. JavaBean可以调用的方法。
      2. JavaBean提供的可读写的属性。
      3. JavaBean向外部发送的或从外部接收的事件。

九、JavaBean组件的开发环境

      普通JavaBean组件是要分布在各自环境中，所以它们应该能够适应各种环境。虽然我们无法事先预知JavaBean要运行的确切环境，但以下两点是可以确定的：
      1. bean必须能够在一个应用程序构造器工具中运行。
      2. bean必须可以在产生的应用程序的运行环境中使用。
      设计环境
      第一点说明的是bean必须可以在设计环境(design environment)中运行。在设计环境中，bean应该提供设计信息给应用程序构造器工具并允许终端用户制定bean的外　　观和行为。
在传统的软件构造活动中，必须通过编译、链接之后才能看到应用程序的最终运行结果；而利用JavaBean设计的软件中，则没有这种明确的界限。使用JavaBean，就可以非常直观地设计应用程序软件，在设计过程中赋予软件生机。而且，这个过程更加容易重复开发，设计思想更加容易变成原型。
      运行环境
      第二点说明的是bean必须可以在运行环境(run-time environment)中使用。在这个环境中，对设计信息和定制的需求并不重要。一个组件的设计环境信息和设计环境中编写的代码通常可能是非常巨大的。
      因此，我们可能需要在bean的设计环境方面和运行环境方面作一个明确的区分，这样，就可能需要在运行环境中不使用bean的任何设计环境代码来配置这个bean。所以，JavaBean就必须分别支持运行环境接口的类库和设计环境接口的类库。







一、 javabean 是什么？

Bean的中文含义是“豆子”，顾名思义，JavaBean是指一段特殊的Java类，

就是有默然构造方法,只有get,set的方法的java类的对象.

 

专业点解释是：

JavaBean定义了一组规则
JavaBean就是遵循此规则的平常的Java对象 

 

满足这三个条件:  
   1.执行java.io.Serializable 接口 
　2.提供无参数的构造器 
  3.提供getter 和 setter方法访问它的属性.

 

简单地说，JavaBean是用Java语言描述的软件组件模型，其实际上是一个类。这些类遵循一个接口格式，以便于使函数命名、底层行为以及继承或实现的行为，可以把类看作标准的JavaBean组件进行构造和应用。

JavaBean一般分为可视化组件和非可视化组件两种。可视化组件可以是简单的GUI元素，如按钮或文本框，也可以是复杂的，如报表组件；非可视化组件没有GUI表现形式，用于封装业务逻辑、数据库操作等。其最大的优点在于可以实现代码的可重用性。JavaBean又同时具有以下特性。

*     易于维护、使用、编写。

*     可实现代码的重用性。

*     可移植性强，但仅限于Java工作平台。

*     便于传输，不限于本地还是网络。

*     可以以其他部件的模式进行工作。

对于有过其他语言编程经验的读者，可以将其看作类似微软的ActiveX的编程组件。但是区别在于JavaBean是跨平台的，而ActiveX组件则仅局限于Windows系统。总之，JavaBean比较适合于那些需要跨平台的、并具有可视化操作和定制特性的软件组件。

 

JavaBean组件与EJB（Enterprise JavaBean，企业级JavaBean）组件完全不同。EJB 是J2EE的核心，是一个用来创建分布式应用、服务器端以及基于Java应用的功能强大的组件模型。JavaBean组件主要用于存储状态信息，而EJB组件可以存储业务逻辑。
2  使用JavaBean的原因
程序中往往有重复使用的段落，JavaBean就是为了能够重复使用而设计的程序段落，而且这些段落并不只服务于某一个程序，而且每个JavaBean都具有特定功能，当需要这个功能的时候就可以调用相应的JavaBean。从这个意义上来讲，JavaBean大大简化了程序的设计过程，也方便了其他程序的重复使用。

JavaBean传统应用于可视化领域，如AWT（窗口工具集）下的应用。而现在，JavaBean更多地应用于非可视化领域，同时，JavaBean在服务器端的应用也表现出强大的优势。非可视化的JavaBean可以很好地实现业务逻辑、控制逻辑和显示页面的分离，现在多用于后台处理，使得系统具有更好的健壮性和灵活性。JSP + JavaBean和JSP + JavaBean + Servlet成为当前开发Web应用的主流模式。

3  JavaBean的开发

在程序设计的过程中，JavaBean不是独立的。为了能够更好地封装事务逻辑、数据库操作而便于实现业务逻辑和前台程序的分离，操作的过程往往是先开发需要的JavaBean，再在适当的时候进行调用。但一个完整有效的JavaBean必然会包含一个属性，伴随若干个get/set（只读/只写）函数的变量来设计和运行的。JavaBean作为一个特殊的类，具有自己独有的特性。应该注意以下3个方面。

*     JavaBean类必须有一个没有参数的构造函数。

*     JavaBean类所有的属性最好定义为私有的。

*     JavaBean类中定义函数setXxx() 和getXxx()来对属性进行操作。其中Xxx是首字母大写的私有变量名称。




# EJB
# Spring Bean

Spring 的 Bean
Bean 是 Spring 装配的组件模型，一切实体类都可以配置成一个 Bean ，进而就可以在任何其他的 Bean 中使用，一个 Bean 也可以不是指定的实体类，这就是抽象 Bean 。
在 Spring 中有两个最基本、最重要的包，即 org.springframework.beans 和 org.springframework.context ，在这两个包中，为了实现无侵入式的框架，代码中大量地使用了 Java 中的反射机制，通过动态调用来避免硬编码，为 Spring 反向控制提供了基础保证，在这两个包中，最重要的类时 BeanFactory 和 ApplicationContext ， BeanFactory 提供一种先进的配置机制来管理任何种类的 Bean ， ApplicationContext 是建立在 BeanFactory 之上的，并增加了其他功能，例如，国际化的支持、资源的访问和事件传播等。
Bean 的标识 (id 和 name)
Id 属性具有唯一性，每一个 Bean 只能有一个对应的 id,name 属性可以指定一个或者多个名称，各个名称之间用逗号或者分号隔开，第一个默认为标识名称，后面的多个自动成为这个 Bean 的别名。
Bean 的 class属性
在 Spring 配置文件中 class 属性指明 Bean 的来源，也就是 Bean 的实际路径，它指向一个实体类。
Bean 的作用域
在 Spring 中可以直接在配置文件中指定类的作用域， scope 标识 Bean 的作用域。
在 Spring2.0 之前 Bean 只有两种作用域，即 Singleton( 单例 ) 和 non-Singleton( 也称 prototype) ， Spring2.0 以后，增加了 session 、 request 和 global session 三个专用于 Web 应用程序上下文的 Bean 。
singleton 作用域
         当一个 Bean 的作用域设置为 Singleton ，那么 Spring IOC 容器中只存在一个共享的 Bean 实例，并且所有对 Bean 的请求，只要 id 与该 bean 定义相匹配，则只会返回 bean 的同一个实例。这个单一实例会被存储到单例缓存 (singleton cache) 中，并且所有针对该 bean 的后续请求和引用都将返回被缓存的对象实例。
       prototype
prototype 的作用域部署的 Bean ，每一个请求都会产生一个新的 Bean 实例，相当于一个 new 的操作，对于 prototype 作用域的 bean ，有一点非常重要，那就是 Spring 不能对一个 prototype 的整个生命周期复杂，容器在初始化、配置、装饰或者是装配完一个 prototype 实例后，将它交给客户端，随后就对该 prototype 实例不负责了。
request
request 表示针对每一个 HTTP 请求都会产生一个新的 Bean ，同时该 Bean 仅在当前 HTTP Request 内有效。
session
session 作用域表示针对在一个 Http 请求都会产生一个新的 Bean ，同时该 Bean 仅在当前 Http session 范围内有效。
global session
       global session 作用域类似于标准的 HTTP Session 作用域。
Bean 的生命周期
一个 Bean 从建立到销毁，会历经几个执行阶段，如果使用 BeanFactory 来生成、管理 Bean ，会尽量支持一下的生命周期。
Bean 的建立
由 BeanFactory 读取 Bean 的定义文件，并生成各个 Bean 的实例。
属性注入
执行相关的 Bean 属性依赖注入
BeanNameAware 的 setBeanName()
         如果 Bean 类有实现 org.springframework.beans.factory.BeanNameAware 接口，则执行它的 setBeanName() 方法。
      BeanFactoryAware 的 setBeanFactory()
如果 Bean 类实现 org.springframework.beans.factory.BeanFactoryAware 接口，则执行它的 setBeanFactory() 方法。
BeanPostProcessors 的 processBeforeInitialization()
如果有任何的 org.springframework.beans.factory.config.BeanPostProcessor 实例与 Bean 实例相关联，则执行 BeanPostProcessor 实例的 processBeforeInitialization() 。
InitializingBean 的 afterPropertiesSet()
如果 Bean 类有实现 org.springframework.beans.factory.InitializingBean ，则执行它的 afterPropertiesSet() 方法。
Bean 定义文件中定义 init-method
       可以在 Bean 定义文件使用 ”init-method” 属性设置方法名称。
       BeanPostProcessors 的 processAfterInitialization()
如果有任何的 org.springframework.beans.factory.config.BeanPostProcessor 实例与 Bean 实例相关联，则执行 BeanPostProcessor 实例的 processAfterInitialization() 。
DisposableBean 的 destroy()
在容器关闭时，如果 Bean 类有实现 org.springframework.beans.factory.DisposableBean 接口，则执行它的 destroy() 方法。
Bean 定义文件中定义 destroy –method
在容器关闭时，可以在 Bean 定义文件使用 ” destroy –method ” 属性设置方法名称。
    FactoryBean
Spring 中有两种类型的 Bean ，一种是普通的 Bean ，普通的 Bean 可以是用户定义的任何类；另一种是工厂 Bean ，即 FactoryBean 。工厂 Bean 与普通的 Bean 不同，其返回的对象不是指定类的一个实例，其返回的是该工厂 Bean 的 getObject 方法返回的对象。在 Spring 框架内部， AOP 相关的功能及事务处理中，很多方法使用到工厂 Bean 。
BeanPostProcessor
         在 Bean 的依赖关系由 Spring 容器建立并设置以后，你还有机会定义一些 Bean 的修正动作来修正相关的属性，方法是让 Bean 类实现 org.springframework.beans.factory.config.BeanPostProcessor 接口，该接口与 Spring 中的定义如下：
 
Java代码  收藏代码
public interface BeanPostProcessor {  
    Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException;  
    Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException;  
}  
 
    postProcessBeforeInitialization 方法会在 Bean 类被初始化之前 ( 例如 InitializingBean 的 afterPropertiesSet() 方法或者自定义的 init 方法 ) 被执行，而 postProcessAfterInitialization() 方法会在 Bean 类被初始化之后立即被执行。






# OSGI
