---
layout: post
title: "Spring对集成测试的支持"
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

# Spring对集成测试的支持

Spring提供了TestContext框架简化集成测试，可以提供上下文管理、事务管理、依赖注入等功能，使得集成测试可以不依赖于J2EE容器或Web容器。
Spring的TestContext框架可以支持Junit、TestNG等测试框架。

- 上下文管理

  Spring测试上下文可以为每个测试用例(测试类)指定一个上下文，该上下文应用于测试类的每个测试方法。测试方法之间共用上下文即可以减少启动容器的开销，又可以保持上下文的一致性。

  举例如下： 

  ```
  @RunWith(SpringJUnit4ClassRunner.class)
  @ContextConfiguration(
      locations={"classpath:applicationContext-resources-test.xml",
                 "classpath:applicationContext-hibernate.xml"}
      inheritLocations=false)
  public class GoodsHibernateDaoIntegrationTest {
  }
  ```
  
  其中，`inheritLocations`属性指定是否继承父测试类的上下文配置。

- Test Fixture（测试固件）的依赖注入

  Test Fixture可以指运行测试时需要的任何东西，一般通过@Before定义的初始化Fixture方法准备这些资源，而通过@After定义的销毁Fixture方法销毁或还原这些资源。

  使用Spring进行单元测试，可以使用`@Autowired`注解，通过依赖注入的方式准备和销毁这些资源。比如：

  ```
  @Autowired
  private IGoodsDao goodsDao;
  @Autowired
  private ApplicationContext ctx;
  ```

- 事务管理

  事务管理一般需要容器的支持。Spring提供了容器的事务管理功能，从而可以独立于应用服务器完成事务相关功能的测试。比如：

  ```
  @RunWith(SpringJUnit4ClassRunner.class)
  @ContextConfiguration(
      locations={"classpath:applicationContext-resources-test.xml",
                 "classpath:applicationContext-hibernate.xml"})
  @TransactionConfiguration(
  transactionManager = "txManager", defaultRollback=true)
  public class GoodsHibernateDaoIntegrationTest {
  }
  ```

  Spring提供如下事务相关注解来支持事务管理：

    * @Transactional：使用@Transactional注解的类或方法将得到事务支持
    * transactionManager:指定事务管理器；
    * defaultRollback：是否回滚事务，默认为true表示回滚事务。
    * @BeforeTransaction和@AfterTransaction：使用这两个注解注解的方法定义了在一个事务性测试方法之前或之后执行的行为 ，且被注解的 方法将运行在该事务性方法的事务之外。
    * @Rollback(true)：默认为true，用于替换@TransactionConfiguration中定义的defaultRollback指定的回滚行为。

- 其他注解

  Spring还提供了一些注解，简化一些常用的测试代码的编写：

   * @DirtiesContext：表示每个测试方法执行完毕需关闭当前上下文并重建一个全新的上下文，即不缓存上下文。可应用到类或方法级别，但在JUnit 3.8中只能应用到方法级别。
   * @ExpectedException：表示被注解的方法预期将抛出一个异常，使用如@ExpectedException(NotCodeException.class)来指定异常，定义方式类似于Junit 4中的@Test(expected = NotCodeException.class)，@ExpectedException注解和@Test(expected =……)应该两者选一。
   * @Repeat：表示被注解的方法应被重复执行多少次，使用如@Repeat(2)方式指定。
   * @Timed：表示被注解的方法必须在多长时间内运行完毕，超时将抛出异常，使用如@Timed(millis=10)方式指定，单位为毫秒。注意此处指定的时间是如下方法执行时间之和：测试方法执行时间（或者任何测试方法重复执行时间之和）、@Before和@After注解的测试方法之前和之后执行的方法执行时间。而Junit 4中的@Test(timeout=2)指定的超时时间只是测试方法执行时间，不包括任何重复等。
   * 除了支持如上注解外，还支持【第十二章 零配置】中依赖注入等注解。

- 支持测试框架

  Spring的TestContext框架支持Junit、TestNG等测试框架。主要是实现了一些基类。通过继承或注解的方式使得编写的测试类能够支持这些测试框架。

    * AbstractJUnit38SpringContextTests：支持JUnit 3.8
    * AbstractTransactionalJUnit38SpringContextTests：支持JUnit 3.8，同时支持容器事务管理
    * AbstractJUnit4SpringContextTests：支持JUnit4+
    * AbstractTransactionalJUnit4SpringContextTests：支持JUnit4+，同时支持容器事务管理
    * AbstractTestNGSpringContextTests：支持TestNG

  对于Junit4+测试框架，还可以使用注解增强测试期的行为，方法是使用注解：

    * @RunWith(SpringJUnit4ClassRunner.class)：指定测试运行器，使用该注解的测试类无需继承bstractJUnit4SpringContextTests
    * @TestExecutionListeners：默认情况下，Spring测试框架将注册DependencyInjectionTestExecutionListener、DirtiesContextTestExecutionListener、TransactionalTestExecutionListener三个监听器。使用该注解可以手工指定：

      ```
      @RunWith(SpringJUnit4ClassRunner.class)
      @TestExecutionListeners({})
      public class GoodsHibernateDaoIntegrationTest {
      }
      ```
# Spring集成测试实例

## 依赖库

与Spring单元测试一样，Spring集成测试也需要一些依赖库。可以参考[单元测试的依赖库](/2014/01/05/unit_tests_within_spring.html#menuIndex3)。

## 集成测试环境

与[单元测试](/2014/01/05/unit_tests_within_spring.html)不同，
集成测试需要单独搭建一套独立的测试环境，从而保证开发、测试、生成环境相分离。

对于Spring应用来说，需要准备独立的资源配置文件，如`applicationContext-resources-test.xml`、`resources-test.properties`等。

## 持久层集成测试

[前面](/2014/01/05/unit_tests_within_spring.html#menuIndex4)说过，持久层的单元测试意义不大。

但是持久层的集成测试不仅测试该层定义的接口实现方法的行为是否正确，而且还要测试是否正确与数据库交互，是否发送并执行了正确的SQL，SQL执行成功后是否正确的组装了业务逻辑层需要的数据。

对持久层的集成测试不再通过Mock对象与数据库交互的API来完成测试，而是使用实实在在存在的与数据库交互的对象来完成测试。

下面是一个例子：

```


package cn.javass.point.dao.hibernate;
//省略import
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(
    locations={"classpath:applicationContext-resources-test.xml",
                      "classpath:applicationContext-hibernate.xml"})
@TransactionConfiguration(transactionManager = "txManager", defaultRollback=false)
public class GoodsHibernateDaoIntegrationTest {
    @Autowired
    private ApplicationContext ctx;
    @Autowired
    private IGoodsCodeDao goodsCodeDao;

//测试分页查询
@Transactional
@Rollback  //替换@ContextConfiguration指定的默认事务回滚行为，即将在测试方法执行完毕时回滚事务
@Test
public void testListAllPublishedSuccess() {
    GoodsModel goods = new GoodsModel();
    goods.setDeleted(false);
    goods.setDescription("");
    goods.setName("测试商品");
    goods.setPublished(true);
    goodsDao.save(goods);
    Assert.assertTrue(goodsDao.listAllPublished(1).size() == 1);
    Assert.assertTrue(goodsDao.listAllPublished(2).size() == 0);
}
} 

```

## 业务层集成测试

与[业务层单元测试](/2014/01/05/unit_tests_within_spring.html#menuIndex5)相比，
业务逻辑层集成测试的目的同样是测试该层的业务逻辑是否正确，
不同之处在于集成测试时使用真实的持久层对象(DAO)，而不是Mock对象。

例子如下：

```

@ContextConfiguration(
locations={"classpath:applicationContext-resources-test.xml",
            “classpath: applicationContext-hibernate.xml",
            “classpath:  applicationContext-service.xml"})
@TransactionConfiguration(transactionManager = "txManager", defaultRollback=false)
public class GoodsCodeServiceImplIntegrationTest extends AbstractJUnit4SpringContextTests {
    @Autowired
    private IGoodsCodeService goodsCodeService;
    @Autowired
    private IGoodsService goodsService;

	//测试购买失败的场景：
	@Transactional
	@Rollback
	@ExpectedException(NotCodeException.class)
	@Test
	public void testBuyFail() {
	    goodsCodeService.buy("test", 1);
	}
	
	// 测试购买成功的场景：
	@Transactional
	@Rollback
	@Test
	public void testBuySuccess() {
	    //1.添加商品
	    GoodsModel goods = new GoodsModel();
	    goods.setDeleted(false);
	    goods.setDescription("");
	    goods.setName("测试商品");
	    goods.setPublished(true);
	    goodsService.save(goods);      
	    //2.添加商品Code码
	    GoodsCodeModel goodsCode = new GoodsCodeModel();
	    goodsCode.setGoods(goods);
	    goodsCode.setCode("test");
	    goodsCodeService.save(goodsCode);
	    //3.测试购买商品Code码
	    GoodsCodeModel resultGoodsCode = goodsCodeService.buy("test", 1);
	    Assert.assertEquals(goodsCode.getId(), resultGoodsCode.getId());
	}
} 
```

## 展现层集成测试

与[展现层单元测试](/2014/01/05/unit_tests_within_spring.html#menuIndex6)相比，
展现层集成测试时使用真实的业务层对象（Service），而不是Mock对象。

以Struts Action的集成测试为例，需要引入struts的junit插件：

```
  <dependency>
    <groupId>org.apache.struts</groupId>
    <artifactId>struts2-junit-plugin</artifactId>
    <version>2.3.16</version>
  </dependency>
```

并准备配置文件`applicationContext-test.xml`:

```
  <import resource="classpath:applicationContext-resources-test.xml"/>
  <import resource="classpath:myapp/dao/applicationContext-hibernate.xml"/>
  <import resource="classpath:myapp/service/applicationContext-service.xml"/>
  <import resource="classpath:myapp/web/pointShop-admin-servlet.xml"/>
  <import resource="classpath:myapp/web/pointShop-front-servlet.xml"/>
```

所有的Action测试类要继承自Struts提供的StrutsSpringTestCase测试支持类，如下：

```
@RunWith(SpringJUnit4ClassRunner.class)
@TestExecutionListeners({})
public class GoodsActionIntegrationTest extends StrutsSpringTestCase {
    @Override
    protected String getContextLocations() {
        return "classpath:applicationContext-test.xml";
    }
    @Before
    public void setUp() throws Exception {
        //1 指定Struts2配置文件
        //该方式等价于通过web.xml中的<init-param>方式指定参数
        Map<String, String> dispatcherInitParams = new HashMap<String, String>();
        ReflectionTestUtils.setField(this, "dispatcherInitParams", dispatcherInitParams);
        //1.1 指定Struts配置文件位置
        dispatcherInitParams.put("config", "struts-default.xml,struts-plugin.xml,struts.xml");
        super.setUp();
    }
 	
 	@After
 	public void tearDown() throws Exception {
 	    super.tearDown();
 	}
 	
 	//测试购买失败的场景：
 	@Test
 	public void testBuyFail() throws UnsupportedEncodingException, ServletException {
 	    //2 前台购买商品失败
 	    //2.1 首先重置hhtp相关对象，并准备准备请求参数
 	    initServletMockObjects();
 	    request.setParameter("goodsId", String.valueOf(Integer.MIN_VALUE));
 	    //2.2 调用前台GoodsAction的buy方法完成购买相应商品的Code码
 	    executeAction("/goods/buy.action");
 	    GoodsAction frontGoodsAction = (GoodsAction) ActionContext.getContext().getActionInvocation().getAction();
 	    //2.3 验证前台GoodsAction的buy方法有错误
 	    Assert.assertTrue(frontGoodsAction.getActionErrors().size() > 0);
 	}
 	
 	
 	//测试购买成功的场景：
 	@Test
 	public void testBuySuccess() throws UnsupportedEncodingException, ServletException {
 	    //3 后台新增商品
 	    //3.1 准备请求参数
 	    request.setParameter("goods.name", "测试商品");
 	    request.setParameter("goods.description", "测试商品描述");
 	    request.setParameter("goods.originalPoint", "1");
 	    request.setParameter("goods.nowPoint", "2");
 	    request.setParameter("goods.published", "true");
 	    //3.2 调用后台GoodsAction的add方法完成新增
 	    executeAction("/admin/goods/add.action");
 	    //2.3 获取GoodsAction的goods属性
 	    GoodsModel goods = (GoodsModel) findValueAfterExecute("goods");
 	    //4 后台新增商品Code码
 	    //4.1 首先重置hhtp相关对象，并准备准备请求参数
 	    initServletMockObjects();
 	    request.setParameter("goodsId", String.valueOf(goods.getId()));
 	    request.setParameter("codes", "a\rb");
 	    //4.2 调用后台GoodsCodeAction的add方法完成新增商品Code码
 	    executeAction("/admin/goodsCode/add.action");
 	    //5 前台购买商品成功
 	    //5.1 首先重置hhtp相关对象，并准备准备请求参数
 	    initServletMockObjects();
 	    request.setParameter("goodsId", String.valueOf(goods.getId()));
 	    //5.2 调用前台GoodsAction的buy方法完成购买相应商品的Code码
 	    executeAction("/goods/buy.action");
 	    GoodsAction frontGoodsAction = (GoodsAction) ActionContext.getContext().getActionInvocation().getAction();
 	    //5.3 验证前台GoodsAction的buy方法没有错误
 	    Assert.assertTrue(frontGoodsAction.getActionErrors().size() == 0);
 	}
}
```
