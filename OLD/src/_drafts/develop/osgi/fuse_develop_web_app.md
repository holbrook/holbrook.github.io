---

---

# 从WAR到WAB

## Developing OSGi-enabled Java EE Applications

http://docs.oracle.com/cd/E26576_01/doc.312/e24930/osgi.htm


## 研究一下基于OSGI的web应用

 目前，J2EE的web应用可以说多不胜数，很多 做过J2EE，并开始接触OSGI的童鞋都会自然而然 地想，如果在OSGI之上该如何构建Web应用。在 这方面，OSGI虽然有一些解决方案，但“似乎”都 不是那么成熟的。这还真不好说，我隐隐约约感 觉似乎在观念上需要改变，就像我们要理解广义 相对论，需要去将万有引力的观念转变成时空扭 曲的观念来理解一样。不管如何，大概我们先理 理现在的观念还是比较必要的。

    我们都知道在J2EE，最基础的web应用的概念 就是Servlet。在OSGI范畴内，Servlet又是如何的 呢？对于OSGI来说，当然愿意将这成熟的Servlet 的概念继续用上，只是希望在servlet在模块化、 动态化方面演进一下。

    在J2EE里，由Selvet container来管理servlet的 生命周期，Servlet container根据部署描述文档 （web.xml)来部署servlet，当收到http请求，就 会根据请求的url查找到相应的servlet来处理请 求，并将servlet的返回的response响应请求。相 应的，在OSGI里，有个HttpService可以提供注册 servlet的方法（registerServlet）

HttpService的bundle有点类似Servlet container，它负责servlet的生命周期管理。

    如果每个Servlet都需要写调用HttpService的 registerServlet方法来注册的话，有点罗嗦。于是 就有whiteboard pattern在这方面的应用了。 whiteboard pattern是OSGI里经常使用的一种设 计模式，正如它的名字一样，这个模式就象你在 白板（whiteboard）上写下一条信息，然后另一 个需要那个信息的人就可以从白板上获得它，并 使用它。在这个过程中，谁写信息，谁用信息， 都不重要，而且什么时候用信息也不重要。

  在OSGI环境下，要将服务的发布和撤离看成是动 态的，就象白板上的信息一样。如果用 whiteboard pattern,就可以将发布者和使用者之 间的关联由OSGI service registry充当代理的角色 而获得解藕。


   除了支持动态页面的Servlet外，web还需要一些静态的资源来支持，例如：图片、待下载的文件、css、javascript脚本等等。

    为了支持这些静态资源，HttpService服务除了提供注册Servlet的方法（registerServlet）外，还提供了一个注册资源的方法（registerResources）  :
Java代码  收藏代码
HttpService service;
... ...

service.registerResources("/static","/var/www",null);

    上面的“/static”是别名，是资源url的一部分，"/var/www"则是别名映射的文件系统路径。例如：资源http://192.168.0.1/static/img1.png 则是指向文件系统/var/www/img1.png 。

    registerResources的第三个参数（上例中为null）是一个实现HttpContext接口的实例引用。
HttpContext接口的定义如下：
Java代码  收藏代码
public interface HttpContext
{
  String getMimeType(java.lang.String url);
  URL getResource(java.lang.String name);
  boolean handleSecurity(HttpServletRequest request, HttpServletResponse response);
}

    其中的getMimeType方法需要根据指定的url返回其对应的Mime Type标识名。有了这个方法，就可以在响应http请求时，带上相应的mime type，浏览器就可以根据mime type来处理相应的资源。
    handleSecurity方法则提供一个对Http请求做安全性检查的机制。
Java代码  收藏代码
HttpService service;
... ...
HttpContext myHttpContext = new MyHttpContext();
service.registerResources("/static", "/var/www", myHttpContext);

    对于Http请求，Servlet还需要过滤器filter的支持，以便作一些通用的过滤处理，例如：编码的转换、身份验证、cookies的处理等等，甚至某些web应用框架就是基于过滤器来做http请求的处理。
    但遗憾的是，在HttpService服务中，并不支持filter（毕竟HttpService服务不是正式的Servlet容器，不能全局性地处理Servlet）。为了达到实现filter的目的，apache felix定义了ExtHttpService服务，但到OSGI R4.2规范为止，ExtHttpService服务并未纳入OSGI规范中，也不知将来会否被纳入OSGI规范中。
    但无论如何，我们还是可以在任何osgi framework上使用felix ExtHttpService的bundle来支持这一特性。
Java代码  收藏代码
ExtHttpService service = (ExtHttpService) context.getService(sRef);
service.registerFilter(new myFilter(), "/servlet/.*", null, 0, null);

  其中myFilter实现javax.servlet.Filter接口。

  有了servlet和filter，web应用的UI部分就己经有了基础，但光凭这个来搭建一个复杂的web应用的UI就象用二极管、三极管、电阻、电容去搭建一台电脑一样，有些不切实际，我们还是渴望着能用上以往的那些mvc框架(例如struts,springmvc等)来降低复杂度。如果能象j2ee那样将一个war作为一个web应用来部署该多好呀！

     我们想到的，也已经有人做到了。这里我们引荐一个Pax web extender。Pax web extender是ops4j开源社区的出品。 Pax web Extender是用于 加载 WAB（Web Application Bundle）的工具，那么什么是WAB呢？它和WAR有什么区别呢？

    简单地说，WAB就是bundle化的WAR。

     首先，我们要意识到war包和jar包并没有本质的区别，如果我们在war包里的manifest.mf里添加上Bundle-ManifestVersion、Bundle-SymbolicName等若干bundle必要的元数据项的话，OSGI framework就可以将它当成一个bundle来加载。这样，osgi framework就可以加载这个bundle了，但对于osgi framework来说，它只是个bundle，并不会象j2ee web应用容器那样去解析这个war里的web.xml。这个工作需要Pax web extender来完成。

     对于Pax web extender来说，它是会监听OSGI framework安装bundle的事件，所以每个bundle被安装时，Pax web extender都能知道，然后就能检查这个bundle是否有部署配置描述文档web.xml,如果有的话，那么它就是个wab。

    我们需要在manifest.mf指定Webapp-Context项来指明这个web应用的Servlet Context路径。如果我们不指定的话，Pax web extender将使用Bundle-SymbolicName作为其默认值。有了Webapp-Context，pax web extender就可以部署这个wab了，就和J2EE web应用容器部署war一样。

    然而，做了以上的事后，WAB虽然被部署好了，但并不能正常运作。因为OSGI环境下特殊的ClassLoader的机制，Pax web extender并不会象J2EE web应用容器那样去加载wab里的WEB-INF/classes下的java类和WEB-INF/lib下的jar包，所以我们还需要在Manaifest.mf里做些手脚。

   用Bundle-ClassPath可以指定需由该bundle自身的classloader来加载的类和jar包，所以我们在Manifest.mf里加上：

Java代码  收藏代码
Bundle-ClassPath: .,WEB-INF/classes,WEB-INF/lib/<dependency>.jar... ...


   .:使web应用可访问到wab中根路径下的所有文件；

   WEB-INF/classes:使wab的classloader加载WEB-INF/classes下的java类;

   WEB-INF/lib/<dependency>.jar:需要将这个WAB所依赖的，并打包在WEB-INF/lib/下的jar包全部列出来（不能用通配符!所以是个挺繁琐的工作。 )。

  最后，WAB必然是需要依赖servlet api的，所以需要将以下package加入Import-Package里：
Java代码  收藏代码
Import-Package: javax.servlet,javax.servlet.http

到此为止，WAB就应该可以正常运作了。

似乎我们已完美解决了基于osgi的web应用问题，但事情并没有这么简单... ...。

上节提到将war包改造成wab，通过pax web extender部署 在OSGI framework上的方式来发布 web应用。表面上，我们似乎只需要作少量的改 动，就能将旧的web应用OSGI化了，但是我们没 得到任何好处，只是为OSGI化而OSGI化了，既 没得到OSGI的模块化、动态化的好处，还得受 OSGI classloader机制的限制。既然如此，我们 何必自讨苦吃地将它改造成wab呢？

   我们审视一下war的一般组成:部署描述文档，一 些配置文件，自有的一系列java类，自有的一堆 web静态资源文件和一大堆依赖的第三方jar 包......,可以说war是一个粗粒度的复合体。

   假设我们需要部署若干个wab到OSGI framework 上，那么，被依赖的第三方jar包就需要在每个 wab各自的classloader重复加载，如果将这些第 三方jar包改造成bundle，独立加载，并export出 相应的package供所有wab共享使用，那么就不 需重复加载了。但是这样做，第三方jar包改造成 的bundle就和这些wab很紧密地藕合在一起，和 OSGI模块化的本义背道而驰了。

    我们用OSGI模块化的其中一个目的就是软件构件 的复用，象war这样粗粒度的构件要复用的可能 性可以说是等于零。所以，要将war这个复合 体"分解"出一批细粒度的构件，才能发挥OSGI的 好处。

    充分利用OSGI service是开发OSGI应用的一种好 的实践。如果我们将wab中公用的功能以SOA的 思路分离出来，用OSGI service的形式来实现和 组装成独立的公用服务，供各wab调用，就可以 将wab这个复合体逐步分离出细粒度的模块出 来，并采用OSGI service的方式与wab松散藕 合，就可以达到OSGI模块化的目的了。

   但是具体的做法如何？是否有好的模式来实现？

# 开发

```
mvn archetype:generate  \
-DarchetypeGroupId=org.ops4j.pax.web.archetypes \
-DarchetypeArtifactId=wab-archetype \
-DarchetypeVersion=3.0.6 \
-DgroupId=thinkinside.demo.fuse \
-DartifactId=webapp-demo \
-Dversion=1.0.0-SNAPSHOT
```
Archetype:

<dependency>
    <groupId>org.ops4j.pax.web.archetypes</Groupid>
    <artifactId>wab-archetype</artifactId>
    <version>3.0.6</version>
</dependency>
