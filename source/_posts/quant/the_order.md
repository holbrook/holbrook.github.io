---
title: 交易系统中的订单(Order)
postslug: the_order
category: 量化交易
tags: 交易系统
date: 2018-02-06
---

思考设计量化交易系统的订单(Order)时，要考虑的因素。并给出一个概念模型。

<!--more-->

# 委托和订单

除了“红马甲”，大多数交易者并不能直接将交易指令提交到交易所，而是需要经过中间环节代为处理。
即交易者提出“委托申请”，中间商将委托提交到交易所形成"订单(Order)"。

为了区分订单，交易所会为每一笔订单分配一个合同号(Order ID)。

在交易所撮合的过程中，订单的状态不断变化，交易者根据订单状态了解自己的委托是否成交。

# 订单状态 OrderStatus

由于要经过交易者、中间环节、交易所三级的处理，需要有很多状态区分订单处于哪个阶段。
目前国内的交易系统中，订单状态主要区分为一下几种：

- 待报: 也称为“未报”，交易者提交委托后的初始状态
- 正报: 中间环节已经收到委托，但还未报到交易所，或者虽然报到交易所但是没有收到交易所的委托确认
- 已报: 交易所确认委托
- 部成: 经过撮合，订单部分成交
- 已成: 经过撮合，订单全部成交
- 废单: 交易所认定订单无效

- 待撤: 交易者提交撤单指令
- 正撤: 中间环节收到撤单指令，但还未报到交易所，或者未收到交易所的确认
- 部撤: 订单部分成交，部分撤销
- 已撤: 订单全部撤销
- 撤废: 无法撤单，通常是因为已经撮合成交

有些系统中，`待撤`会根据当前成交状态，进一步细分为 `已报待撤`和`部成待撤`。

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


# 订单方向 TradeSide

对于A股，只有买入(BUY)和卖出(SELL)，其他市场还有一些别的方式。
常见的包括以下几种：

- BUY: 买入开仓(证券买入)
- SELL: 卖出平仓(证券卖出)
- SHORT: 卖出开仓
- COVER: 买入平仓
- SELLTODAY: 卖出平今仓
- COVERTODAY: 买入平今仓

# 委托方式

按照委托价格的指定方式，可以分为限价委托(LimitOrder)和市价委托(MarketOrder)。
其中，市价委托又分为几种方式。

- 限价委托(LMT, limit), 以指定的价格报单

- 对手方最优价格委托（BOC, best of counterparty)

  如果有对手方报价，则以买一/卖一价格成交，未能完全成交的按成交价转为限价单；
  如果没有对手方报价，自动撤单。

- 本方最优价格委托(BOP, best of party)

  如果有买一/买一价格，则跟随报价；如果没有自动撤单。

- 即时成交剩余撤销委托(ITC, immediately then cancel)

  自动追涨买入/杀跌卖出，直到涨停/跌停。还有剩余的自动撤单。

- 最优五档即时成交剩余撤销委托(B5TC, best 5 then cancel)

  是对ITC的改进，只与对手方的前五档价格成交。

- 全额成交或撤销委托(FOK, fill or kill)

  类似ITC，但是不用指定数量，自动全仓操作

- 最优五档剩余转限价委托(B5TL,best 5 then limit)

  类似B5TC, 区别是剩余的不撤单，而是转为限价

目前，深交所支持 LMT, BOC, BOP, ITC, B5TC, FOK；上交所支持LMT、B5TC、B5TL。

除了 LimitOrder和 MarketOrder，有些交易所/交易系统(如CTP,文华)还支持其他类型的委托，比如：

- Stop Orders (STP, stop-loss order) 市价止损/止盈单

  Stop orders are similar to market orders in that they are orders to buy or sell an asset at the best available price, but these orders are only processed if the market reaches a specific price.

  For example, if the current price of an asset is 1.2567, a trader might place a buy stop order with a price of 1.2572. If the market trades at 1.2572 or above, the trader's stop order will be processed as a market order, and will then get filled at the current best price.

  Stop orders are processed as market orders, so if the stop (or trigger) price is reached, the order will always get filled, but not necessarily at the price that the trader intended. Stop orders will trigger if the market trades at or past the stop price. For a buy order, the stop price must be above the current price, and for a sell order, the stop price must be below the current price.

  Stop orders can be used to enter a trade, but also used to exit a trade, typically called a stop loss. For example, if a trader buys a stock at$50.50, they may place a sell stop at$50.25.

  If the price reaches$50.25 or below, the sell order will be executed, getting the trader out of the position at$50.25 (or below), limiting the loss on the position. If a trader is short at$50.50, they may place a buy stop at$50.75 to limit their loss. If the price reaches$50.75 (or above) the buy stop will execute, closing the trader's position at$50.75 or above.

- Stop Limit Orders (STPLMT) 限价止损/止盈单

  Traders will commonly combine a stop and a limit order to fine-tune what price they get. To open a trade, a trader could place a buy stop limit at$50.75. Assume the stock currently trades at$50.50. If the price reaches$50.75 the buy stop limit order will be executed, but only if the order can executed at$50.75 or below. This also works to initiate a short positions. If the current price is$25.25, and a trader wants to go short if the price falls to$25.10, they could place a sell stop limit at$25.10. If the price reaches$25.10 the order will be executed, but only if the order can be executed$25.10 or above.

  When using a stop limit order, the stop and limit prices of the order can be different. For the buying example, our trader could place a buy stop at$50.75, but with a limit at$50.78. The buy stop kicks in and buys if$50.75 is reached, but due to the limit order, the order will only buy up to$50.78. This assures that the trader buys if$50.75 is reached, but only if the market allows them to do so below$50.78.

  Stop limit orders will remain pending until someone else is willing to transact at the stop limit order price(s), or better.

- Market If Touched Orders (MIT)

  A buy MIT order price is placed below the current price, while the sell MIT order price is placed above the current price. For example, assume a stock is trading at$16.50. A MIT buy order could be placed at$16.40. If the price moves to$16.40 or below--the trigger price--then an market buy order will be sent out.

  For a sell order, assume a stock is trading$16.50. An MIT sell order could be place at$16.60. If the price moves to$16.60--the trigger price--than a market sell order be sent out.

- Limit If Touched Orders (LIT)

  A LIT is like a MIT order, but it sends out a limit order instead of a market order. For a LIT order there is a trigger price, and a limit price.

  For example, assume a stock is trading at$16.50. A LIT trigger could be placed at$16.40. In addition, a limit price of$16.35 could be set. If the price moves to$16.40 or below--the trigger price--then a limit order will be placed at$16.35. Since it is a limit order, the buy will only be executed at$16.35 or below..

  For a sell order, assume a stock is trading at$16.50. A LIT trigger could be placed at$16.60. In addition, a limit price of$16.65 could be set. If the price moves to$16.60 or above--the trigger price--then a limit order will be placed at$16.65. Since it is a limit order, the sell trade will only be executed at$16.65 or above.


- One Cancels the Other (OCO)

  One Cancels the Other (OCO) order is used in case if one simultaneously places a limit order and a stop-loss order. If either order is carried out the other is abrogated which lets the broker to make a deal without
  supervising the market. Once the market reaches up the level of the limit order, the currency is sold at a profit but when he market falls, the stop-loss order is used.

对于 StopOrder 和 StopLimitOrder，有人画了一张图更容易理解：

{% asset_img stoporder.jpg 停止单 %}

# 最终模型

{% plantuml %}

enum OrderState {
    UNKNOWN = 0
    NEW = 1
    PENDING = 1 << 1
    ACTIVE = 1 << 2
    PARTIALLY_FILLED = 1 << 3
    FILLED = 1 << 4
    REJECTED = 1 << 5
    CANCELLING = 1 << 8
    PENDING_CANCELLING = 1 << 9
    PARTIALLY_CANCELLED = 1 << 10
    CANCELLED = 1 << 11
    CANCEL_REJECTED = 1 << 12
}

enum TradeSide {
    BUY = 1
    SELL = 1 << 1
    SELLTODAY = 1 << 2
    SHORT = 1 << 5
    COVER = 1 << 6
    COVERTODAY = 1 << 7
}

enum OrderType {
    LMT = 0
    BOC = 1
    BOP = 1 << 1
    ITC = 1 << 2
    B5TC = 1 <<3
    FOK = 1 << 4
    B5TL = 1 << 5
}

class OrderBase {

}

class LimitOrder {

}

class MarketOrder {

}

class StopOrder {

}

{% endplantuml %}
