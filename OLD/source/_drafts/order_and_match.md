Title: 委托和成交
Date: 2017-03-02
category: 量化交易
Tags: 交易规则,
---

 abc


# demo

::uml:: format="png" alt="Sample sequence diagram"
  participant User

  User -> A: DoWork
  activate A #FFBBBB

  A -> A: Internal call
  activate A #DarkSalmon

  A -> B: << createRequest >>
  activate B

  B --> A: RequestCreated
  deactivate B
  deactivate A
  A -> User: Done
  deactivate A
::end-uml::



