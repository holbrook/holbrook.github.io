---
layout: post
title: "CEP中的时间推理(Temporal)"
description: "时间推理(Temporal)是CEP中特有的条件判断(LHS)。本文介绍13种时间推理运算符及其DRL表示"
category: 软件开发
tags: [CEP]
lastmod:
---

[CEP](/2012/11/06/about_cep.html)中的[事件(Event)](/2013/12/21/event_in_CEP.html)具有两个与时间相关的属性。一个是timestamp，标记事件发生的时间；另一个是duration，标记事件持续的时间间隔。

由这两个时间属性，还可以计算出事件结束的事件。

时间推理(Temporal)是CEP中特有的条件判断([LHS](/2012/12/06/rule_language.html#menuIndex3))，其判断的要素正是基于事件的上述时间属性。

Allen在《An Interval-based Representation of Temporal Knowledge》中描述了13种时间推理的运算符。

下面用DRL语言介绍这13种运算符。其中，运算符的参数格式均为`[#d][#h][#m][#s][#[ms]]`。比如`3m30s`、`4m`等。


# After 和 Before(之前和之后)

  ![](images/rule-engine/temporal-after_and_before.png)

  ```
  // x∈[a,b]时，满足以下条件
  //A发生在B之前
  $eventA : EventA( this before[a,b] $eventB )
  //B发生在A之后
  $eventB : EventB( this after[a,b] $eventA )

  ```

  + 如果没有给出参数，则a=1ms, b=+∞
  + 如果只给出一个参数a,则b=+∞


# Coincides（同时发生）

  ![](images/rule-engine/temporal-coincides.png)

  ```
  // x∈[0,a]，且y∈[0,b]时，满足以下条件
  $eventA : EventA( this coincides[a,b] $eventB )
  $eventB : EventB( this coincides[a,b] $eventA )

  ```

  + 如果只给出一个参数a,则b=a
  + 如果不给出参数，则a=0,b=0


# During 和 Includes（包含）

  ![](images/rule-engine/temporal-during.png)

  ```
  // x∈[a,b]，且y∈[c,d]时，满足以下条件
  //A在B期间发生
  $eventA : EventA( this during[a,b,c,d] $eventB )
  //B包含A
  $eventB : EventB( this includes[a,b,c,d] $eventA )

  ```

  + 如果只给出二个参数a,b,则c=a,d=b
  + 如果只给出一个参数b,则a=0,c=0,d=b
  + 如果不给出参数，则a=0,b=+∞, c=0,d=+∞


# Finishes 和 Finished by（同时结束）


  ![](images/rule-engine/temporal-finishes.png)

  ```
  // x∈[0,a]时，满足以下条件
  //A在B之后开始，和B同时结束
  $eventA : EventA( this finishes[a] $eventB )
  //B在A之前开始，和B同时结束
  $eventB : EventB( this finishedby[a] $eventA )

  ```

  + 如果不给出参数，则a=0



# Meets 和 Met by（相邻）

  ![](images/rule-engine/temporal-after_and_before.png)

  ```
  // x∈[0,a]时，满足以下条件
  //A结束时B开始
  $eventA : EventA( this meets[a] $eventB )
  //A结束时B开始
  $eventB : EventB( this metby[a] $eventA )

  ```

  + 如果没有给出参数，则a=0


# Overlaps 和 Overlappd by（相交）

  ![](images/rule-engine/temporal-overlaps.png)

  ```
  // x∈[a,b]时，满足以下条件
  //A在B之前开始，在B之后结束
  $eventA : EventA( this overlaps[a,b] $eventB )
  //B在A之后开始，在A之前结束
  $eventB : EventB( this overlappedby[a,b] $eventA )

  ```

  + 如果只给出一个参数b,则a=0
  + 如果不给出参数，则a=0,b=0



# Starts 和 Started by（同时开始）


  ![](images/rule-engine/temporal-starts.png)

  ```
  // x∈[0,a]时，满足以下条件
  //A和B同时开始，A先结束
  $eventA : EventA( this starts[a] $eventB )
  //B和A同时开始，B后结束
  $eventB : EventB( this startedby[a] $eventA )

  ```

  + 如果不给出参数，则a=+∞


