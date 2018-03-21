---
layout: post
title: "OSGi构建工具：Tycho还是Maven-Bundle-Plugin？"
description: ""
category: 软件开发
tags: [OSGi, maven]
lastmod: 
---

# Tycho与Maven-Bundle-Plugin的对比

Maven与OSGi天生就是冤家：Maven通过`pom.xml`描述一个产物的全部，而OSGi将这项工作交给了`MANIFEST.MF`。

如果仅仅是一些定义信息还好说，但是Maven和OSGi都希望能够描述产物的依赖关系，在使用Maven开发OSGi bundle的时候，就导致了一个问题：

依赖关系到底是在`pom.xml`中描述，还是在`MANIFEST.MF`中描述？

[前面提到的Tycho](/2014/01/08/build_osgi_bundle_with_tycho_maven_plugin.html)的思路是由`MANIFEST.MF`自行管理bundle的依赖关系，`pom.xml`只记录使用maven进行构建时需要的信息，比如maven工程的父子关系、打包时需要的bundle仓库及要发布的目标平台等。

Tycho的这种机制对Eclipse IDE比较友好，在开发期间完全使用IDE的机制进行开发和调试，只有在打包部署时才依赖maven。



[Apache Felix Maven-Bundle-Plugin](http://felix.apache.org/site/apache-felix-maven-bundle-plugin-bnd.html)
则使用另一套机制：使用Maven-Bundle-Plugin，在开发时可以没有`MANIFEST.MF`文件！Maven-Bundle-Plugin在`pom.xml`中复制了一套`MANIFEST.MF`的元数据，完全可以通过`pom.xml`文件中的定义生成出完整的`MANIFEST.MF`文件。

Maven-Bundle-Plugin的这种机制使得工程完全的”maven化”，更适合传统非OSGi开发人员的使用习惯。但是无法很好的利用IDE的开发和调试功能，比如，你可能需要自己搭建一个运行环境从IDE中调用。


两种方式可谓各有千秋。但是Tycho明显基于Equniox和Eclipse，比如，Tycho可以配置Eclipse p2站点作为bundle库。如果要使用Tycho开发和调试Felix，需要搭建一个Eclipse风格的p2站点，将Felix runtime和需要的各种bundle都放到该站点中并发布，然后[在Tycho中引用该站点](/2014/01/08/build_osgi_bundle_with_tycho_maven_plugin.html#menuIndex2)。更详细的说明可以参考[这里](http://vzurczak.wordpress.com/2013/02/27/a-target-platform-based-on-apache-felix/)。

而Felix Maven-Bundle-Plugin对于各种OSGi runtime的支持是相同的，由于完全基于maven，使用任何IDE开发bundle的效果都差不多。通常，Felix系的平台，如Karaf、Geronimo、Camel、ServiceMix、Fuse等，其例子都是使用Maven-Bundle-Plugin构建的。

由于[前文已经说明了如何用Tycho开发OSGi](/2014/01/08/build_osgi_bundle_with_tycho_maven_plugin.html)，下面只给出使用Maven-Bundle-Plugin的例子。


# Maven-Bundle-Plugin的pom例子

```
 <project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
	<modelVersion>4.0.0</modelVersion>
	<groupId>thinkinside.demo.osgi</groupId>
	<artifactId>simple-bundle</artifactId>
	<version>0.0.1-SNAPSHOT</version>


	<build>
		<plugins>
			<plugin>
				<groupId>org.apache.felix</groupId>
				<artifactId>maven-bundle-plugin</artifactId>
				<executions>
					<execution>
						<id>generate-resources</id>
						<goals>
							<goal>manifest</goal>
						</goals>

						<configuration>
							<instructions>
								<Bundle-Name>${project.name}</Bundle-Name>
								<Bundle-SymbolicName>${project.artifactId}</Bundle-SymbolicName>
								<Bundle-Activator>test.bundle.internal.Activator</Bundle-Activator>
								<Export-Package>***</Export-Package>
            					<Import-Package>***</Import-Package>
            					<Private-Package>***</Private-Package>
            				</instructions>
						</configuration>
					</execution>
				</executions>
			</plugin>

			<plugin>
				<groupId>org.apache.maven.plugins</groupId>
				<artifactId>maven-jar-plugin</artifactId>
				<version>2.3.1</version>
				<configuration>
					<archive>
						<manifestFile>${project.build.outputDirectory}/META-INF/MANIFEST.MF</manifestFile>
					</archive>
				</configuration>
			</plugin>
		</plugins>
	</build>

	<dependencies>
		<dependency>
			<groupId>org.apache.felix</groupId>
			<artifactId>org.osgi.core</artifactId>
			<version>1.4.0</version>
		</dependency>
	</dependencies>
 </project>
```

使用Maven-Bundle-Plugin构建bundle，就是构建一个简单的jar。不同之处在于：要通过pom.xml中的信息生成符合OSGi要求的`MANIFEST.MF`文件并打包到jar中。这通过两个插件来完成：

- org.apache.felix:maven-bundle-plugin

  在项目生命周期的"generate-resources"阶段，根据`<instructions>`标签内定义的信息生成`MANIFEST.MF`文件。这里可以配置OSGi所需要的全部元数据。

- org.apache.maven.plugins:maven-jar-plugin

  配置其在打包是使用前面生成的`MANIFEST.MF`文件

由于OSGi bundle通常会使用OSGi API，这里添加了org.apache.felix:org.osgi.core的依赖。当然也可以换成其他的OSGi运行时，比如Equinox。

此时，使用`mvn package`生成的jar包中，`MANIFEST.MF`文件内已经添加了配置好的bundle信息。

当然，使用[maven-bundle-plugin的目标(Goals)](http://svn.apache.org/repos/asf/felix/releases/maven-bundle-plugin-2.3.7/doc/site/index.html)
可以进行更细致的控制。

# 在Eclipse中运行和调试

本来，传说中的[Pax Cursor](http://wiki.ops4j.org/confluence/display/ops4j/Pax%20Cursor)可以在Eclipse中基于各种OSGi runtime运行和调试bundle，但是天朝的网络中似乎不存在`ops4j.org`这个域名。

好在我们可用一个Java Project的方式建立起Felix的环境，通过Eclipse对bundle进行运行和调试。
由于[这里](http://felix.apache.org/site/integrating-felix-with-eclipse.html)有非常详细的说明，故不再赘述。

其实，我们还可以基于maven构建，而不是使用Java Project的方式。使用maven的好处是这种方法可以用于任何支持maven的IDE。

Felix runtime的主要内容包括：

![](/images/fuse/felix-tree.png)

其中：

- bin/felix.jar  启动的jar, MainClass是`org.apache.felix.main.Main`
- bundle/	存放可用的bundle，Felix runtime中内置了4个必需的bundle
- conf/conf.properties 启动配置。类似于Eclipse的`configuration/config.ini`。Felix配置项可以参考[官方网站中的内容](http://felix.apache.org/site/apache-felix-framework-configuration-properties.html)

知道了Felix runtime的构成，就可以用maven构建出相同的结构，并插入到项目周期的适当位置。pom如下：

```
 <project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
	<modelVersion>4.0.0</modelVersion>
	<groupId>thinkinside.demo.fuse</groupId>
	<artifactId>felix-launcher</artifactId>
	<version>0.0.1-SNAPSHOT</version>
	<name>Felix Launcher</name>
	<properties>
		<felix.bundlerepository.version>1.6.4</felix.bundlerepository.version>
		<felix.gogo.version>0.10.0</felix.gogo.version>
		<felix.framework.version>4.2.1</felix.framework.version>
	</properties>

	<build>
		<plugins>
			<plugin>
				<artifactId>maven-clean-plugin</artifactId>
				<version>2.4.1</version>
				<configuration>
					<filesets>
						<fileset>
							<directory>bundle</directory>
						</fileset>
					</filesets>
				</configuration>
			</plugin>

			<plugin>
				<groupId>org.apache.maven.plugins</groupId>
				<artifactId>maven-dependency-plugin</artifactId>
				<version>2.2</version>
				<executions>
					<execution>
						<id>copy</id>
						<phase>generate-resources</phase>
						<goals>
							<goal>copy</goal>
						</goals>
						<configuration>
							<artifactItems>
								<artifactItem>
									<groupId>org.apache.felix</groupId>
									<artifactId>org.apache.felix.gogo.command</artifactId>
									<version>${felix.gogo.version}</version>
								</artifactItem>
								<artifactItem>
									<groupId>org.apache.felix</groupId>
									<artifactId>org.apache.felix.gogo.runtime</artifactId>
									<version>${felix.gogo.version}</version>
								</artifactItem>
								<artifactItem>
									<groupId>org.apache.felix</groupId>
									<artifactId>org.apache.felix.gogo.shell</artifactId>
									<version>${felix.gogo.version}</version>
								</artifactItem>
								<artifactItem>
									<groupId>org.osgi</groupId>
									<artifactId>org.osgi.compendium</artifactId>
									<version>4.2.0</version>
								</artifactItem>
							</artifactItems>
							<outputDirectory>bundle</outputDirectory>
						</configuration>
					</execution>
				</executions>
			</plugin>
		</plugins>
		
	</build>

	<dependencies>
		<dependency>
			<groupId>org.apache.felix</groupId>
			<artifactId>org.apache.felix.main</artifactId>
			<version>${felix.framework.version}</version>
		</dependency>

		<dependency>
			<groupId>org.ops4j.pax.url</groupId>
			<artifactId>pax-url-assembly</artifactId>
			<version>1.6.0</version>
		</dependency>
	</dependencies>
 </project>
```

该pom在标准的生命周期中增加了两项工作：

- 在`generate-resources`阶段，创建bundle文件夹，复制必需的4个bundle
- 在`clean`阶段，清除bundle文件夹


最后，还需要一个配置文件。在工程目录建立`/conf/config.properties`文件，并进行基本配置：

```
felix.auto.deploy.action=install,start
felix.log.level=1
 
org.osgi.framework.storage.clean=onFirstInit
```

配置完成了，先执行`mvn compile`生成需要的资源。此时使用命令`mvn exec:java -Dexec.mainClass="org.apache.felix.main.Main"`即可以启动Felix runtime：

![](/images/fuse/felix_launch_from_maven.png)

在Eclipse中，将这个工程作为`Java Application`运行，选择`org.apache.felix.main.Main`作为Main Class，就可以进行运行和调试。



