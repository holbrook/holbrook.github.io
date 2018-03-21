---
layout: post
title: "Eclipse e4 概览"
description: "尽管至今为止，仍然处于孵化器阶段(Incubation Phase)，但是e4代表了Eclipse的未来。e4提供的新特性包括：
基于EMF的应用模型(Application Model)；依赖注入；基于CSS定义外观"
category: 软件开发
tags: [OSGi]
lastmod: 
---

尽管至今为止，[Eclipse e4](http://www.eclipse.org/e4/)仍然处于孵化器阶段(Incubation Phase)，但是e4代表了Eclipse的未来。

e4是位于底层的Equinox、EMF、SWT/JFace和上层的Eclipse应用(Plugin、RCP、RAP等)之间的一个应用开发平台。
从RCP的角度来说，e4的一个主要目标就是更轻松地编写和重用组件。
为了实现这个目标，与之前的Eclipse平台相比，e4带来的新特性主要包括：

- 基于EMF的应用模型(Application Model)
- 依赖注入
- 基于CSS定义外观

# 快速开始

需要的环境和工具包括：

- Java >= 1.7
- Eclipse >= 4.3
- [Enide - Eclipse bootstrap e4](https://marketplace.eclipse.org/content/enide-eclipse-boostrap-e4)
- [WindowBuilder](http://www.eclipse.org/windowbuilder/)

安装了Eclipse bootstrap e4插件之后，可以创建Eclipse 4 --> Eclipse 4 Application Project。

生成的目录结构如下：

![](/images/e4/e4_project.png)

其中，`*.product`文件是Eclipse插件项目的产品配置文件，可以以“E4Application”的方式运行：

![](/images/e4/e4_product.png)

在`*.product`文件上右键-->Run As-->Eclipse Application，就可以启动一个e4应用：

![](/images/e4/e4_application.png)

整个工程可以导出(Export)为"Eclipse Product"，称为一个可以脱离Eclipse独立运行的、跨平台的RCP应用。


# 应用模型

好吧，到目前为止，e4所表现出来的功能与Eclipse 3.x相比没什么区别。但是请关注一下上面生成的`Application.e4xmi`文件。
该文件是e4中的应用模型文件。

在 Eclipse 平台 UI 的早期版本中，workbench 被显式地硬编码来布局 workbench 窗口、workbench 页面、编辑器区域或视图堆栈。e4 引入了额外的一层，可将UI元素提取和抽象成一个模型。应用程序可以重新配置或扩展这个模型来制作不同的外观。这个模型也可被动态操纵；模型的改变可以立即反映出 UI 的变化。

e4的模型的特性为：

- 基于抽象描述
- 可以在运行时(runtime)更改
- 支持扩展

## 抽象描述

e4的应用模型基于抽象描述——应用模型只定义了需要哪些组件，而不关注这些组件是如何实现的。e4应用模型实现了应用模型和实际视图(Views)的分离。

由于应用模型没有绑定的具体实现，这意味着一种可能：同一个应用模型可以用各种界面技术（如SWT/JFace, Swing甚至web，Flash）来实现。


模型中即描述了可视的组件，如 windows, parts (views 和 editors), menus, toolbars等，也可以描述非可视化组件如handlers, commands , key bindings等。所有能够在模型中描述的组件（包括可视化组件和非可视化组件），都实现了MApplicationElement接口，如下图：

![](/images/e4/e4_MApplicationElement.png)


用Eclipse 4 model editor打开`Application.e4xmi`，可以看到如下的视图：

![](/images/e4/e4_app_model.png)

`Application.e4xmi`是基于EMF定义的。其定义文件(.ecore）位于 org.eclipse.e4.ui.model.workbench 插件的model文件夹中。

## 常用的可视化组件

e4中的可视化组件描述类都来自`MUIElement`，该接口当然也继承了`MApplicationElement`接口。
常用的可视化组件包括：


- Window

  窗口。一个Eclipse 应用可以包含一个或多个窗口。

  ![](/images/e4/elements/window.png)

- Parts

  e4中不区分Views和editors，而是统一定义为Parts。Part能够放置在用户界面的任何位置，每个Part可以有自己的菜单、工具条，可以出来自己的模型数据。

  ![](/images/e4/elements/part.png)


- Perspective

  Perspective是Parts的容器，可以管理内部Part的布局。一个应用可以有多个不同的Perspective(不能同时出现)，以适应不同的应用场景。
  比如，Eclipse IDE提供了Java、Java EE、Debug等Perspective。

  在应用模型中，为了管理方便，还可以将Perspective放置到Perspective Stack中。

- PartStack 和 PartSashContainer

  Part可以直接用于Window或Perspective中，也可以将其分组。使用PartStack 和 PartSashContainer可以实现Part的分组和布局管理。

  PartStack可以容纳多个Part，每次只能显示其中一个Part，以页签(tab)的形式进行切换，而PartSashContainer以水平或竖直布局的方式同时显示多个Part。如下图：

  ![](/images/e4/elements/partstack.png)

  通过PartStack和PartSashContainer的组合，能够创建出非常复杂的布局：

  ![](/images/e4/elements/partsashcontainer.png)

  PartStack 和 PartSashContainer中的子组件，可以设置“容器数据(Container Data)”，作为决定自己在容器中布局的参数。

  ![](/images/e4/elements/containerdata.png)

  需要注意的是，容器中的所有元素要么都设置容器数据，要么都不设置，否则会出现异常。


# 依赖注入

基于上一节的内容，我们可以脱离UI组件的实现，直接定义出应用模型。

同样的，当我们实现一个UI组件的时候，也完全无需考虑应用模型的存在。在e4中，View甚至无需实现任何接口，而是通过依赖注入的方式获取UI组件的上下文环境。可以使用[JSR330](/2013/12/31/jsr330.html)中定义的`@Inject`注解，也可以使用e4的`org.eclipse.e4.ui.di`包中定义的`@Focus`、`@Persist`等注解。比如：

```
public class SamplePart {
	private Text txtInput;
	private TableViewer tableViewer;

	@Inject
	private MDirtyable dirty;

	@PostConstruct
	public void createComposite(Composite parent) {
		parent.setLayout(new GridLayout(1, false));

		txtInput = new Text(parent, SWT.BORDER);
		txtInput.setMessage("Enter text to mark part as dirty");
		txtInput.addModifyListener(new ModifyListener() {
			@Override
			public void modifyText(ModifyEvent e) {
				dirty.setDirty(true);
			}
		});
		txtInput.setLayoutData(new GridData(GridData.FILL_HORIZONTAL));

		tableViewer = new TableViewer(parent);

		tableViewer.add("Sample item 1");
		tableViewer.add("Sample item 2");
		tableViewer.add("Sample item 3");
		tableViewer.add("Sample item 4");
		tableViewer.add("Sample item 5");
		tableViewer.getTable().setLayoutData(new GridData(GridData.FILL_BOTH));
	}

	@Focus
	public void setFocus() {
		tableViewer.getTable().setFocus();
	}

	@Persist
	public void save() {
		dirty.setDirty(false);
	}
}
```

由于UI组件与应用模型完全解耦，可以对UI组件单独进行测试：


```
public static void main(String[] args) {
	Display display = new Display();
	  Shell shell = new Shell(display);
	  shell.setLayout(new FillLayout());
	  SamplePart part = new SamplePart();
	  part.createComposite(shell);
	  shell.open();
	  while( !shell.isDisposed() ) {
	      if( ! display.readAndDispatch() ) {
	        display.sleep();
	      }
	  }
}
```	

# 向模型注入资源

前面两节分别介绍了创建应用模型和UI组件，接下来就是将二者结合起来。

在应用模型中，使用URI注入外部资源。比如，一个Part的Icon、Class都是通过URI注入的。这些资源是延迟加载(lazy loaded)的——只有显示某个可视化组件时，才加载其需要的资源。

模型使用的资源即可以在运行时注入或更改，也可以在Eclipse 4 model editor中指定初始的资源：

![](/images/e4/e4_app_model.png)

任何形式的URI都可以作为资源使用。比如：`http://thinkinside.tk/assets/ico/favicon.png`。

对于Eclipse的插件环境，可以使用应用模型所在的插件(bundle)或来自其他插件的资源，分别使用

  `bundleclass://Bundle-SymbolicName/ package.classname` 和 

  `platform:/plugin/Bundle-SymbolicName/ path/filename.extension`的形式。

比如：

```
bundleclass://tangle-app/parts.SamplePart

platform:/plugin/test/icons/save_edit.gif
```
  







# 定义行为

e4的应用模型中，通过`Handler`定义行为。可视化组件和`Handler`之间通过`Command`关联。

与GUI组件一样，Handler的定义和实现也是分离的。在应用模型中定义的`Handler`通过Class URI关联到具体的实现类。我们可以单独编写一个`Handler`，无需实现任何接口：

```
public class MyHandler {
	@Execute
	public void execute(Shell shell) {
		MessageDialog.openInformation(shell, "", "Hello World!");
	}
	
	
	@CanExecute
	public boolean canExecute() {
		
		return true;
	}
		
}
```

其中，`canExecute()`方法是可选的。该方法定义了`execute()`方法是否可以被执行的一个开关。

由于`Handler`与应用模型完全解耦，可以单独对`Handler`进行测试：

```
public static void main(String[] args) {
  Display display = new Display();
  Shell shell = new Shell(display);
  shell.open();
  MyHandler.execute(shell);
  while( !shell.isDisposed() ) {
      if( ! display.readAndDispatch() ) {
        display.sleep();
      }
  }
}
```

最简单的事件处理是菜单/工具条的处理。使用模型编辑器，可以在图形界面中很容易的将`Handler`和菜单项都关联到同一个`Commnad`，
即实现了行为的定义。这里不做截图，定义好的`Application.e4xmi`中相关内容可能是：

```
	<!--定义一个Command-->
	<commands xmi:id="_4mWoMHcyEeOYmvSF-9z33Q" elementId="holbrook.tangle.demo.myCommand" commandName="测试Cmd"/>

	<!--定义一个Handler，并关联到Command-->
	<handlers xmi:id="_J-fYsHczEeOYmvSF-9z33Q" elementId="holbrook.tangle.demo.myHandler" contributionURI="bundleclass://tangle-app/handlers.MyHandler" command="_4mWoMHcyEeOYmvSF-9z33Q"/>
	
	<!--定义一个菜单项，也关联到Command-->
	<mainMenu xmi:id="_FfY8UHbUEeOYmvSF-9z33Q" elementId="tangle-app.menu.0">
      <children xsi:type="menu:Menu" xmi:id="_OwboQHc0EeOYmvSF-9z33Q" elementId="tangle-app.menu.1" label="测试菜单">
        <children xsi:type="menu:HandledMenuItem" xmi:id="_TwOjEHc0EeOYmvSF-9z33Q" elementId="tangle-app.handledmenuitem.0" label="测试Cmd" command="_4mWoMHcyEeOYmvSF-9z33Q"/>
      </children>
    </mainMenu>
```



# CSS样式

e4将桌面应用和Web应用的一些特性融合在了一起，比如，可以通过CSS定义桌面应用的外观。

使用Eclipse bootstrap e4创建的Eclipse 4 Application Project，会包含一个`css/default.css`的空文件。
编辑这个文件就可以修改应用的外观。

在e4中，CSS选择器使用`type#id.class`的格式。其中：

- type：对应SWT组件类（如Button、Composite等）
- id：对应应用模型中的`elementId`

一些映射关系可以参考[这里](http://wiki.eclipse.org/E4/CSS/SWT_Mapping)

下面是一个CSS的例子：

```
Text {
    font: Verdana 15px;
    color: red;
    background-color: green;
}
```

默认情况下，该CSS就会生效。因为在`plugin.xml`中，已经指定了CSS的扩展点：

![](/images/e4e4_css_extension.png)

更灵活的使用CSS是通过主题管理器。

