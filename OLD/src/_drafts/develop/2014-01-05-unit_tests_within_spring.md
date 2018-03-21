---
layout: post
title: "Spring对单元测试的支持"
description: "功能测试的目的首先是为了保证软件功能的正确性，其次是为了保证软件的质量。Spring提供了专门的测试模块用于简化单元测试和集成测试。"
category: 软件开发
tags: [spring, 测试]
lastmod: 
---

功能测试的目的首先是为了保证软件功能的正确性，其次是为了保证软件的质量。测试相当重要，甚至有人提出了“测试驱动开发”。“测试驱动开发”通常会与“面向接口编程”相结合。

Spring提供了专门的测试模块用于简化单元测试和集成测试。

# 单元测试和集成测试

单元测试是最细粒度的测试，即具有原子性，通常测试的是某个功能（如测试类中的某个方法的功能）。在单元测试中，对于所依赖的对象，
会构建对应的Mock对象。一般来说，只有复杂的功能需要进行单元测试，而一些简单的功能（如数据访问层的CRUD）没有必要花费时间进行单元测试。

集成测试是在单元测试之上，通常是将一个或多个已进行过单元测试的组件组合起来完成的。集成测试中一般不会出现Mock对象，而是使用真实的接口实现。

# Spring对单元测试的支持

Spring IoC容器对对象没有入侵性，所以单元测试无需依赖Spring容器，只要简单的实例化对象、注入依赖的Mock对象，然后测试相应方法即可。

Spring对单元测试提供如下支持：

- Mock对象

  在`org.springframework.mock`包下面，提供了`env`、`jndi`、`web`、`web.portlet`等子包，可以用于简化Mock对象的创建。使得无需依赖特定的容器即可完成测试。

- 工具类

  在`org.springframework.test.util`包下面，有一些工具类可以简化测试代码的编写；`SimpleJdbcTestUtils`能读取一个sql脚本文件并执行来简化SQL的执行，还提供了如清空表、统计表中行数的简便方法来简化测试代码的编写。
  



# Spring单元测试实例

## 依赖库
用Spring进行测试，需要依赖spring-test、junit, jmock等库。Maven配置如下： 

```
  <dependency>
	<groupId>junit</groupId>
	<artifactId>junit</artifactId>
	<version>4.8.2</version>
	<scope>test</scope>
  </dependency>
  <dependency>
	<groupId>org.jmock</groupId>
	<artifactId>jmock-script</artifactId>
	<version>${jmock.version}</version>
	<scope>test</scope>
  </dependency>
  <dependency>
	<groupId>org.jmock</groupId>
	<artifactId>jmock-legacy</artifactId>
	<version>${jmock.version}</version>
	<scope>test</scope>
  </dependency>
  <dependency>
	<groupId>org.jmock</groupId>
	<artifactId>jmock-junit4</artifactId>
	<version>${jmock.version}</version>
	<scope>test</scope>
  </dependency>
  <dependency>
	<groupId>org.jmock</groupId>
	<artifactId>jmock</artifactId>
	<version>${jmock.version}</version>
	<scope>test</scope>
  </dependency>
  <dependency>
	<groupId>org.springframework</groupId>
	<artifactId>spring-test</artifactId>
	<version>${spring.version}</version>
	<scope>test</scope>
  </dependency>
```		

## 持久层单元测试

持久层的单元测试，是测试DAO对象的行为：

- 是否正确与数据库交互
- 是否发送并执行了正确的SQL
- SQL执行成功后是否正确的组装了业务逻辑层需要的数据

一般来说，DAO中简单的CRUD功能无需单元测试，只有相当复杂的方法才有必要写单元测试。

而且，由于通过Mock对象模拟对数据库的访问，没有真正与数据库交互，持久层的单元测试其实没有意义。
下面的例子只是为了演示，实际项目中通常通过继承测试来测试持久层。

例子：

```
public class GoodsHibernateDaoUnitTest {
    //1、Mock对象上下文，用于创建Mock对象
    // Mockery是JMock的核心类，其mock()方法可以创建接口或类的Mock对象
    private final Mockery context = new Mockery() { {
        //1.1、表示可以支持Mock非接口类，默认只支持Mock接口
        setImposteriser(ClassImposteriser.INSTANCE);
    }};
    //2、Mock HibernateTemplate类
    private final HibernateTemplate mockHibernateTemplate = context.mock(HibernateTemplate.class);
    private IGoodsDao goodsDao = null; 

    @Before
    public void setUp() {
        //3、创建IGoodsDao实现
        GoodsHibernateDao goodsDaoTemp = new GoodsHibernateDao();
        //4、通过ReflectionTestUtils注入需要的非public字段数据
        ReflectionTestUtils.setField(goodsDaoTemp, "entityClass", GoodsModel.class);
        //5、注入mockHibernateTemplate对象
        goodsDaoTemp.setHibernateTemplate(mockHibernateTemplate);
        //6、赋值给我们要使用的接口
        goodsDao = goodsDaoTemp;
	}

	@Test
	public void testSave () {
	    //7、创建需要的Model数据
	    final GoodsModel expected = new GoodsModel();
	    //8、定义预期行为，并在后边来验证预期行为是否正确
	    context.checking(new org.jmock.Expectations() {
	        {
	            //9、表示需要调用且只调用一次mockHibernateTemplate的get方法，
	            //且get方法参数为(GoodsModel.class, 1)，并将返回goods
	            one(mockHibernateTemplate).get(GoodsModel.class, 1);
	            will(returnValue(expected));
	        }
	    });
	    //10、调用goodsDao的get方法，在内部实现中将委托给
	    //getHibernateTemplate().get(this.entityClass, id);
	    //因此按照第8步定义的预期行为将返回goods
	    GoodsModel actual = goodsDao.get(1);
	    //11、来验证第8步定义的预期行为是否调用了
	  context.assertIsSatisfied();
	    //12、验证goodsDao.get(1)返回结果是否正确
	    Assert.assertEquals(goods, expected);
	}
}
```

## 业务层单元测试


业务层单元测试，目的是测试业务服务(Service)行为。通常使用Mock对象替代Service对象依赖的Dao对象，从而隔离与数据库交互，无需连接数据库即可测试业务逻辑是否正确。


测试业务逻辑时需要分别测试多种场景，即如在某种场景下成功或失败等等，即测试应该全面，每个功能点都应该测试到。

下面是一个例子：

```
public class GoodsCodeServiceImplUnitTest {
    //1、Mock对象上下文，用于创建Mock对象
    private final Mockery context = new Mockery() { {
        //1.1、表示可以支持Mock非接口类，默认只支持Mock接口
        setImposteriser(ClassImposteriser.INSTANCE);
    }};
  
    //2、Mock IGoodsCodeDao接口
    private IGoodsCodeDao goodsCodeDao = context.mock(IGoodsCodeDao.class);;
  
    private IGoodsCodeService goodsCodeService;

    @Before
    public void setUp() {
        GoodsCodeServiceImpl goodsCodeServiceTemp = new GoodsCodeServiceImpl();
        //3、依赖注入
        goodsCodeServiceTemp.setDao(goodsCodeDao);
        goodsCodeService = goodsCodeServiceTemp;
	}
	
	
	//测试购买失败的场景
	@Test(expected = NotCodeException.class)
	public void testBuyFail() {
	    final int goodsId = 1;
	    //4、定义预期行为，并在后边来验证预期行为是否正确
	    context.checking(new org.jmock.Expectations() {
	      {
	          //5、表示需要调用goodsCodeDao对象的getOneNotExchanged一次且仅以此
	          //且返回值为null
	          one(goodsCodeDao).getOneNotExchanged(goodsId);
	          will(returnValue(null));
	      }
	    });
	    goodsCodeService.buy("test", goodsId);
	    context.assertIsSatisfied();
	}
	
	//测试购买成功的场景
	@Test()
	public void testBuySuccess () {
	    final int goodsId = 1;
	    final GoodsCodeModel goodsCode = new GoodsCodeModel();
	    //6、定义预期行为，并在后边来验证预期行为是否正确
	    context.checking(new org.jmock.Expectations() {
	      {
	          //7、表示需要调用goodsCodeDao对象的getOneNotExchanged一次且仅以此
	          //且返回值为null
	          one(goodsCodeDao).getOneNotExchanged(goodsId);
	          will(returnValue(goodsCode));
	          //8、表示需要调用goodsCodeDao对象的save方法一次且仅一次
	          //且参数为goodsCode
	          one(goodsCodeDao).save(goodsCode);
	        }
	      });
	    goodsCodeService.buy("test", goodsId);
	    context.assertIsSatisfied();
	    Assert.assertEquals(goodsCode.isExchanged(), true);
	}
}
```
## 展现层单元测试

展现层单元测试可能包括对Action、Filter、JSP等的单元测试。对于Web展现层，会涉及到Servlet API、ActionContext等。
为避免对Web容器的依赖，可以使用stub（桩）实现或mock对象来模拟HttpServletRequest等对象。

类似于测试业务逻辑时需要分别测试多种场景，展现层单元测试同样需要分别测试多种场景。

下面是一个Action单元测试的例子：

```
public class GoodsActionUnitTest {
    //1、Mock对象上下文，用于创建Mock对象
    private final Mockery context = new Mockery() { {
        //1.1、表示可以支持Mock非接口类，默认只支持Mock接口
        setImposteriser(ClassImposteriser.INSTANCE);
    }};  
    //2、Mock IGoodsCodeService接口
    private IGoodsCodeService goodsCodeService = context.mock(IGoodsCodeService.class);

    private GoodsAction goodsAction;

    @Before
    public void setUp() {
        goodsAction = new GoodsAction();
        //3、依赖注入
        goodsAction.setGoodsCodeService(goodsCodeService);
	}
	
	//测试购买失败的场景
	@Test
	public void testBuyFail() {
	    final int goodsId = 1;
	    //4、定义预期行为，并在后边来验证预期行为是否正确
	    context.checking(new org.jmock.Expectations() {
	      {
	          //5、表示需要调用goodsCodeService对象的buy方法一次且仅一次
	          //且抛出NotCodeException异常
	          one(goodsCodeService).buy("test", goodsId);
	      will(throwException(new NotCodeException()));
	      }
	    });
	    //6、模拟Struts注入请求参数
	    goodsAction.setGoodsId(goodsId);
	    String actualResultCode = goodsAction.buy();
	    context.assertIsSatisfied();
	    Assert.assertEquals(ReflectionTestUtils.getField(goodsAction, "BUY_RESULT"), actualResultCode);
	    Assert.assertTrue(goodsAction.getActionErrors().size() > 0);
	}
	//测试购买成功的场景：
	
	@Test
	public void testBuySuccess() {
	    final int goodsId = 1;
	    final GoodsCodeModel goodsCode = new GoodsCodeModel();
	    //7、定义预期行为，并在后边来验证预期行为是否正确
	    context.checking(new org.jmock.Expectations() {
	      {
	          //8、表示需要调用goodsCodeService对象的buy方法一次且仅一次
	          //且返回goodsCode对象
	          one(goodsCodeService).buy("test", goodsId);
	          will(returnValue(goodsCode));
	      }
	    });
	    //9、模拟Struts注入请求参数
	    goodsAction.setGoodsId(goodsId);
	    String actualResultCode = goodsAction.buy();
	    context.assertIsSatisfied();
	    Assert.assertEquals(ReflectionTestUtils.getField(goodsAction, "BUY_RESULT"), actualResultCode);
	    Assert.assertTrue(goodsAction.getActionErrors().size() == 0);
	}
}
```


通过模拟ActionContext对象内容，从可以非常容易的测试Action中各种与http请求相关情况，无需依赖web服务器即可完成测试。

但如果需要测试http请求相关的对象，需要使用ActionContext获取值栈数据等情况，就需要Struts提供的junit插件支持了。

可以参考[Spring集成测试](/2014/01/05/integration_tests_within_spring.html)中的内容。

