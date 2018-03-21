---
title: Order颜色
date: 2018-03-08
postslug: order_color
category: 
tags: 
---

{% plantuml %}

skinparam state {
    BackgroundColor<<BeforeQuote>> DarkGreen
    BackgroundColor<<Quoted>> Green
    BackgroundColor<<Partical>> Yellow
    BackgroundColor<<Failed>> Red
    BackgroundColor<<BeforeCancel>> Blue
    BackgroundColor<<Cancelled>> LightBlue
}

state 交易者触发 {
    [*] --> 待报 <<BeforeQuote>> : 提交委托
    [*] --> 待撤 <<BeforeCancel>> : 提交撤单指令
}

state 中间环节触发 {
    待报 --> 正报 <<BeforeQuote>>: 收到交易者委托
    待撤 --> 正撤 <<BeforeCancel>>: 收到撤单指令
}

state 交易所触发 {
    正报 --> ===撮合===
    ===撮合=== --> 已报 <<Quoted>>
    ===撮合=== --> 废单 <<Failed>>
    ===撮合=== --> 部成 <<Partical>>
    ===撮合=== --> 已成 <<Failed>>
    部成 --> 已成
    已报 --> 部成
    已报 --> 已成

    正撤 --> ===撤销===
    ===撤销=== --> 部撤 <<Cancelled>>
    ===撤销=== --> 已撤 <<Cancelled>>
    ===撤销=== --> 撤废 <<Failed>>
    部撤 --> 已撤
}

{% endplantuml %}