---
layout: post
title: "Tycho：用Maven构建Eclipse Plugin项目"
description: "Tycho以一组maven插件的形式，支持Eclipse的plug-ins, features, update sites (based on p2) 、products等类型工程的构建。"
category: 软件开发
tags: [OSGi, maven]
lastmod: 
---



[Tycho](http://www.sonatype.org/tycho)是一个Maven插件，目标是使用Maven构建Eclipse插件，OSGI Bundle等工程。

如果说[Maven](http://maven.apache.org/)的出现是一群Java程序员受不了繁琐的插件依赖管理，受不了冗长的ant build.xml文件而创造出来的，
那Tycho则是一群Eclipse、OSGi插件开发人员受不了重复地配置类似的Maven pom.xml而创造出来的。

Tycho以一组maven插件的形式，支持Eclipse的plug-ins, features, update sites (based on p2) 、products等类型的工程，
表现为不同的maven打包类型(packaging):

- eclipse-plugin
- eclipse-feature
- eclipse-test-plugin
- eclipse-repository
- eclipse-target-definition


# 父工程

基于OSGi的工程通常会划分很多模块，对于Maven来说，一般通过一个父工程（parent）来管理所有模块的构建。父工程的`packaging`类型为`pom`.

为了使用Tycho，需要在父工程的pom文件中增加一些配置。

## 增加Tycho插件

父工程中定义的插件可以在所有子工程中使用：

```
  <properties>
    <tycho-version>0.16.0</tycho-version>
  </properties>

  <build>
    <plugins>
      <plugin>
        <groupId>org.eclipse.tycho</groupId>
        <artifactId>tycho-maven-plugin</artifactId>
        <version>${tycho-version}</version>
        <extensions>true</extensions>
      </plugin>
    </plugins>
  </build>
```

## 定义bundle仓库

比如，基于Eclipse 4.3(Kepler)的RCP应用，使用了Texo、GeminiJPA等插件，需要如下的仓库定义：

```
  <repositories>
    <repository>
      <id>Kepler</id>
      <url>http://download.eclipse.org/releases/kepler</url>
      <layout>p2</layout>
    </repository>
    <repository>
      <id>Texo</id>
      <url>http://download.eclipse.org/modeling/emft/texo/updates/interim</url>
      <layout>p2</layout>
    </repository>
    <repository>
      <id>GeminiJPA</id>
      <url>http://download.eclipse.org/gemini/jpa/updates</url>
      <layout>p2</layout>
    </repository>
    <repository>
      <id>EclipseLink</id>
      <url>http://download.eclipse.org/rt/eclipselink/updates/</url>
      <layout>p2</layout>
    </repository>
  </repositories>
```  

## 定义目标

定义不同的目标平台：


```
  <plugin>
    <groupId>org.eclipse.tycho</groupId>
    <artifactId>target-platform-configuration</artifactId>
    <configuration>
      <environments>
        <environment>
          <os>linux</os>
          <ws>gtk</ws>
          <arch>x86</arch>
        </environment>
        <environment>
          <os>macosx</os>
          <ws>cocoa</ws>
          <arch>x86_64</arch>
        </environment>
      </environments>
    </configuration>
  </plugin>
```

如果要发布比较复杂的目标，比如Eclipse Product的发布，需要单独构建`eclipse-target-definition`类型的子工程。


# 为现有工程生成pom

Tycho提供了一个工具，可以为现有的Eclipse Plugin、Feature等工程生成pom文件，从而将其整合到Tycho的管理之下。

该工具也是基于maven的，只需要在工程文件夹执行命令：

```
    mvn org.eclipse.tycho:tycho-pomgenerator-plugin:generate-poms -DgroupId=thinkinside.tangle
```

生成的pom文件举例如下：

```
  <?xml version="1.0" encoding="UTF-8"?>  
  <project xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd" xmlns="  http://maven.apache.org/POM/4.0.0"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <modelVersion>4.0.0</modelVersion>
    <groupId>thinkinside.tangle</groupId>
    <artifactId>tangle-app</artifactId>
    <version>1.0.0-SNAPSHOT</version>
    <packaging>eclipse-plugin</packaging>
  </project>
```

由于种种原因，Eclipse Plugin工程的配置内容分散在多个文件中，包括：

- OSGi的配置文件：MANIFEST.MF
- 插件工程构建文件：build.properties
- 插件定义文件：plugin.xml
- 产品描述文件：.product

这些文件中的配置项有重复，开发人员要保证各文件中的相关配置的一致性。

Tycho在生成pom文件时，会检查这些配置文件，将其中的配置项写入pom文件中。

Tycho的逻辑是以上述标准的配置文件优先。比如，在pom文件中没有定义依赖关系，而是以`MANIFEST.MF`中定义的依赖为准。


如果现有工程已经有了pom文件，还可以使用Tycho进行更新：

```
  mvn org.eclipse.tycho:tycho-versions-plugin:update-pom -Dtycho.mode=maven
```

# "目标定义"子工程

前面提到，如果要发布比较复杂的目标，比如Eclipse Product的发布，需要单独构建`eclipse-target-definition`类型的子工程。

在"目标定义"子工程中创建`.product`文件，然后在pom文件中添加：

```
  <build>
    <plugins>
      <plugin>
        <groupId>org.eclipse.tycho</groupId>
        <artifactId>tycho-p2-director-plugin</artifactId>
        <version>${tycho-version}</version>
        <executions>
          <execution>
            <!-- install the product for all configured os/ws/arch environments 
              using p2 director -->
            <id>materialize-products</id>
            <goals>
              <goal>materialize-products</goal>
            </goals>
          </execution>
          <!-- (optional) create product zips (one per os/ws/arch) -->
          <execution>
            <id>archive-products</id>
            <goals>
              <goal>archive-products</goal>
            </goals>
          </execution>



        </executions>
      </plugin>
    </plugins>
  </build>
```


"目标定义"子工程中还可以使用”目标定义文件（Target Definition, *.target）“进行复杂的配置。
可以参考[这里](http://wiki.eclipse.org/Tycho/Target_Platform)的说明，也可以查看[GitHub上的例子](https://github.com/toedter/e4-tutorial)的例子。



# Test工程

与专门的测试工具[Pax Exam]()相比，Tycho test使用起来会更简单。当然前提是测试由Tycho构建的OSGi应用。

Tycho将一个"Fragment"工程包装成Maven工程，可以在其中编写测试代码，然后使用"JUnit Plug-in Test"执行测试。

# 对比Maven-Bundle-Plugin

Maven-Bundle-Plugin提供了与Tycho不同风格的另一种构建OSGi的maven插件。关于二者的对比，可以参考[这里](/2014/01/21/tycho_vs_maven_bundle_plugin.html)
