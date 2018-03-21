---
layout: post
title: "Eclipse e4中的平台服务"
description: ""
category: 软件开发
tags: [OSGi]
lastmod: 
---


# 概述

[前面](/2014/01/12/dependency_injection_in_e4.html)提到，e4中可以通过依赖注入进行服务的发布和获取。并且，”在Eclipse e4中，将全局的上下文分成了多个层次“：

![](/images/e4/e4_context_hierarchy.png)

e4提供了很多平台级的服务，注册于OSGi context之上的其他各个context层。这些服务提供了开发应用的很多通用的功能。一些常用的服务包括：

展现层MVC的视图、模型、控制器相关的服务，以及逻辑层服务。


+ 视图相关服务

  - EPartService

  	访问和修改Part，使用Part模板，切换perspectives，支持Edit方法

  - ESelectionService

    处理GUI界面中的”选中“

  - EMenuService

    Registers a popup menu (MPopupMenu) for an SWT control.

  - org.eclipse.jface.window.IShellProvider

    在SWT环境中访问Shell

  - IThemeEngine	

    Allows to switch the styling of the application at runtime.
  

+ 模型相关服务
  - EModelService

    在运行时访问或更改e4的[应用模型](/2014/01/07/eclipse_e4_RCP_quickstart.html#menuIndex1)


+ 控制器相关服务
  - MDirtyable

    用于标记Part中的内容是否被修改过

  - ECommandService

    访问、创建和更改应用模型中的command对象

  - EHandlerService

  	访问、更改或触发(trigger)应用模型中的handler对象


+ 逻辑层相关服务

  - IEventBroker

    提供基于发布、订阅机制的事件处理功能

  - StatusReporter	 

    Allows you to report Status objects.

  - EContextService	 

    Activate and deactivate key bindings defined as BindingContext in the application model. The content referred to in this service is the BindingContext and not the IEclipseContext.

  - Logger 

    `org.eclipse.e4.core.services`插件中的`Logger`提供了日志功能

  - Adapter 

    An adapter can adapt an object to the specified type, allowing clients to request domain-specific behavior for an object. It integrates IAdaptable and IAdapterManager


# 视图相关服务

## EPartService

在应用模型中，可以定义PartDescriptors。PartDescriptors可以作为创建Part的模板。

![](/images/e4/PartDescriptors.png)

通过EPartService可以访问这些模板，比如：

```

  @Inject private EPartService partService;
  
  // Showing and hiding parts
  detailsTodoPart = partService.findPart("com.example.todo.rcp.parts.tododetails");
  partService.hidePart(detailsTodoPart);
  ……
  detailsTodoPart.setVisible(true);
  partService.showPart(detailsTodoPart, PartState.VISIBLE); 
  
  //Switching perspectives
  @Execute
    public void execute(MApplication app, EPartService partService, 
        EModelService modelService) {
      MPerspective element = 
          (MPerspective) modelService.find("secondperspective", app);
      // now switch perspective
      partService.switchPerspective(element);
    }
  
  
  // creating parts dynamically
  @Execute
    public void execute(EPartService partService) {
      
      // create a new Part based on a PartDescriptor
      // in the application model 
      // assume the ID is used for the PartDescriptor
      MPart part = partService
          .createPart("com.example.e4.rcp.todo.partdescriptor.fileeditor");
      part.setLabel("New Dynamic Part");
      
      // If multiple parts of this type are now allowed 
      // in the application model, 
      // then the provided part will be shown 
      // and returned
      partService.showPart(part, PartState.ACTIVATE);
    }
  
  //switch perspective
  @Execute
    public void execute(MApplication app, EPartService partService, 
        EModelService modelService) {
      MPerspective element = 
          (MPerspective) modelService.find("secondperspective", app);
      partService.switchPerspective(element);
    }
```
  




## ESelectionService

e4的应用模型中，MWindow对象可以保持选中的Part。e4在IEclipseContext中注册了`ESelectionService`，可以设置或获取选中的组件。

使用`setSelection()`方法可以设置选中状态：

```
  // use field injection for the service
  @Inject ESelectionService selectionService;
  
  // viewer is a JFace Viewer
  viewer.addSelectionChangedListener(new ISelectionChangedListener() {
    @Override
    public void selectionChanged(SelectionChangedEvent event) {
      IStructuredSelection selection = (IStructuredSelection) 
          viewer.getSelection();
      selectionService.setSelection(selection.getFirstElement());
    }
  }); 

```


使用` getSelection(partId)`方法可以获取选中的组件，更常用的做法是使用`IServiceConstants.ACTIVE_SELECTION`作为`@Named`注解的参数，自动注入选中的组件：

```
  @Inject
  public void setTodo(@Optional 
      @Named(IServiceConstants.ACTIVE_SELECTION) Todo todo) {
    if (todo != null) {
      // do something with the value
    }
  } 
```


# 模型相关服务EModelService

使用`EModelService`可以在运行时访问或更改e4的[应用模型](/2014/01/07/eclipse_e4_RCP_quickstart.html#menuIndex1)，比如增加或删除模型元素。EModelService中一些常用的方法包括：

- `cloneElement()`和`cloneSnippet()`：克隆元素或模型片段
- `findElements()`：通过ID、类型、或标签(tags)搜索元素

使用举例：

```
  //search by type
    private void findParts(MApplication application,
        EModelService service) {
      List<MPart> parts = service.findElements(application, null,
          MPart.class, null);
      System.out.println("Found parts(s) : " + parts.size());
  
    }
  
  //Dynamically create a new window
  MWindow window = modelService.createModelElement(MWindow.class);
  window.setWidth(200);
  window.setHeight(300);
  
  // add new Window to the application
  application.getChildren().add(window); 

```

# 控制器相关服务
## MDirtyable和@Persist注解

   e4中不再区分ViewPart和EditPart，而是统一使用Part。通过MDirtyable可以标记Part中的内容是否被修改过；使用`@Persist`注解可以标记持久化Part内容的方法。比如：

```
  public class MyEditPart {
  
    @Inject
    MDirtyable dirty;
  
    @PostConstruct
    public void createControls(Composite parent) {
      Button button = new Button(parent, SWT.PUSH);
      button.addSelectionListener(new SelectionAdapter() {
        @Override
        public void widgetSelected(SelectionEvent e) {
          dirty.setDirty(true);
        }
      });
    }
  
    @Persist
    public void save(MDirtyable dirty, ITodoService todoService) {
      // save changes via ITodoService for example
      todoService.saveTodo(todo);
      // save was successful
      dirty.setDirty(false);
    } 
  } 
```

在上面的例子中，看起来`@Persist`注解没有多大用处。其实，该注解主要用于EPartService的`saveAll()`方法：

```
  public class SaveHandler {
  
    @Execute
    void execute(EPartService partService) {
      partService.saveAll(false);
    }
  } 
```

## ECommandService和EHandlerService

举例如下：

```
  Command command = commandService.getCommand("com.example.mycommand");
  
  // check if the command is defined
  System.out.println(command.isDefined());
  
  // activate Handler, assume AboutHandler() class exists already
  handlerService.activateHandler("com.example.mycommand", 
      new AboutHandler());
  
  ParameterizedCommand cmd =
    commandService.createCommand("com.example.mycommand", null);
  
  // check if the command can get executed
  System.out.println(handlerService.canExecute(cmd));
  
  // execute the command
  handlerService.executeHandler(cmd); 
```


# 逻辑层相关服务

## IEventBroker

Eclipse 3.x中，事件处理使用Observer模式：事件接收者实现事件发布者指定的Listener接口，并注册到事件发布者。
这带来两个问题：

- 一个Listener接口要写很多个实现，这些实现中的代码有重复
- 事件发布者和接收者的生命周期紧耦合

Eclipse e4中，将OSGi的`EventAdmin`API封装为事件服务，提供了基于发布、订阅机制的事件处理功能：`EventBroker`作为事件总线，通过`EventBroker`可以发布和订阅事件。

要使用e4事件服务，需要增加依赖插件：
    * org.eclipse.e4.core.services
    * org.eclipse.osgi.services


- 获取EventBroker

e4中定义了`org.eclipse.e4.core.services.events.IEventBroker`接口，可以通过依赖注入、e4上下文等方式获取：

```
  @Inject
  IEventBroker eventBroker;

  @Inject
  private IEclipseContext eclipseContext;
  ……
  IEventBroker eventBroker = eclipseContext.get(IEventBroker.class);

- 发布事件

可以用`IEventBroker`的`post()`或`send()`方法，进行同步(synchronous)或异步(asynchronous)事件的发布：

```
  boolean IEventBroker.post(String topic, Object data) // synchronous delivery

  boolean IEventBroker.send(String topic, Object data) // asynchronous delivery

```

返回值为是否发生成功。


- 订阅事件

可以通过依赖注入或者`IEventBroker`的`subscribe()`方法订阅事件：

```
  @Inject 
  @Optional
  private void closeHandler(@UIEventTopic(''TOPIC_STRING'') foo.Bar payload) {    
    //do something with payload 
  }
```

```
  @Inject
  IEventBroker eventBroker;

  org.osgi.service.event.EventHandler closeHandler = new EventHandler() { 
    public void handleEvent(Event event) { 
        foo.Bar payload = (foo.Bar) event.getProperty(IEventBroker.DATA);
    }
  }

  eventBroker.subscribe(TOPIC_STRING, closeHandler);
  ……
  eventBroker.unsubscribe(closeHandler);
```

消息对象(payload)作为附件存储在`IEventBroker.DATA`属性中。对于`Dictionary`或`Map`等集合类型的消息，会将其中所有的值按照KEY添加为属性。

## Logger

Eclipse 3.x中，Log的接口和实现类分别为`org.eclipse.core.runtime.ILog`和`org.osgi.service.log.LogService`，可以使用`ServiceTracker`获取：

```
LogService getLog() {
  fLogServiceTracker = new ServiceTracker(fBundleContext, LogService.class.getName(), null);
  return (LogService) fLogServiceTracker.getService();
}
```

为了方便，在`Plugin`的基类中实现了`getLog()`方法，所有的`Plugin`子类可以直接使用。

在`org.eclipse.e4.core.services`插件中提供了`org.eclipse.e4.core.services.Logger`类，可以通过`@Inject`注解或使用`IEclipseContext`接口获取：

```
@Inject 
private Logger logger;


//or use code:
Logger log = (Logger) context.get(Logger.class.getName());

```



# 实现自己的服务

Usually services have two parts: the interface definition and the implementation. How these two are linked is defined by a context function , an OSGi service or plain context value setting (IEclipseContext). Please note that there can be more than one service implementation for an interface.

