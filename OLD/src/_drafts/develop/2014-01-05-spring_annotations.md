---
layout: post
title: "Sping中的注解"
description: "使用注解的好处是减少配置。结合基于Java代码的容器配置，可以实现“零配置”。"
category: 软件开发
tags: [spring]
lastmod: 
---

[前面](/2013/12/31/jsr330.html)提到[Spring](http://spring.io/)支持
[JSR330](https://jcp.org/en/jsr/detail?id=330)中定义的[依赖注入的标准注解](/2013/12/31/jsr330.html#menuIndex3)。

Spring从2.5开始，还支持[JSR250](https://jcp.org/en/jsr/detail?id=250)(Common Annotations for the JavaTM Platform)注解，以及[JSR317](JavaTM Persistence 2.0)中的[JPA注解](/2012/12/30/JPA.html)。

不仅如此，Spring还扩展了自己的一些注解，能够进行更精细的声明。

使用注解的好处是减少配置。结合[基于Java代码的容器配置](/2014/01/01/spring_Java_based_container_configuration.html)，可以实现“零配置”。

本文介绍Spring中定义的一些注解。

# 标记bean

[JSR330](https://jcp.org/en/jsr/detail?id=330)中没有约定bean的注解，需要注入（`@Inject`）的地方，通过`[@Named](/2013/12/31/jsr330.html#menuIndex3)`限定器指定需要注入的接口类型。

在Spring中，定义了`@Component`、`@Repository`、`@Service`、`@Controller`等注解，用于标记bean：

- `@Component`： 是一个泛化的概念，仅仅表示一个组件 (Bean) ，可以作用在任何层次。
- `@Service`： 通常作用在业务层，但是目前该功能与 @Component 相同。
- `@Controller`： 通常作用在控制层，但是目前该功能与 @Component 相同。
- `@Repository`：通常用在数据访问层的DAO类上。Spring会将该注解标记的类中抛出的数据访问异常封装为 Spring 的数据访问异常类型。

可以在标记Bean时使用`@Lazy`注解标记该Bean可以延迟初始化。

此外，Spring还允许自定义bean的注解类型。比如，如果自定义一个@Cache的注解来表示缓存类:

```

//定义注解类型
package my.app.stereotype;
……
@Target({ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Component
public @interface Cache{
      String value() default "";
}


//使用自定义注解

@Cache("cache")
public class TestCache {

}

```

# bean作用域

[JSR330](https://jcp.org/en/jsr/detail?id=330)中只定义了`[@Singleton](/2013/12/31/jsr330.html#menuIndex3)`，标记singleton作用域；
spring提供“singleton”和“prototype”两种基本作用域，以及“request”、“session”、“global session”三种web作用域；
Spring还允许用户定制自己的作用域。作用域的作用是标记Bean对象相对于其他Bean对象的请求可见范围。

+ 基本作用域

  - singleton
  
    Bean在容器中只有一个实例，其整个生命周期交由容器管理。Spring使用注册表模式实现singleton模式，不需要在bean代码中用编程方式实现。
  
  - prototype
  
    每次请求bean时容器创建并返回该bean的一个新的实例。

+ Web作用域

  Web作用域只有在应用处于Web环境、并且在Web容器中配置对应的监听器或拦截器之后才会生效。包括：

  
  - request
    
    每个http请求创建一个新的Bean，比如Form表单数据对象。

  - session

    表示每个会话创建一个新的Bean。比如当前用户的用户信息对象。

  - globalSession

    用于portlet环境。如果在非portlet环境，等同于session作用域。

在Spring中，作用域用`@Scpoe`进行标记。比如：

```
@Scope("prototype") 
@Repository 
public class Demo { … }
```

# 自动装配

自动装配是指根据一定的策略，自动注入依赖对象，无需人工参与。使用自动装配可以减少构造器注入和setter注入配置。

Spring可以使用[JSR250规定的`@Resource`、`@Qualifier`注解]()处理自动装配，
也可以使用Spring自身的`@Autowired`和`@Qualifier`的组合。

`@Autowired`用于根据类型进行装配，可以用于Setter方法、构造函数、字段，甚至普通方法，前提是方法必须有至少一个参数。

`@Autowired`可以用于数组和使用泛型的集合类型。然后 Spring 会将容器中所有类型符合的 Bean 注入进来。

`@Autowired`标注作用于 Map 类型时，如果 Map 的 key 为 String 类型，则 Spring 会将容器中所有类型符合 Map 的 value 对应的类型的 Bean 增加进来，用 Bean 的 id 或 name 作为 Map 的 key。

`@Autowired`标注作用于普通方法时，会产生一个副作用，就是在容器初始化该 Bean 实例的时候就会调用该方法。当然，前提是执行了自动装配，对于不满足装配条件的情况，该方法也不会被执行。


当标注了`@Autowired`后，自动注入不能满足，则会抛出异常。可以给 @Autowired 标注增加一个 required=false 属性，以改变这个行为。
如果出现多个Bean候选者时，被注解为@Primary的Bean将作为首选者。

另外，每一个类中只能有一个构造函数的 @Autowired.required() 属性为 true。否则就出问题了。如果用 @Autowired 同时标注了多个构造函数，那么，Spring 将采用贪心算法匹配构造函数 ( 构造函数最长 )。

@Autowired 还有一个作用就是，如果将其标注在 BeanFactory 类型、ApplicationContext 类型、ResourceLoader 类型、ApplicationEventPublisher 类型、MessageSource 类型上，那么 Spring 会自动注入这些实现类的实例，不需要额外的操作。

JSR330中只定义了一个`@Named`注解，可以根据bean的ID进行限定；当容器中存在多个 Bean 的类型与需要注入的相同时，注入将不能执行。
Spring中定义了`@Qualifier`标注，可以提供更细致的限制粒度。比如：

```
@Autowired(required=false) 
@Qualifier("ppp") 
public void setPerson(person p){}
```

@Qualifier 甚至可以作用于方法的参数 ( 对于方法只有一个参数的情况，我们可以将 @Qualifer 标注放置在方法声明上面，但是推荐放置在参数前面 )，举例如下：

```
@Autowired(required=false) 
public void sayHello(@Qualifier("ppp")Person p,String name){}
```

如果 @Autowired 注入的是 BeanFactory、ApplicationContext、ResourceLoader 等系统类型，那么则不需要 @Qualifier，此时即使提供了 @Qualifier 注解，也将会被忽略；而对于自定义类型的自动装配，如果使用了 @Qualifier 注解并且没有名字与之匹配的 Bean，则自动装配匹配失败。



# 依赖检查

使用自动装配，很可能发生没有装配成功的情况。通常，在运行时(runtime)才会发现错误（比如空指针异常）。

为了能够提前发现装配错误，Spring提供了`@Required`注解用于依赖检查。

`@Required`注解应用在setter方法上，其机制 **不是** 判断字段值是否存在，
而是判断是否调用了setter方法。`@Required`也不检查setter方法的有效性。即使注入了"null"，也认为执行了注入。

如果标注了`@Required`的Setter方法没有被调用，则 Spring 在解析的时候会抛出异常。


`@DependsOn`注解则影响Bean初始化及销毁时的顺序。

# 使用表达式

通常，依赖关系是静态的。但是Spring还提供了`@Value`注解，能够按照SpEL表达式进行依赖注入。该注解可以用于字段、方法或参数。比如：

```
//用于字段
@Value(value = "#{message}")
private String message;

//用于标记了@Autowired的方法的参数上
@Autowired
public void initMessage(@Value(value = "#{message}#{message}") String message) {
    this.message = message;
}

//用于标记了@Autowired的构造器的参数上
@Autowired
private TestBean43(@Value(value = "#{message}#{message}") String message) {
    this.message = message;
}

```
 
# 注解与XML配置的结合

使用注解和[基于Java代码配置Spring容器](/2014/01/01/spring_Java_based_container_configuration.html)并不是为了完全取代XML，
将二者结合起来能收到更好的效果。详细资料参考[这里](http://www.ibm.com/developerworks/cn/opensource/os-cn-spring-iocannt/#major6)。