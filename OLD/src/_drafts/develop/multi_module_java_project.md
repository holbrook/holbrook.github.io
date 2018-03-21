当软件系统的规模变大时，一个基本的处理办法是将其分解成若干个小的组成部分。根据组成部分的规模，可以划分成子系统、层、模块等。

尽管[分层架构]()已经被广泛应用，但是当系统的规模进一步扩大时，每个层的已经膨胀

分层架构


包，jar, 模块， 层，

jar:物理分割

包，层：逻辑分割

通常，jar 之间的包不应该重复


# UML包图

尽管可以对一个大型的类图随意进行分割，但这种随意的分割没有任何意义。

为了对类之间的关系进行更好的控制，UML中引入的包图。

包中可以包含包或类。

（图）

引入包的目的是为了管理可见性。
1. java语言中，包内类的可见性？属性和方法的可见性？
2. 包之间的可见性：隐含

包之间可见性的关系：


依赖关系
•《use》使用关系：是一种默认的依赖关系，说明客户包（发出者）中的元素以某种方式使用提供者包（箭头指向的包）的公共元素，也就是说客户包依赖于提供者包
•《import》引用关系：最普遍的包依赖类型，说明提供者包(箭头指向的包)的命名空间（包本身代表命名空间）将被添加到客户包（发出者）的命名空间中，客户包中的元素也能够访问提供者包的所有公共元素
•《access》访问关系：只想使用提供者包中的元素，而不想将其命名空间合并则应使用该关系
•《trace》追溯关系：想表示一个包到另一个包的历史发展，则需要使用《trace》关系来表示


- 前提？

一个包的函数中使用了另一个包



- 包中类的可见性

包外是否可见

包图可以表示包含关系

# 分层架构

包常用于分层架构。这里的层(layer)是指逻辑上的层次，与物理上的层(Tier)不同。

# 层内分包

对于更大规模的系统，每个层的规模都会比较大，需要进一步的分割。通常，这种分割会以领域模型入手，……



# 设计篇

DDD

聚合


模块关系

组装assembly



分析模式：

11.交易包
12.分层架构
13.应用外关

# 框架篇

## spring

## OSGI



# 构建篇

## maven
### http://www.davenkin.me/post/2013-08-03/create-multi-module-maven-project

Maven提高篇系列之一——多模块 vs  继承
这是一个关于Maven的提高系列，其中包含以下文章：
通常来说，在Maven的多模块工程中，都存在一个pom类型的工程作为根模块，该工程只包含一个pom.xml文件，在该文件中以模块（module）的形式声明它所包含的子模块，即多模块工程。在子模块的pom.xml文件中，又以parent的形式声明其所属的父模块，即继承。然而，这两种声明并不必同时存在，我们将在下文中讲到这其中的区别。
（一）创建Maven多模块工程
多模块的好处是你只需在根模块中执行Maven命令，Maven会分别在各个子模块中执行该命令，执行顺序通过Maven的Reactor机制决定。先来看创建Maven多模块工程的常规方法。在我们的示例工程中，存在一个父工程，它包含了两个子工程（模块），一个core模块，一个webapp模块，webapp模块依赖于core模块。这是一种很常见的工程划分方式，即core模块中包含了某个领域的核心业务逻辑，webapp模块通过调用core模块中服务类来创建前端网站。这样将核心业务逻辑和前端展现分离开来，如果之后决定开发另一套桌面应用程序，那么core模块是可以重用在桌面程序中。
首先通过Maven的Archetype插件创建一个父工程，即一个pom类型的Maven工程，其中只包含一个pom.xml文件：
mvn archetype:generate -DgroupId=me.davenkin -DartifactId=maven-multi-module -DarchetypeGroupId=org.codehaus.mojo.archetypes -DarchetypeArtifactId=pom-root -DinteractiveMode=false
以上命令在当前目录下创建了一个名为maven-multi-module的目录，该目录便表示这个pom类型的父工程，在该目录只有一个pom.xml文件：
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
 <modelVersion>4.0.0</modelVersion>
 <groupId>me.davenkin</groupId>
 <artifactId>maven-multi-module</artifactId>
 <version>1.0-SNAPSHOT</version>
 <packaging>pom</packaging>
 <name>maven-multi-module</name>
</project>
这个pom.xml非常简单，最值得一看的是其中的“<packaging>pom</packaging>”，表示该工程为pom类型。其他的Maven工程类型还有jar、war、ear等。
此时，父工程便创建好了，接下来我们创建core模块，由于core模块属于maven-multi-module模块，我们将工作目录切换到maven-multi-module目录下（当然你也可以不用，只是需要一些额外的配置），创建core模块命令如下：
mvn archetype:generate -DgroupId=me.davenkin -DartifactId=core  -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false
这里我们使用了Archetype插件的maven-archetype-quickstart，它创建一个jar类型的模块。此时，如果我们在打开maven-multi-module模块的pom.xml会发现，其中多了以下内容：
 <modules>
   <module>core</module>
 </modules>
这里的core即是我们刚才创建的core模块，再看看core模块中的pom.xml文件：
<?xml version="1.0"?>
<project xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd" xmlns="http://maven.apache.org/POM/4.0.0"
   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
 <modelVersion>4.0.0</modelVersion>
 <parent>
   <artifactId>maven-multi-module</artifactId>
   <groupId>me.davenkin</groupId>
   <version>1.0-SNAPSHOT</version>
 </parent>
 <groupId>me.davenkin</groupId>
 <artifactId>core</artifactId>
 <version>1.0-SNAPSHOT</version>
 <name>core</name>
 <url>http://maven.apache.org</url>
 <dependencies>
   <dependency>
     <groupId>junit</groupId>
     <artifactId>junit</artifactId>
     <version>3.8.1</version>
     <scope>test</scope>
   </dependency>
 </dependencies>
</project>
请注意里面的  “<parent>...  </parent>”，它将maven-multi-module模块做为了自己的父模块。这里我们看出，当创建core模块时，Maven将自动识别出已经存在的maven-multi-module父模块，然后分别创建两个方向的指引关系，即在maven-multi-module模块中将core作为自己的子模块，在core模块中将maven-multi-module作为自己的父模块。要使Maven有这样的自动识别功能，我们需要在maven-multi-module目录下创建core模块（请参考前文），不然，core模块将是一个独立的模块，但是我们可以通过手动修改两个模块中的pom.xml文件来创建他们之间的父子关系，从而达到同样的目的。
依然在maven-multi-module目录下，通过与core相同的方法创建webapp模块：
mvn archetype:generate -DgroupId=me.davenkin -DartifactId=webapp -DarchetypeArtifactId=maven-archetype-webapp -DinteractiveMode=false
这里的maven-archetype-webapp表明Maven创建的是一个war类型的工程模块。此时再看maven-multi-module模块的pom.xml文件，其中的<modules>中多了一个webapp模块：
<modules>
   <module>core</module>
   <module>webapp</module>
 </modules>
而在webapp模块的pom.xml文件中，也以 “<parent>...  </parent>”的方式将maven-multi-module模块声明为自己的父模块，这些同样是得益于Maven自动识别的结果。
此时，在maven-multi-module目录下，我们执行以下命令完成整个工程的编译、打包和安装到本地Maven Repository的过程：
mvn clean install
（二）手动添加子模块之间的依赖关系
此时我们虽然创建了一个多模块的Maven工程，但是有两个问题我们依然没有解决：
（1）没有发挥Maven父模块的真正作用
（2）webapp模块对core模块的依赖关系尚未建立
针对（1），Maven父模块的作用本来是使子模块可以继承并覆盖父模块中的配置，比如dependency等，但是如果我们看看webapp和core模块中pom.xml文件，他们都声明了对Junit的依赖，而如果多个子模块都依赖于相同的类库，我们应该将这些依赖配置在父模块中，继承自父模块的子模块将自动获得这些依赖。所以接下来我们要做的便是：将webapp和core模块对junit的依赖删除，并将其迁移到父模块中。
对于（2），Maven在创建webapp模块时并不知道webapp依赖于core，所以这种依赖关系需要我们手动加入，在webapp模块的pom.xml中加入对core模块的依赖：
       <dependency>
           <groupId>me.davenkin</groupId>
           <artifactId>core</artifactId>
           <version>1.0-SNAPSHOT</version>
       </dependency>
此时再在maven-multi-module目录下执行 “mvn clean install”，Maven将根据自己的Reactor机制决定哪个模块应该先执行，哪个模块应该后执行。比如，这里的webapp模块依赖于core模块，那么Maven会先在core模块上执行“mvn clean install”，再在webapp模块上执行相同的命令。在webapp上执行“mvn clean install”时，由于core模块已经被安装到了本地的Repository中，webapp便可以顺利地找到所依赖的core模块。
总的来看，此时命令的执行顺序为maven-multi-module -> core -> webapp，先在maven-multi-module上执行是因为其他两个模块都将它作为父模块，即对它存在依赖关系，又由于core被webapp依赖，所以接下来在core上执行命令，最后在webapp上执行。
这里又有一个问题：为什么非得在maven-multi-module目录下执行 “mvn clean install”？答案是，并不是非得如此，只是你需要搞清楚Maven的工作机制。在maven-multi-module目录下执行，即是在父工程中执行，此时Maven知道父模块所包含的所有子模块，并会自动按照模块依赖关系处理执行顺序。如果只在子模块中执行，那么Maven并不知道它对其他模块的依赖关系。举个例子，当在webapp中执行 “mvn clean install”，Maven发现webapp自己依赖于core，此时Maven只会在本地的Repository中去找core，如果存在，那么你很幸运，如果不存在，那么对不起，运行失败，说找不到core，因为Maven并不会先将core模块安装到本地Repository。此时你需要做的是，切换到core目录，执行“mvn clean install”将core模块安装到本地Repository，再切换回webapp目录，执行“mvn clean install”，万事才大吉。
多么繁琐的步骤，此时你应该能体会到在maven-multi-module下执行Maven命令的好处了吧。总结一下：在maven-multi-module下执行“mvn clean install”， Maven会在每个模块上执行该命令，然后又发现webapp依赖于core，此时他们之间有一个协调者（即父工程），它知道将core作为webapp的依赖，于是会先在core模块上执行“mvn clean install”，当在webapp上执行命令时，无论此时的core模块是否存在于本地Repository中，父工程都能够获取到core模块（如果不存在于本地Repository，它将现场编译core模块，再将其做为webapp的依赖，比如此时使用“mvn clean package”也是能够构建成功的），所以一切成功。
这里又牵扯到Maven如何查找依赖的问题，简单来说，Maven会先在本地Repository中查找依赖，如果依赖存在，则使用该依赖，如果不存在，则通过pom.xml中的Repository配置从远程下载依赖到本地Repository中。默认情况下，Maven将使用Maven Central Repository 作为远端Repository。于是你又有问题了：“在pom.xml中为什么没有看到这样的配置信息啊？”原因在于，任何一个Maven工程都默认地继承自一个Super POM，Repository的配置信息便包含在其中。
（三）多模块 vs 继承
在文章一开始我们便提到，在Maven中，由多模块（由上到下）和继承（由下到上）关系并不必同时存在。
（1）如果保留webapp和core中对maven-multi-module的父关系声明，即保留 “<parent>...  </parent>”，而删除maven-multi-module中的子模块声明，即“<modules>...<modules>”，会发生什么情况？此时，整个工程已经不是一个多模块工程，而只是具有父子关系的多个工程集合。如果我们在maven-multi-module目录下执行“mvn clean install”，Maven只会在maven-multi-module本身上执行该命令，继而只会将maven-multi-module安装到本地Repository中，而不会在webapp和core模块上执行该命令，因为Maven根本就不知道这两个子模块的存在。另外，如果我们在webapp目录下执行相同的命令，由于由子到父的关系还存在，Maven会在本地的Repository中找到maven-multi-module的pom.xml文件和对core的依赖（当然前提是他们存在于本地的Repository中），然后顺利执行该命令。
这时，如果我们要发布webapp，那么我们需要先在maven-multi-module目录下执行“mvn clean install”将最新的父pom安装在本地Repository中，再在core目录下执行相同的命令将最新的core模块安装在本地Repository中，最后在webapp目录下执行相同的命令完成最终war包的安装。麻烦。
（2）如果保留maven-multi-module中的子模块声明，而删除webapp和core中对maven-multi-module的父关系声明，又会出现什么情况呢？此时整个工程只是一个多模块工程，而没有父子关系。Maven会正确处理模块之间的依赖关系，即在webapp模块上执行Maven命令之前，会先在core模块上执行该命令，但是由于core和webapp模块不再继承自maven-multi-module，对于每一个依赖，他们都需要自己声明，比如我们需要分别在webapp和core的pom.xml文件中声明对Junit依赖。
综上，多模块和父子关系是不同的。如果core和webapp只是在逻辑上属于同一个总工程，那么我们完全可以只声明模块关系，而不用声明父子关系。如果core和webapp分别处理两个不同的领域，但是它们又共享了很多，比如依赖等，那么我们可以将core和webapp分别继承自同一个父pom工程，而不必属于同一个工程下的子模块。



### Maven多项目依赖配置

http://niweiwei.iteye.com/blog/1965760

Maven多项目依赖配置 - niweiwei - ITeye 技术网站
最近在学习Maven，把一个开源的项目改成maven管理，期间使用到了多项目，从网上查阅了一些资料，主要参考的是http://kyfxbl.iteye.com/blog/1680045 ，在此把自己的一些心得体会写出来，供大家学习交流。
关于maven的安装，在此就不进行阐述，请参考网上其他教程。
本实例由4个项目组成，其中，aggregator是父工程，同时承担聚合模块和父模块的作用，没有实际代码和资源文件；open-plagform-common是公共的java工程；open-platfor-web是公共的web文件，主要包括css、js等；open-bug-m是最终要发布的应用，形成war包。
一、建立一个Maven工程：aggregator
/aggregator
   /src/main/java
   /src/test/java
   pom.xml
此工程主要是父模块，聚合其他工程，没有实际代码和资源文件，最主要的是pom.xml文件，其主要内容如下：


Xml代码  

  1. <modelVersion>4.0.0</modelVersion>  
  2.   <groupId>cn.jess.platform</groupId>  
  3.   <artifactId>aggregator</artifactId>  
  4.   <version>0.0.1-SNAPSHOT</version>  
  5. <!-- 因为是父工程 ，因此此处的packaging必须为pom -->  
  6.   <packaging>pom</packaging>  
  7.   <name>aggregator</name>  
  8.   <modules>    
  9.     <module>../open-platform-common</module>    
  10.     <module>../open-platform-web</module>    
  11.     <module>../open-bug-m</module>  
  12.   </modules>  
  13.   <!-- 配置部署的远程仓库 -->    
  14.   <distributionManagement>    
  15.     <snapshotRepository>    
  16.       <id>nexus-snapshots</id>    
  17.       <name>nexus distribution snapshot repository</name>    
  18.       <url>http://127.0.0.1:8081/nexus/content/repositories/snapshots/</url>    
  19.     </snapshotRepository>    
  20.   </distributionManagement>  
  21.   <build>    
  22.      <pluginManagement>    
  23.        <plugins>    
  24.              <plugin>    
  25.                  <groupId>org.apache.maven.plugins</groupId>    
  26.                  <artifactId>maven-resources-plugin</artifactId>    
  27.                  <version>2.6</version>    
  28.                  <configuration>    
  29.                      <encoding>UTF-8</encoding>    
  30.                  </configuration>    
  31.              </plugin>    
  32.              <plugin>    
  33.                  <groupId>org.apache.maven.plugins</groupId>    
  34.                  <artifactId>maven-compiler-plugin</artifactId>    
  35.                  <version>2.5.1</version>    
  36.                  <configuration>    
  37.                      <encoding>UTF-8</encoding>  
  38.                      <source>1.6</source>  
  39.                      <target>1.6</target>    
  40.                  </configuration>    
  41.              </plugin>    
  42.          </plugins>    
  43.      </pluginManagement>    
  44.  </build>    
  45.  <dependencyManagement>    
  46.      <dependencies>    
  47.          <dependency>    
  48.              <groupId>com.sun</groupId>    
  49.              <artifactId>tools</artifactId>    
  50.              <version>1.6.0</version>    
  51.              <scope>system</scope>    
  52.              <systemPath>${env.JAVA_HOME}/lib/tools.jar</systemPath>    
  53.          </dependency>    
  54.      </dependencies>    
  55.  </dependencyManagement>  

<modelVersion>4.0.0</modelVersion>  <groupId>cn.jess.platform</groupId>  <artifactId>aggregator</artifactId>  <version>0.0.1-SNAPSHOT</version><!-- 因为是父工程 ，因此此处的packaging必须为pom -->  <packaging>pom</packaging>  <name>aggregator</name>    <modules>      <module>../open-platform-common</module>      <module>../open-platform-web</module>      <module>../open-bug-m</module>  </modules>    <!-- 配置部署的远程仓库 -->    <distributionManagement>      <snapshotRepository>        <id>nexus-snapshots</id>        <name>nexus distribution snapshot repository</name>        <url>http://127.0.0.1:8081/nexus/content/repositories/snapshots/</url>      </snapshotRepository>    </distributionManagement>    <build>       <pluginManagement>         <plugins>               <plugin>                   <groupId>org.apache.maven.plugins</groupId>                   <artifactId>maven-resources-plugin</artifactId>                   <version>2.6</version>                   <configuration>                       <encoding>UTF-8</encoding>                   </configuration>               </plugin>               <plugin>                   <groupId>org.apache.maven.plugins</groupId>                   <artifactId>maven-compiler-plugin</artifactId>                   <version>2.5.1</version>                   <configuration>                       <encoding>UTF-8</encoding>                     <source>1.6</source>                                 <target>1.6</target>                   </configuration>               </plugin>           </plugins>       </pluginManagement>   </build>     <dependencyManagement>       <dependencies>           <dependency>               <groupId>com.sun</groupId>               <artifactId>tools</artifactId>               <version>1.6.0</version>               <scope>system</scope>               <systemPath>${env.JAVA_HOME}/lib/tools.jar</systemPath>           </dependency>       </dependencies>   </dependencyManagement>
    二、建立一个Maven工程：open-platform-common
此工程主要是项目中使用到的公共java类库，pom文件主要内容如下：


Xml代码  

  1. <!-- 由于存在parent工程，因此groupId和version可以省略，直接使用parent工程-->  
  2.   <modelVersion>4.0.0</modelVersion>  
  3.   <artifactId>open-platform-common</artifactId>  
  4.  <!-- 因为此工程要发布到webapp的lib目录下，因此为jar(不知道这样解释对否？) -->  
  5.  <packaging>jar</packaging>  
  6.   <properties>  
  7.     <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>  
  8.   </properties>    
  9.     <!-- 指定Maven仓库 -->  
  10.     <repositories>  
  11.         <!-- my的maven仓库 -->  
  12.         <repository>  
  13.             <id>myRepository</id>  
  14.             <name>local private nexus</name>  
  15.             <url>http://127.0.0.1:8081/nexus/content/groups/public/</url>  
  16.             <releases>  
  17.                 <enabled>true</enabled>  
  18.             </releases>  
  19.             <snapshots>  
  20.                 <enabled>true</enabled>  
  21.             </snapshots>  
  22.         </repository>  
  23.     </repositories>  
  24.   <!-- 指定maven plugin仓库 -->  
  25.     <pluginRepositories>  
  26.         <!-- oschina的maven plugin仓库 -->  
  27.         <pluginRepository>  
  28.             <id>myPluginRepository</id>  
  29.             <name>local private nexus</name>  
  30.             <url>http://127.0.0.1:8081/nexus/content/groups/public/</url>  
  31.             <releases>  
  32.                 <enabled>true</enabled>  
  33.             </releases>  
  34.             <snapshots>  
  35.                 <enabled>false</enabled>  
  36.             </snapshots>  
  37.         </pluginRepository>  
  38.     </pluginRepositories>  
  39.   <dependencies>  
  40.         <!-- 此处的类库根据自己的需要进行添加 -->  
  41.   </dependencies>  
  42.   <!-- 用来指定父工程-->  
  43.   <parent>  
  44.     <groupId>cn.jess.platform</groupId>  
  45.     <artifactId>aggregator</artifactId>  
  46.     <version>0.0.1-SNAPSHOT</version>  
  47.     <relativePath>../aggregator</relativePath>  
  48.   </parent>  

<!-- 由于存在parent工程，因此groupId和version可以省略，直接使用parent工程-->  <modelVersion>4.0.0</modelVersion>  <artifactId>open-platform-common</artifactId> <!-- 因为此工程要发布到webapp的lib目录下，因此为jar(不知道这样解释对否？) --> <packaging>jar</packaging>  <properties>    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>  </properties>          <!-- 指定Maven仓库 -->        <repositories>                <!-- my的maven仓库 -->                <repository>                        <id>myRepository</id>                        <name>local private nexus</name>                        <url>http://127.0.0.1:8081/nexus/content/groups/public/</url>                        <releases>                                <enabled>true</enabled>                        </releases>                        <snapshots>                                <enabled>true</enabled>                        </snapshots>                </repository>        </repositories>  <!-- 指定maven plugin仓库 -->        <pluginRepositories>                <!-- oschina的maven plugin仓库 -->                <pluginRepository>                        <id>myPluginRepository</id>                        <name>local private nexus</name>                        <url>http://127.0.0.1:8081/nexus/content/groups/public/</url>                        <releases>                                <enabled>true</enabled>                        </releases>                        <snapshots>                                <enabled>false</enabled>                        </snapshots>                </pluginRepository>        </pluginRepositories>  <dependencies>        <!-- 此处的类库根据自己的需要进行添加 -->  </dependencies>  <!-- 用来指定父工程-->  <parent>        <groupId>cn.jess.platform</groupId>        <artifactId>aggregator</artifactId>        <version>0.0.1-SNAPSHOT</version>        <relativePath>../aggregator</relativePath>  </parent>
    三、建立一个Maven工程：open-platform-web
    此工程主要是项目中使用到的公共web文件，pom文件主要内容如下：


Xml代码  

  1. <!-- 由于存在parent工程，因此groupId和version可以省略，直接使用parent工程-->  
  2.   <modelVersion>4.0.0</modelVersion>  
  3.   <artifactId>open-platform-web</artifactId>  
  4. <!-- 因为此工程要发布到webapp应用的根目录下，因此为war(不知道这样解释对否？) -->  
  5.   <packaging>war<ng>  
  6.   <properties>  
  7.     <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>  
  8.   </properties>    
  9.     <!-- 指定Maven仓库 -->  
  10.     <repositories>  
  11.         <!-- my的maven仓库 -->  
  12.         <repository>  
  13.             <id>myRepository</id>  
  14.             <name>local private nexus</name>  
  15.             <url>http://127.0.0.1:8081/nexus/content/groups/public/</url>  
  16.             <releases>  
  17.                 <enabled>true</enabled>  
  18.             </releases>  
  19.             <snapshots>  
  20.                 <enabled>true</enabled>  
  21.             </snapshots>  
  22.         </repository>  
  23.     </repositories>  
  24.   <!-- 指定maven plugin仓库 -->  
  25.     <pluginRepositories>  
  26.         <!-- oschina的maven plugin仓库 -->  
  27.         <pluginRepository>  
  28.             <id>myPluginRepository</id>  
  29.             <name>local private nexus</name>  
  30.             <url>http://127.0.0.1:8081/nexus/content/groups/public/</url>  
  31.             <releases>  
  32.                 <enabled>true</enabled>  
  33.             </releases>  
  34.             <snapshots>  
  35.                 <enabled>false</enabled>  
  36.             </snapshots>  
  37.         </pluginRepository>  
  38.     </pluginRepositories>  
  39.   <parent>  
  40.     <groupId>cn.jess.platform</groupId>  
  41.     <artifactId>aggregator</artifactId>  
  42.     <version>0.0.1-SNAPSHOT</version>  
  43.     <relativePath>../aggregator</relativePath>  
  44.   </parent>  
  45. </project>  

<!-- 由于存在parent工程，因此groupId和version可以省略，直接使用parent工程-->  <modelVersion>4.0.0</modelVersion>  <artifactId>open-platform-web</artifactId><!-- 因为此工程要发布到webapp应用的根目录下，因此为war(不知道这样解释对否？) -->  <packaging>war<ng>  <properties>    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>  </properties>          <!-- 指定Maven仓库 -->        <repositories>                <!-- my的maven仓库 -->                <repository>                        <id>myRepository</id>                        <name>local private nexus</name>                        <url>http://127.0.0.1:8081/nexus/content/groups/public/</url>                        <releases>                                <enabled>true</enabled>                        </releases>                        <snapshots>                                <enabled>true</enabled>                        </snapshots>                </repository>        </repositories>  <!-- 指定maven plugin仓库 -->        <pluginRepositories>                <!-- oschina的maven plugin仓库 -->                <pluginRepository>                        <id>myPluginRepository</id>                        <name>local private nexus</name>                        <url>http://127.0.0.1:8081/nexus/content/groups/public/</url>                        <releases>                                <enabled>true</enabled>                        </releases>                        <snapshots>                                <enabled>false</enabled>                        </snapshots>                </pluginRepository>        </pluginRepositories>    <parent>        <groupId>cn.jess.platform</groupId>        <artifactId>aggregator</artifactId>        <version>0.0.1-SNAPSHOT</version>        <relativePath>../aggregator</relativePath>  </parent></project>
    注意：此工程的WEB-INF目录下必须包含web.xml文件，否则在执行mvn时会报错
    四、建立一个Maven工程：open-bug-m：
此工程是最终要发布的应用，其依赖于open-platform-common和open-platform-web，因此在pom文件中要加入这两个工程的依赖，pom文件内容如下所示：


Xml代码  

  1. <groupId>open-bug-m</groupId>  
  2.   <artifactId>open-bug-m</artifactId>  
  3.   <packaging>war</packaging>  
  4.   <name/>  
  5.   <description/>  
  6.   <properties>  
  7.     <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>  
  8.   </properties>  
  9.   <parent>  
  10.     <groupId>cn.jess.platform</groupId>  
  11.     <artifactId>aggregator</artifactId>  
  12.     <version>0.0.1-SNAPSHOT</version>  
  13.     <relativePath>../aggregator</relativePath>  
  14.   </parent>   
  15.     <!-- 指定Maven仓库 -->  
  16.     <repositories>  
  17.         <!-- my的maven仓库 -->  
  18.         <repository>  
  19.             <id>myRepository</id>  
  20.             <name>local private nexus</name>  
  21.             <url>http://127.0.0.1:8081/nexus/content/groups/public/</url>  
  22.             <releases>  
  23.                 <enabled>true</enabled>  
  24.             </releases>  
  25.             <snapshots>  
  26.                 <enabled>true</enabled>  
  27.             </snapshots>  
  28.         </repository>  
  29.     </repositories>  
  30.   <!-- 指定maven plugin仓库 -->  
  31.     <pluginRepositories>  
  32.         <!-- oschina的maven plugin仓库 -->  
  33.         <pluginRepository>  
  34.             <id>myPluginRepository</id>  
  35.             <name>local private nexus</name>  
  36.             <url>http://127.0.0.1:8081/nexus/content/groups/public/</url>  
  37.             <releases>  
  38.                 <enabled>true</enabled>  
  39.             </releases>  
  40.             <snapshots>  
  41.                 <enabled>false</enabled>  
  42.             </snapshots>  
  43.         </pluginRepository>  
  44.     </pluginRepositories>  
  45.   <dependencies>  
  46.     <dependency>  
  47.       <groupId>cn.jess.platform</groupId>  
  48.       <artifactId>open-platform-common</artifactId>  
  49.       <version>0.0.1-SNAPSHOT</version>  
  50.       <type>jar</type>  
  51.     </dependency>  
  52.     <dependency>  
  53.       <groupId>cn.jess.platform</groupId>  
  54.       <artifactId>open-platform-web</artifactId>  
  55.       <version>0.0.1-SNAPSHOT</version>  
  56.       <type>war</type>  
  57.     </dependency>        
  58.     <!-- 此处的类库根据自己的需要进行添加 -->  
  59.   </dependencies>  
  60.   <build>  
  61.     <finalName>open-bug</finalName>  
  62.     <plugins>  
  63.       <plugin>    
  64.           <groupId>org.apache.maven.plugins</groupId>    
  65.           <artifactId>maven-war-plugin</artifactId>  
  66.           <version>2.3</version>    
  67.           <configuration>    
  68.              <packagingExcludes>WEB-INF/web.xml</packagingExcludes>      
  69.              <overlays>    
  70.                 <overlay>    
  71.                   <groupId>cn.jess.platform</groupId>    
  72.                   <artifactId>open-platform-web</artifactId>    
  73.                 </overlay>    
  74.              </overlays>    
  75.           </configuration>    
  76.       </plugin>    
  77.       <plugin>    
  78.         <groupId>org.codehaus.cargo</groupId>    
  79.         <artifactId>cargo-maven2-plugin</artifactId>    
  80.         <version>1.2.3</version>    
  81.         <configuration>    
  82.           <container>    
  83.             <containerId>tomcat7x</containerId>    
  84.             <home>F:\apache-tomcat-7.0.42(x64)</home>    
  85.           </container>    
  86.           <configuration>    
  87.             <type>existing</type>    
  88.             <home>F:\apache-tomcat-7.0.42(x64)</home>    
  89.             <properties>    
  90.               <cargo.jvmargs>    
  91.                   -Xdebug                    -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=8787    
  92.               </cargo.jvmargs>    
  93.             </properties>    
  94.           </configuration>    
  95.         </configuration>    
  96.         <executions>    
  97.           <execution>    
  98.              <id>cargo-run</id>    
  99.              <phase>pre-integration-test</phase>    
  100.              <goals>    
  101.                  <goal>run</goal>    
  102.              </goals>    
  103.           </execution>    
  104.         </executions>    
  105.     </plugin>   
  106.     </plugins>  
  107.   </build>  

<groupId>open-bug-m</groupId>  <artifactId>open-bug-m</artifactId>  <packaging>war</packaging>  <name/>  <description/>  <properties>    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>  </properties>  <parent>        <groupId>cn.jess.platform</groupId>        <artifactId>aggregator</artifactId>        <version>0.0.1-SNAPSHOT</version>        <relativePath>../aggregator</relativePath>  </parent>         <!-- 指定Maven仓库 -->        <repositories>                <!-- my的maven仓库 -->                <repository>                        <id>myRepository</id>                        <name>local private nexus</name>                        <url>http://127.0.0.1:8081/nexus/content/groups/public/</url>                        <releases>                                <enabled>true</enabled>                        </releases>                        <snapshots>                                <enabled>true</enabled>                        </snapshots>                </repository>        </repositories>  <!-- 指定maven plugin仓库 -->        <pluginRepositories>                <!-- oschina的maven plugin仓库 -->                <pluginRepository>                        <id>myPluginRepository</id>                        <name>local private nexus</name>                        <url>http://127.0.0.1:8081/nexus/content/groups/public/</url>                        <releases>                                <enabled>true</enabled>                        </releases>                        <snapshots>                                <enabled>false</enabled>                        </snapshots>                </pluginRepository>        </pluginRepositories>  <dependencies>        <dependency>      <groupId>cn.jess.platform</groupId>          <artifactId>open-platform-common</artifactId>          <version>0.0.1-SNAPSHOT</version>          <type>jar</type>    </dependency>    <dependency>      <groupId>cn.jess.platform</groupId>          <artifactId>open-platform-web</artifactId>          <version>0.0.1-SNAPSHOT</version>          <type>war</type>    </dependency>              <!-- 此处的类库根据自己的需要进行添加 -->          </dependencies>  <build>        <finalName>open-bug</finalName>    <plugins>      <plugin>            <groupId>org.apache.maven.plugins</groupId>            <artifactId>maven-war-plugin</artifactId>          <version>2.3</version>            <configuration>               <packagingExcludes>WEB-INF/web.xml</packagingExcludes>                 <overlays>                  <overlay>                    <groupId>cn.jess.platform</groupId>                    <artifactId>open-platform-web</artifactId>                  </overlay>               </overlays>            </configuration>        </plugin>        <plugin>          <groupId>org.codehaus.cargo</groupId>          <artifactId>cargo-maven2-plugin</artifactId>          <version>1.2.3</version>          <configuration>            <container>              <containerId>tomcat7x</containerId>              <home>F:\apache-tomcat-7.0.42(x64)</home>            </container>            <configuration>              <type>existing</type>              <home>F:\apache-tomcat-7.0.42(x64)</home>              <properties>                <cargo.jvmargs>                    -Xdebug                    -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=8787                </cargo.jvmargs>              </properties>            </configuration>          </configuration>          <executions>            <execution>               <id>cargo-run</id>               <phase>pre-integration-test</phase>               <goals>                   <goal>run</goal>               </goals>            </execution>          </executions>      </plugin>     </plugins>  </build>
    关于maven-war-plugin和cargo-maven2-plugin的使用方法请参考网上其他使用教程。
所有上述四个工程准备就绪后，执行mvn install就可对工程项目进行部署。
现在存在的一个问题主要是：
如果把open-platform-common和open-platform-web工程合并为一个，则在open-bug-m不知道如何去引用它？ 
## gradle

http://www.infoq.com/cn/articles/Gradle-application-in-large-Java-projects


Gradle在大型Java 项目上的应用
作者 何海洋 发布于 七月 05, 2013 | 6 讨论
在Java构建工具的世界里，先有了Ant，然后有了Maven。Maven的CoC[1]、依赖管理以及项目构建规则重用性等特点，让Maven几乎成为Java构建工具的事实标准。然而，冗余的依赖管理配置、复杂并且难以扩展的构建生命周期，都成为使用Maven的困扰。
Gradle 作为新的构建工具，获得了2010 Springy 大奖，并入围了2011的Jax 最佳Java技术发明奖。它是基于Groovy语言的构建工具，既保持了Maven的优点，又通过使用Groovy定义的DSL[2]，克服了 Maven中使用XML繁冗以及不灵活等缺点。在Eugene Dvorkin撰写的文章《最让人激动的5个Java项目》 中，他是这样介绍Gradle的：
“工程自动化是软件项目成功的必要条件，而且它应该实现起来简单、易用、好玩。构建没有千篇一律的方法，所以Gradle没有死板的强加方法于我们，尽管你会认为查找和描述方法很重要，然而Gradle对于如何描述有着非常好的支持。我不认为工具能够拯救我们，但是Gradle能给你所需要的自由，你可以利用Gradle构建易描述的、可维护的、简洁的、高性能项目”。
在最近半年里，我在使用Gradle作为构建脚本的大型Java项目上工作，更深切体会到Gradle在项目构建过程中是如此的简单、易用。
1. 多Module 的项目
Hibernate项目负责人Steve Ebersole在Hibernate将构建脚本从Maven换成Gradle时，专门写了一篇文章《Gradle: why?》 ，文中提到Maven的一个缺点就是：Maven不支持多module的构建。在Micro-Service[3]架构风格流行的今天，在一个项目里面包含多个Module已成为一种趋势。Gradle天然支持多module，并且提供了很多手段来简化构建脚本。在Gradle中，一个模块就是它的一个子项目（subproject），所以，我使用父项目来描述顶级项目，使用子项目来描述顶级项目下面的模块。
1.1  配置子项目
在多模块的项目中，Gradle遵循惯例优于配置 （Convention Over Configuration）原则。
在父项目的根目录下寻找settings.gradle文件，在该文件中设置想要包括到项目构建中的子项目。在构建的初始化阶段（Initialization），Gradle会根据settings.gradle 文件来判断有哪些子项目被include到了构建中，并为每一个子项目初始化一个Project对象，在构建脚本中通过project(‘:sub-project-name’)来引用子项目对应的Project对象。
通常，多模块项目的目录结构要求将子模块放在父项目的根目录下，但是如果有特殊的目录结构，可以在settings.gradle文件中配置。
我所在的项目包括：

   * 一个描述核心业务的core模块
   * 一个遗留的Enterprise Java Bean（enterprise-beans）模块
   * 两个提供不同服务的Web项目（cis-war和admin-war）
   * 一个通过schema生成jaxb对象的jaxb项目以及一个用来用来打ear包的ear项目
   * 一个用于存放项目配置文件相关的config子目录。它不是子模块，所以 config不应该被加到项目的构建中去。

它们都放置在根项目目录下。我们通过如下的settings.gradle来设置项目中的子项目：
include 'core', 'enterprise-beans', 'cis-war', 'admin-war', 'jaxb', 'ear'
我们将需要加入到项目构建中的子项目配置在settings.gradle文件中，而没有加入不需要的config子目录。
1.2  共享配置
在大型Java项目中，子项目之间必然具有相同的配置项。我们在编写代码时，要追求代码重用和代码整洁；而在编写Gradle脚本时，同样需要保持代码重用和代码整洁。Gradle 提供了不同的方式使不同的项目能够共享配置。

   * allprojects：allprojects是父Project的一个属性，该属性会返回该Project对象以及其所有子项目。在父项目的build.gradle脚本里，可以通过给allprojects传一个包含配置信息的闭包，来配置所有项目（包括父项目）的共同设置。通常可以在这里配置IDE的插件，group和version等信息，比如：allprojects {    apply plugin: 'idea'    }
这样就会给所有的项目（包括当前项目以及其子项目）应用上idea插件。
   * subprojects：subprojects和allprojects一样，也是父Project的一个属性，该属性会返回所有子项目。在父项目的build.gradle脚本里，给 subprojects传一个包含配置信息的闭包，可以配置所有子项目共有的设置，比如共同的插件、repositories、依赖版本以及依赖配置：subprojects {    apply plugin: 'java'    repositories {        mavenCentral()    }    ext {          guavaVersion = ’14.0.1’          junitVersion = ‘4.10’    }     dependencies {        compile(                “com.google.guava:guava:${guavaVersion}”        )        testCompile(                “junit:junit:${junitVersion}”        )    }}
这就会给所有子项目设置上java的插件、使用mavenCentral作为 所有子项目的repository以及对Guava[4]和JUnit的项目依赖。此外，这里还在ext里配置依赖包的版本，方便以后升级依赖的版本。
   * configure：在项目中，并不是所有的子项目都会具有相同的配置，但是会有部分子项目具有相同的配置，比如在我所在的项目里除了cis-war和admin-war是web项目之外，其他子项目都不是。所以需要给这两个子项目添加war插件。Gradle的configure可以传入子项目数组，并为这些子项目设置相关配置。在我的项目中使用如下的配置：configure(subprojects.findAll {it.name.contains('war')}) {    apply plugin: 'war'    }
configure需要传入一个Project对象的数组，通过查找所有项目名包含war的子项目，并为其设置war插件。

1.3  独享配置
在项目中，除了设置共同配置之外， 每个子项目还会有其独有的配置。比如每个子项目具有不同的依赖以及每个子项目特殊的task等。Gradle提供了两种方式来分别为每个子项目设置独有的配置。

   * 在父项目的build.gradle文件中通过project(‘:sub-project-name’)来设置对应的子项目的配置。比如在子项目core需要Hibernate的依赖，可以在父项目的build.gradle文件中添加如下的配置：project(‘:core’) {      ext{                   hibernateVersion = ‘4.2.1.Final’      }        dependencies {                 compile “org.hibernate:hibernate-core:${hibernateVersion}”}}
注意这里子项目名字前面有一个冒号（：）。 通过这种方式，指定对应的子项目，并对其进行配置。
   * 我们还可以在每个子项目的目录里建立自己的构建脚本。在上例中，可以在子项目core目录下为其建立一个build.gradle文件，并在该构建脚本中配置core子项目所需的所有配置。例如，在该build.gradle文件中添加如下配置： ext{       hibernateVersion = ‘4.2.1.Final’      }        dependencies {         compile “org.hibernate:hibernate-core:${hibernateVersion}”}

根据我对Gradle的使用经验，对于子项目少，配置简单的小型项目，推荐使用第一种方式配置，这样就可以把所有的配置信息放在同一个build.gradle文件里。例如我同事郑晔 的开源项目moco 。它只有两个子项目，因而就使用了第一种方式配置，在项目根目录下的build.gradle 文件中设置项目相关的配置信息。但是，若是对于子项目多，并且配置复杂的大型项目，使用第二种方式对项目进行配置会更好。因为，第二种配置方式将各个项目的配置分别放到单独的build.gradle文件中去，可以方便设置和管理每个子项目的配置信息。
1.4  其他共享
在Gradle中，除了上面提到的配置信息共享，还可以共享方法以及Task。可以在根目录的build.gradle文件中添加所有子项目都需要的方法，在子项目的build.gradle文件中调用在父项目build.gradle脚本里定义的方法。例如我定义了这样一个方法，它可以从命令行中获取属性，若没有提供该属性，则使用默认值：
def defaultProperty(propertyName, defaultValue) {    return hasProperty(propertyName) ? project[propertyName] : defaultValue}
注意，这段脚本完全就是一段Groovy代码，具有非常好的可读性。
由于在父项目中定义了defaultProperty方法，因而在子项目的build.gradle文件中，也可以调用该方法。
2 . 环境的配置
为了方便地将应用部署到开发、测试以及产品等不同环境上， Gradle提供了几种不同的方式为不同的环境打包，使得不同的环境可以使用不同的配置文件。此外，它还提供了简单的方法，使得我们能够便捷地初始化数据库 。
2.1 Properties 配置
要为不同的环境提供不一样的配置信息，Maven选择使用profile，而Gradle则提供了两种方法为构建脚本提供Properties配置：

   * 第一种方式是使用传统的properties文件， 然后在使用Gradle时，通过传入不同的参数加载不同的properties文件。例如，我们可以在项目中提供development.properties、test.properties和production.properties。在项目运行时，使用-Pprofile=development来指定加载开发环境的配置。构建脚本中加载properties文件的代码如下：ext {    profile = project['profile']}def loadProperties(){    def props = new Properties()    new File("${rootProject.projectDir}/config/${profile}.properties")            .withInputStream {                stream -> props.load(stream)            }    props}
在运行脚本的时候，传入的-Pprofile=development可以指定使用哪个运行环境的配置文件。代码中使用了project['profile']从命令行里读取-P传入的参数，Gradle会去父项目根目录下的config文件夹中需找对应的properties文件。
   * 另外一种方式就是使用Groovy的语法，定义可读性更高的配置文件。比如可以在项目中定义config.groovy的配置文件，内容如下：environments {    development {        jdbc {            url = 'development'            user = 'xxxx'            password = 'xxxx'        }    }    test {        jdbc {            url = 'test'            user = 'xxxx'            password = 'xxxx'        }    }    production {        jdbc {            url = 'production'            user = 'xxxx'            password = 'xxxx'        }    }}
这里定义了三个环境下的不同数据库配置，在构建脚本中使用如下的代码来加载：
ext {    profile = project['profile']}def loadGroovy(){    def configFile = file('config.groovy')    new ConfigSlurper(profile).parse(configFile.toURL()).toProperties()}
这里在ConfigSlurper的构造函数里传入从命令行里取到的-P的参数。调用loadGroovy方法就可以加载项目根目录下的config.groovy文件，并作为一个Map返回，这样就可以通过jdbc.url来获取url的值。

从可读性以及代码整洁（配置文件也需要代码整洁）而言，我推荐使用第二种方式来配置，因为这种方法具有清晰的结构。如上面的例子，就可以把数据库相关的信息都放在jdbc这个大的节点下，而不用像properties文件这样的扁平结构。但是对于一些已经使用properties文件来为不同环境提供配置信息的遗留项目里，使用properties文件也没有问题。
2.2  替换
通过不同的方式加载不同环境的配置后，就需要把它们替换到有占位符的配置文件中去。在配置文件中使用@key@来标注要被替换的位置，比如在config文件夹中有jdbc.properties文件，其内容如下：
jdbc.url=@jdbc.url@jdbc.user=@jdbc.user@jdbc.password=@jdbc.password@
在Gradle构建过程中，有一个processResources的Task，可以修改该Task的配置，让其在构建过程中替换资源文件中的占位符：
processResources {    from(sourceSets.main.resources.srcDirs) {        filter(org.apache.tools.ant.filters.ReplaceTokens,                                tokens: loadGroovyConfig())    }}
上面这种做法用来处理子项目src/main/resources文件夹下的资源文件，所以需要将这段代码放在子项目的独立配置文件里。
在一些复杂的项目中，经常会把配置文件放置到一个目录进行统一管理。比如在我所在的项目，就专门提供了一个config子目录，里面存放了所有的配置信息。在处理这些资源文件时， Gradle默认提供的processResources就不够用了，我们需要在Gradle脚本中定义一个Task去替换这些包含占位符的配置文件，然后让package或者deploy的Task依赖这个Task。该Task的代码如下：
task replace(type: Sync) {            def configHome = "${project.rootDir}/config"    from(configHome) {        include '**/*.properties'        include '**/*.xml'        filter org.apache.tools.ant.filters.ReplaceTokens, tokens: loadGroovyConfig()    }    into "${buildDir}/resources/main"}
这里定义了一个Sync类型的Task，会将父项目的根目录下的config文件夹的所有properties和xml文件使用从loadGroovyConfig()方法中加载出来的配置替换，并将替换之后的文件放到build文件夹下的resource/main目录中。再让打包的Task依赖这个Task，就会把替换之后的配置文件打到包中。
2.3  更复杂的情况
上面介绍了在项目中如何使用Gradle处理 properties和xml文件中具有相同配置，但其中的一些值并不相同的情况 。然而，在有些项目中不同的环境配置之间变化的不仅是值，很有可能整个配置文件都不相同；那么，使用上面替换的处理方式就无法满足要求了。
在我所在的项目中，我们需要依赖一个外部的Web Service。在开发环境上，我们使用了Stub来模拟和Web Service之间的交互，为开发环境提供测试数据，这些数据都放置在一个Spring的配置文件中；而在测试和产品环境上，又要使用对应的测试和产品环境的Web Service。这时，开发、测试与产品环境的配置完全不同。对于这种复杂的情况，Gradle可以在构建过程中为不同的环境指定不同的资源文件夹，在不同的资源文件夹中包含不同的配置文件。
例如，在我们项目的config目录下包含了application文件夹，定义了不同环境所需的不同配置文件，其目录结构如下图所示：



在构建脚本中，根据从命令行读入的-P参数，使用不同的资源文件夹，其代码如下：
sourceSets {    main {        resources {            srcDir "config/application/spring/${profile}",                         "config/application/properties/${profile}"        }    }}
这样在打包的过程中，就可以使用-P传入的参数的资源文件夹下面的properties和xml文件作为项目的配置文件。
2.4  初始化数据库
在项目开发过程中，为了方便为不同环境构建相同的数据库及数据，我们通常需创建数据库的表以及插入一些初始化数据。Gradle目前没有提供相关的Task或者Plugin，但是我们可以自己创建Task去运行SQL来初始化各个环境上的数据库。
前面也提到Gradle是Groovy定义的DSL，所以我们可以在Gradle中使用Groovy的代码来执行SQL脚本文件。在Gradle脚本中，使用Groovy加载数据库的Driver之后，就可以使用Groovy提供的Sql类去执行SQL来初始化数据库了。代码如下：
groovy.sql.Sql oracleSql =         Sql.newInstance(props.getProperty('database.connection.url'),                props.getProperty('database.userid'),                props.getProperty('database.password'),                props.getProperty('database.connection.driver'))try {        new File(script).text.split(";").each {            logger.info it            oracleSql.execute(it)        }    } catch (Exception e) { }
这段代码会初始化执行SQL的groovy.sql.Sql对象，然后按照分号（;）分割SQL脚本文件里的每一条SQL并执行。对于一些必须运行成功的SQL文件，可以在catch块里通过抛出异常来中止数据库的初始化。需要注意的是需要将数据库的Driver加载到ClassPath里才可以正确地执行。
因为在Gradle中包含了Ant，所以我们除了使用Groovy提供的API来执行SQL之外，还可以使用Ant的sql任务 来执行SQL脚本文件。但若非特殊情况，我并不推荐使用Ant任务，这部分内容与本文无关，这里不再细述 。
3 . 代码质量
代码质量是软件开发质量的一部分，除了人工代码评审之外，在把代码提交到代码库之前，还应该使用自动检查工具来自动检查代码，来保证项目的代码质量。下面介绍一下Gradle提供的支持代码检查的插件 。
3.1 CheckStyle 
CheckStyle是SourceForge下的一个项目，提供了一个帮助JAVA开发人员遵守某些编码规范的工具。它能够自动化代码规范检查过程，从而使得开发人员从这项重要却枯燥的任务中解脱出来。Gradle官方提供了CheckStyle的插件 ，在Gradle的构建脚本中只需要应用该插件：
apply plugin: 'checkstyle'
默认情况下，该插件会找/config/checkstyle/checkstyle.xml作为CheckStyle的配置文件，可以在checkstyle插件的配置阶段（Configuration） 设置CheckStyle的配置文件：
checkstyle{configFile = file('config/checkstyle/checkstyle-main.xml')}
还可以通过checkstyle设置CheckStyle插件的其他配置。
3.2 FindBugs 
FindBugs 是一个静态分析工具，它检查类或者 JAR 文件，将字节码与一组缺陷模式进行对比以发现可能的问题。Gradle使用如下的代码为项目的构建脚本添加FindBugs的插件：
apply plugin: 'findbugs'
同样也可以在FindBugs的配置阶段（Configuration）设置其相关的属性，比如Report的输出目录、检查哪些sourceSet等。
3.3 JDepend 
在开发Java项目时经常会遇到关于包混乱的问题， JDepend工具可以帮助你在开发过程中随时跟踪每个包的依赖性（引用/被引用），从而设计高维护性的架构，不论是在打包发布还是版本升级都会更加轻松。在构建脚本中加入如下代码即可：
apply plugin: 'jdepend'3.4 PMD 
PMD是一种开源分析Java代码错误的工具。与其他分析工具不同的是，PMD通过静态分析获知代码错误，即在不运行Java程序的情况下报告错误。PMD附带了许多可以直接使用的规则，利用这些规则可以找出Java源程序的许多问题。此外，用户还可以自己定义规则，检查Java代码是否符合某些特定的编码规范。在构建脚本中加入如下代码：
apply plugin: 'pmd'3.5  小结
上面提到的几种代码检查插件apply到构建脚本之后，可以运行：
gradle check
来执行代码质量检查。更详细的信息请查阅Gradle的官方文档 。运行结束后会在对应的项目目录下的build文件夹下生成report。
对于Gradle没有提供的代码检查工具，我们可以有两种选择：第一就是自己实现一个Gradle插件 ，第二就是调用Ant任务，让Ant作为一个媒介去调用在Ant中已经有的代码检查工具，比如测试覆盖率的Cobertura 。我们的项目使用了Ant来调用Cobertura，但是为了使用方便，我们将它封装为一个Gradle插件，这样就可以在不同的项目里重用。
几乎每个Java项目都会用到开源框架。同时，对于具有多个子模块的项目来说，项目之间也会有所依赖。所以，管理项目中对开源框架和其他模块的依赖是每个项目必须面对的问题。同时，Gradle也使用Repository来管理依赖。
4.1 Jar 包依赖管理
Maven提出了使用Repository来管理Jar包，Ant也提供了使用Ivy来管理jar包。Gradle提供了对所有这些Respository的支持，可以从Gradle的官方文档上了解更详细的信息。
Gradle沿用Maven的依赖管理方法，通过groupId、name和version到配置的Repository里寻找指定的Jar包。同样，它也提供了和Maven一样的构建生命周期，compile、runtime、testCompile和testRuntime分别对应项目不同阶段的依赖。通过如下方式为构建脚本指定依赖：
dependencies {    compile group: 'org.hibernate', name: 'hibernate-core', version: '3.6.7.Final'    testCompile group:'junit', name: 'junit', version '4.11'}
这里分别指定group、name以及version，但是Gradle提供了一种更简单的方式来指定依赖：
dependencies {    compile 'org.hibernate:hibernate-core:3.6.7.Final'    testCompile 'junit:junit:4.11'}
这样比Maven使用XML来管理依赖简单多了，但是还可以更简单一点。实际上这里的compile和testCompile是Groovy为Gradle提供的方法，可以为其传入多个参数，所以当compile有多个Jar包依赖的时候，可以同时指定到compile里去，代码如下：
compile(               'org.hibernate:hibernate-core:3.6.7.Final',            'org.springframework:spring-context:3.1.4.RELEASE')
另外，当在Respository无法找到Jar包时（如数据库的driver），就可以将这些Jar包放在项目的一个子目录中，然后让项目管理依赖。例如，我们可以在项目的根目录下创建一个lib文件夹，用以存放这些Jar包。使用如下代码可以将其添加到项目依赖中：
dependencies {    compile(               'org.hibernate:hibernate-core:3.6.7.Final',            'org.springframework:spring-context:3.1.4.RELEASE',               fileTree(dir: "${rootProject.projectDir}/lib", include: '*.jar'))}4.2  子项目之间的依赖
对于多模块的项目，项目中的某些模块需要依赖于其他模块，前面提到在初始化阶段，Gradle为每个模块都创建了一个Project对象，并且可以通过模块的名字引用到该对象。在配置模块之间的依赖时，使用这种方式可以告诉Gradle当前模块依赖了哪些子模块。例如，在我们的项目中，cis-war会依赖core子项目，就可以在cis-war的构建脚本中加上如下代码：
dependencies {    compile(               'org.hibernate:hibernate-core:3.6.7.Final',             project(':core'))}
通过project(':core')来引用core子项目，在构建cis-war时，Gradle会把core加到ClassPath中。
4.3  构建脚本的依赖
除了项目需要依赖之外，构建脚本本身也可以有自己的依赖。当使用一个非Gradle官方提供的插件时，就需要在构建脚本里指定其依赖，当然还需要指定该插件的Repository。在Gradle中，使用buildscript块为构建脚本配置依赖。
比如在项目中使用cucumber-JVM 作为项目BDD工具，而Gradle官方没有提供它的插件，好在开源社区有人提供cucumber的插件 。在构建脚本中添加如下代码：
buildscript {    repositories {        mavenCentral()    }    dependencies {        classpath "gradle-cucumber-plugin:gradle-cucumber-plugin:0.2"    }}apply plugin: com.excella.gradle.cucumber.CucumberPlugin5.1 apply其他Gradle 文件
当一个项目很复杂的时候，Gradle脚本也会很复杂，除了将子项目的配置移到对应项目的构建脚本之外，还可以可以按照不同的功能将复杂的构建脚本拆分成小的构建脚本，然后在build.gradle里使用apply from，将这些小的构建脚本引入到整体的构建脚本中去。比如在一个项目中既使用了Jetty，又使用了Cargo插件启动JBoss，就可以把他们分别提到jetty.gradle和jboss.gradle，然后在build.gradle里使用如下的代码将他们引入进来：
apply from: "jetty.gradle"apply from: "jboss.gradle"5.2 project 的目录
在脚本文件中，需要访问项目中的各级目录结构。Gradle为Project对象定义了一些属性指向项目的根目录，方便在脚本中引用。

   * rootDir：在子项目的脚本文件中可以通过该属性访问到根项目路径。
   * rootProject：在子项目中，可以通过该属性获取父项目的Project 对象。

5.3 使用Wrapper指定Gradle 的版本
为了统一项目中Gradle的版本，可以在构建脚本中通过定义一个wrapper的Task，并在该Task中指定Gradle的版本以及存放Gradle的位置。
task wrapper(type: Wrapper) {    gradleVersion = '1.0'    archiveBase = 'PROJECT'    archivePath = 'gradle/dists'}
运行gradle wrapper， 就会在根项目目录下创建一个wrapper的文件夹，会包含wrapper的Jar包和properties文件。之后就可以使用gradlew来运行task。第一次使用gradlew执行task的时候，会在项目根目录下的gradle/dists下下载你指定的Gradle版本 。这样在项目构建的时候，就会使用该目录下的Gradle，保证整个团队使用了相同的Gradle版本。
5.4 使用gradle.properties 文件
Gradle构建脚本会自动找同级目录下的gradle.properties文件，在这个文件中可以定义一些property，以供构建脚本使用。例如，我们要使用的Repository需要提供用户名和密码，就可以将其配置在gradle.properties中。这样，每个团队成员都可以修改该配置文件，却不用上传到代码库中对团队其他成员造成影响。可以使用如下的代码定义：
username=userpassword=password
在构建脚本中使用"${username} "就可以访问该文件中定义的相关值。
由于篇幅有限，本文只是我在一个大型Java项目上使用Gradle的部分经验，并未涵盖所有Gradle相关的知识，包括如何编写Gradle插件以及Gradle对其他语言的构建，读者可以通过阅读Gradle的官方文档 （比起其他开源软件，Gradle的另一特点就是文档详细）来了解。另外，Gradle是基于Groovy的构建工具，在使用Gradle的时候也需要了解和使用Groovy。所以，在学习Gradle插件的过程中，也能学会Groovy相关的用法，可谓一举两得。
参考文献:
[1] CoC: http://en.wikipedia.org/wiki/Convention_over_configuration
[2] DSL: http://en.wikipedia.org/wiki/Domain-specific_language
[3] Micro Service Architecture: http://yobriefca.se/blog/2013/04/29/micro-service-architecture/
[4] Guava: https://code.google.com/p/guava-libraries/
作者介绍：何海洋，Thoughtworks咨询师，毕业于大连海事大学，有多年软件开发经验，主要从事Java项目的开发。目前在Thoughtworks公司从事敏捷软件开发。
感谢张逸 对本文的审校。
给InfoQ中文站投稿或者参与内容翻译工作，请邮件至editors@cn.infoq.com 。也欢迎大家通过新浪微博（@InfoQ ）或者腾讯微博（@InfoQ ）关注我们，并与我们的编辑和其他读者朋友交流。
告诉我们您的想法


刚刚将接手的一个项目从 Gradle 转换到 Maven 七月 09, 2013 06:21 by Bai Hantsy
刚刚将接手的一个项目从 Gradle 转换到 Maven，目前对企业级开发，Maven 插件如山， Gradle 在这方面连 Ant 都不如。

Gradle 唯一可以比 Ant 强点就是使用 Groovy 直接写一些自定义的任务，这对于熟悉 Groovy 的人有点用。对于不熟悉的人是鸡肋。

对于那一套Build生命周期， Maven 已经太成熟了。 Ant 下Ivy 相关子项目也在开始这方面的工作。

Gradle是以后的趋势 七月 23, 2013 12:43 by Fu Cheng
Maven已经是比较过时的技术了，基于XML的配置方式实在是过于繁琐。Maven的确有很多out-of-box的插件，但是问题在于Maven可以很好的处理80%的情况，剩下的20%如果你需要自定义的话，会非常的复杂。这点上我觉得Gradle要好很多。Gradle是给程序员用的，而Maven更多的是给配置管理人员用的。Spring和Hibernate等开源软件都已经切换到Gradle了。 