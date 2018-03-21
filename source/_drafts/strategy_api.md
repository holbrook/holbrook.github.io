---
title: 交易策略接口设计
date: 2018-03-09
postslug: strategy_api
category: 量化交易
tags: 交易系统
---

国内开源的量化交易平台，或多或少都参考了 [quantopian](https://www.quantopian.com)。
这是一个不错的起点，可以少走很多弯路。

本文介绍一个 C# 策略平台的 API 设计。

{% plantuml %}

interface Strategy {
    void Initialize(StrategyContext ctx, dynamic config)
    void Start(IStrategyContext ctx)
    void Stop(IStrategyContext ctx)
}

interface StrategyContext {
    String[] Codes {get;}
}

Strategy -- StrategyContext

{% endplantuml %}

# 策略和上下文

策略可能会运行在单独的线程中，对策略的生命周期也需要进行管理。而为了简化策略的开发，
策略不知道自己运行环境的具体信息，只能通过上下文对环境进行有限的访问。

为了方便策略调用，策略容器每次调用策略的方法时，都将上下文作为一个参数传入。

策略可以通过上下文获取模型数据

# 账户模型

{% plantuml %}

class Portfolio {
   
}

class Account {
    
}

Portfolio -- "*" Position
Account -- "*" Position
Position -- Instrument

{% endplantuml %}

# 策略生命周期

平台通过容器控制策略的初始化、启动、停止等行为。

- void Initialize(StrategyContext ctx, dynamic config)
- void Start(IStrategyContext ctx)
- void Stop(IStrategyContext ctx)

