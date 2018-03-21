---
layout: post
title: "Drools规则描述语言快速手册"
description: ""
category: 软件开发
tags: [规则引擎]
lastmod: 
---

[在规则引擎中，通常会使用某种表述性的语言（而不是编程语言）来描述规则](/2012/03/20/rule_engine_1.html)。
所以规则描述语言也是规则引擎的一个重要组成部分。

目前在规则描述语言方面，并没有一个通用的标准获得规则引擎厂商的广泛支持，大部分规则描述语言都是厂商私有的。

大体来说，规则语言可以分为结构化的（Structured)和基于标记的（Markup，通常为xml）。

常见的规则描述语言包括：


- srl(Structured Rule Language)	: Fair Isaac（以前是Blaze Software）定义的结构化规则描述语言
- drl(Drools Rule Language)	: Jboss（以前是drools.org)定义的结构化规则描述语言
- RuleML(Rule Markup Language）: www.ruleml.org定义的xml规则描述语言
- SRML(Simple Rule Markup Language): xml规则描述语言
- BRML(Business Rules Markup Language):xml规则描述语言
- SWRL（A Semantic Web Rule Language):www.daml.org定义的xml规则描述语言

不管是哪种规则描述语言，都需要描述一组条件以及在此条件下执行的操作（即规则）。

# 概览

下面是一个drl的例子：

```
package com.sample
 
import com.sample.DroolsTest.Message;
 
rule "Hello World"
    when
        m : Message( status == Message.HELLO, myMessage : message )
    then
        System.out.println( myMessage );
        m.setMessage( "Goodbye cruel world" );
        m.setStatus( Message.GOODBYE );
        update( m );
end

rule "GoodBye"
    when
        Message( status == Message.GOODBYE, myMessage : message )
    then
        System.out.println( myMessage );
end
```

完整的drl文件会包含以下几个部分：

- package 声明
- imports
- declares
- globals
- functions
- queries
- rules


# package和import声明

与Java语言类似，drl的头部需要有package和import的声明。

规则文件当中必须要有一个 **package** 声明,同时 package 声明必须要放在规则文件的第一行。

# 规则定义

drl中，一个规则的标准结构如下：

```
rule "name" 
    attributes
    when 
        LHS
    then 
        RHS
end
```

一个规则通常包括三个部分:属性部分(attribute)、条件 部分(LHS)和结果部分(RHS)。

## 条件部分(LHS)

在 LHS 当中,可以包含多个条件,如果 LHS 部分没空的话,那么引擎会自动添加一 个 eval(true)的条件。

多个条件之间之间用可以使用 **and** 或 **or** 来进行连接。默认是 **and** 关系。

每个条件的语法为：

[绑定变量名:]Object([field 约束])

“绑定变量名”是可选的。绑定的变量可以在该LHS后续的条件中引用。

“field 约束”是指当前对象里相关字段的条件限制, 多个约束之间可以用“&&”(and)、“||”(or)和“,”(and)来连接。



举例如下：

```
when
    $customer:Customer()
then
    ……


when
    $customer:Customer(age>20,gender==􏰃male􏰃)
    Order(customer==$customer,price>1000)
then
    ……


when
    Customer(age>20 || (gender=='male' && city==‘sh'))
then
    ……
```

约束中可以使用的比较操作符包括：

```
>、>=、<、<=、= =、!=、contains、not contains、 memberof、not memberof、matches、not matches
```

举例如下：

```
when
    $order:Order();
    $customer:Customer(age >20, orders contains $order); 
then
    ……


when
    $order:Order(name memberOf orderNames); # orderNames为数组或集合类型
then
    ……

when
    $customer:Customer(name matches "李.*"); # 正则表达式匹配
then
    ……

```

## 结果部分(RHS)

RHS 部分定义了当LHS满足是要进行的操作。

RHS中可以编写代码，可以使用 LHS 部分当中定义的绑定变量名以及drl头部定义的全局变量。

在 RHS 当中虽然可以直接编写 Java 代码,但不建议在代码当中有条件判断,如果需要条件判断,那么请重新考虑将其放在 LHS 当中,否则就违背了使用规则的初衷。

### 使用宏函数

RHS中可以使用宏函数对工作空间(Working Memory)进行操作。当调用宏函数后，所有未设置“no-loop”属性的规则都会被重新匹配，符合条件的重新触发。

宏函数包括：

- insert：将一个 Fact 对象插入到当前的 Working Memory
- update：对当前 Working Memory 中的 Fact 进行更新
- retract ：从 Working Memory 中删除某个 Fact 对象

这些宏函数都是StatefulSession中定义的方法。


举例如下：

```
when
    ……
then
    Customer cus=new Customer(); 
    cus.setName("张三"); 
    insert(cus);


when
    $customer:Customer(name=="张三",age<10); 
then
    $customer.setAge($customer.getAge()+1); 
    update($customer);


when
    $customer:Customer(name=="张三",age<10); 
then
    Customer customer=new Customer(); 
    customer.setName("张三"); 
    customer.setAge($customer.getAge()+1);

    # 用新对象替换Working Memory中的旧对象
    update(drools.getWorkingMemory().getFactHandleByIdentity($customer),customer);  


when
    $customer:Customer(name=="张三"); 
then
    retract($customer);

```

### modify代码块

modify代码块用于快速修改并更新(update)某个 Fact 对象的多个属性。语法及例子如下：

```
modify(fact-expression){
    <修改 Fact 属性的表达式>[,<修改 Fact 属性的表达式>*]
}


when
    $customer:Customer(name=="张三",age==20); 
then
    modify($customer){ 
        setId("super man"), 
        setAge(30)
    }


```


### drools宏对象

通过使用 drools 宏对象可以实现在规则文件里直接访问 Working Memory, 从而获取对当前的 Working Memory 的更多控制。

drools 宏对象的常用方法包括：

- drools.getWorkingMemory()：获取当前的 WorkingMemory 对象
- drools.halt()：在当前规则执行完成后,不再执行 其它未执行的规则。
- drools.getRule()：得到当前的规则对象
- drools.insert(new Object)：向当前的 WorkingMemory 当中插入 指定的对象,功能与宏函数 insert 相同。
- drools.update(new Object)：更新当前的 WorkingMemory 中指定 的对象,功能与宏函数 update 相同。
- drools.update(FactHandle Object)：更新当前的 WorkingMemory 中指定 的对象,功能与宏函数 update 相同。
- drools.retract(new Object)：从当前的 WorkingMemory 中删除指 定的对象,功能与宏函数 retract 相 同。

例如：

```
when 
    eval(true);
then
    Customer cus=new Customer(); 
    cus.setName("张三"); 
    drools.insert(cus)
```

### kcontext宏对象

kcontext 也是 Drools 提供的一个宏对象,它的作用主要是用来得到当前的 KnowledgeRuntime 对象,KnowledgeRuntime 对象可以实现与引擎的各种交互。



## 规则属性

主要的规则属性如下：

13 个:  auto-focus、、lock-on-active、no-loop、 ruleflow-group、、when。

- salience

  设置规则执行的优先级,数字越大越先执行，数字相同的使用随机顺序。默认值为0，可以设置为负数。

- no-loop

  默认为false。设置为true时，表示该规则只会被引擎检查一次。引擎内部对Fact更新时，忽略本规则的再次检查。

- date-effective

  设置规则的开始生效日期。默认接受“dd-MMM-yyyy”格式的字符串。可以用代码修改日期格式，如：

  `System.setProperty("drools.dateformat","yyyy-MM-dd")`。

- date-expires

  设置规则的过期日期。格式与`date-effective`相同。

- enabled

  默认为true。设置规则是否可用。

- dialect

  设置规则中使用的编程语言。默认为java，还可以设置为mvel。通过drools.getRule().getDialect()可以获取该属性的设置。

- duration

  延迟指定的时间后，在 **另一个线程中** 触发规则。单位为毫秒。

- activation-group

  为规则划指定一个活动组（组名为字符串）。同一个活动组中的规则只执行一个，根据优先级(salience)来决定执行哪一个规则。

- agenda-group 和 auto-focus

  为规则指定一个议程(agenda)组。指定了议程组的规则只有在该议程组得到焦点时才被触发。但如果规则同时指定了auto-focus属性为true，则该规则自动得到焦点。

  指定议程组焦点可以通过回话(session)：

  ```
  session.getAgenda().getAgendaGroup("GROUP_NAME").setFocus();
  session.fireAllRules();
  ```

  也可以实现org.drools.runtime.rule.AgendaFilter 接口：

  {% highlight java %}
    package test;
    import org.drools.runtime.rule.Activation;
    import org.drools.runtime.rule.AgendaFilter;

    public class TestAgendaFilter implements AgendaFilter { 
        private String startName;
        public TestAgendaFilter(String startName){
            this.startName=startName; 
        }
        public boolean accept(Activation activation) { 
            String ruleName=activation.getRule().getName(); 
            if(ruleName.startsWith(this.startName)){
                return true; 
            }else{
                return false; 
            }
        } 
    }  
  {% endhighlight %}

- ruleflow-group

  指定规则流组。

- lock-on-active

  当在规则上使用 ruleflow-group 属性或 agenda-group 属性的时候,将 lock-on-action 属性 的值设置为 true,可能避免因某些 Fact 对象被修改而使已经执行过的规则再次被激活执行。lock-on-active 是 no-loop 的增强版属性，在规则流中很有用。

举例如下：

```
rule "rule1"
    salience 1 
    when
    ……

```

# 注释

Drools 当中注释的写法与编写 Java 类的注 释的写法完全相同,注释的写法分两种:单行注释与多行注释。

单行注释可以采用“#”或者“//”来进行标记， 多行注释以“/*”开始,以“*/”结束。

例如：

```
/* 规则rule1的注释
这是一个测试用规则
*/
rule "rule1" 
    when
        eval(true) #没有条件判断 
    then
        System.out.println("rule1 execute"); //仅仅是输出
end
```


# 类型声明

可以在规则文件中定义Fact类型，而不需要编写Java类。比如：

```
declare Address 
    city : String
    addressName : String
end

declare Person 
    name:String
    birthday:Date
    address:Address //使用declare声明的对象作为address属性类型 
    order:Order //使用名为Order的JavaBean作为order属性类型
end
```

在KnowledgeBase中可以获取规则文件中定义的Fact类型，比如：

```
//获取规则文件当中定义的Address对象并对其进行实例化
FactType addressType=knowledgeBase.getFactType("test","Address");
Object add=addressType.newInstance(); 
addressType.set(add, "city","Beijing"); 
addressType.set(add, "addressName","Capital");
```

在声明中还可以定义元数据。可以为 Fact 对象、Fact对象的属性或者是规则来定义元数据,元数据定义采用的是“@”符号开头。

比如：

```
declare User
    @createTime(2009-10-25) 
    username : String @maxLenth(30) 
    userid : String @key
    birthday : java.util.Date
end
```

元数据的获取？(TODO)

# 全局变量（TODO）

# 函数和import function

## 函数的定义和使用

函数是定义在规则文件当中一代码块,作用是将在规则文件当中若干个规则都会用到的业务操作封装起来,实现业务代码的复用,减少规则编写的工作量。
函数的可见范围是函数所在的规则文件。

函数以function定义，可以是void，也可以有返回值。例如：

```
package test
import java.util.List; 
import java.util.ArrayList;
/*
一个测试函数
用来向Customer对象当中添加指定数量的Order对象的函数
*/

function void setOrder(Customer customer,int orderSize) {
    List ls=new ArrayList(); 
    for(int i=0;i< orderSize;i++){
        Order order=new Order();
        ls.add(order);
    }
    customer.setOrders(ls);
}

/*
测试规则
*/
rule "rule1" when
    $customer :Customer();
then
    setOrder($customer,5);
    System.out.println("rule 1 customer has order size:"+$customer.getOrders().size());
end

/*
测试规则
*/
rule "rule2" when
    $customer :Customer();
then
    setOrder($customer,10);
    System.out.println("rule 2 customer has order size:"+$customer.getOrders().size());
end
```

## 引入静态方法

实际应用当中,可以考虑使用在 Java 类当中定义静态方法的办法来替代在规则文件当 中定义函数。

Drools 提供了一个特殊的 import 语句:import function,通过该 import 语句,可以实现将一个 Java 类中静态方法引入到一个规则文件当中,使得该文件当中的规 则可以像使用普通的 Drools 函数一样来使用 Java 类中某个静态方法。


比如：

{% highlight java %}
package test;
public class RuleTools {
    public static void printInfo(String name){
        System.out.println("your name is :"+name); 
    }
}
{% endhighlight %}

```
package test
import function test.RuleTools.printInfo;
/*
测试规则
*/
rule "rule1" 
    when
        eval(true); 
    then
        printInfo("test import function");
end

```

# 查询定义

查询用于根据条件在当前的 WorkingMemory 当中查找 Fact。Drools 当中查询可分为两种:一种是不需要外部传入参数;一种是需要外部传入参 数。


如：

```
query "testQuery" 
    customer:Customer(age>30,orders.size >10)
end

query "testQuery2"(int $age,String $gender) 
    customer:Customer(age>$age,gender==$gender)
end
```

通过session可以在外部调用规则文件中的查询，比如：

{% highlight java %}
……
QueryResults queryResults=statefulSession.getQueryResults("testQuery");
for(QueryResultsRow qr:queryResults){
    Customer cus=(Customer)qr.get("customer"); //打印查询结果
    System.out.println("customer name :"+cus.getName());
}

QueryResults queryResults2=statefulSession.getQueryResults("testQuery2", new Object[]{new Integer(20),"F"});

……
{% endhighlight %}