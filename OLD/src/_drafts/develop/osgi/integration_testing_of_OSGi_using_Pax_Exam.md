---
layout: post
title: "Tycho：用Maven构建Eclipse Plugin项目"
description: "Tycho以一组maven插件的形式，支持Eclipse的plug-ins, features, update sites (based on p2) 、products等类型工程的构建。"
category: 软件开发
tags: [eclipse, maven]
lastmod: 
---


# OSGi测试之痛

测试OSGi应用是非常痛苦的。OSGi应用的测试，一般是基于OSGi容器，针对多个bundle进行[集成测试](/2014/01/06/integration_tests_within_spring.html#menuIndex0)。需要解决bundle之间的依赖关系，
并按照一定的启动顺序在OSGi容器中加载各个bundle。

在非OSGi环境，依赖关系可以通过Maven解决，而且在一个`ClassLoader`之下，没有“启动顺序”的问题。
由于OSGi与Maven的阻抗不匹配，尽管[Tycho支持用Maven构建OSGi应用](/2014/01/08/build_osgi_bundle_with_tycho_maven_plugin.html)，



OSGi集成测试的困难：
 - 定义一大串的依赖关系
- 对组件的启动顺序有要求

1. 创建一个maven工程


# PaxExam: 容器内测试框架

Spring-test也是一个容器内测试框架

spring的osgi测试比较麻烦
spring已经放弃osgi


[PaxExam](https://ops4j1.jira.com/wiki/display/PAXEXAM3/Pax+Exam)是一个“容器内测试框架（In-Container Testing Framework）”。最初，PaxExam只支持OSGi容器的测试，从3.0开始，已经扩展到了OSGi、
Java EE、CDI([JSR-299]():Contexts and Dependency Injection for the Java EE platform)等容器环境。

