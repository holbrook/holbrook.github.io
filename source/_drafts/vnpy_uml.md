---
title: vnpy解析
postslug: the_order
category: 量化交易
tags: vnpy
date: 2019-08-12
---

vnpy

<!--more-->

# domain model

The domain model shows how vnpy understand the conception of trading ragion.

The entities in domain model are defined in `vnpy/trader/object.py` , and enumurations in `vnpy/trader/constant.py`.

{% plantuml %}

package vnpy.trader {
  package object {    
    class BaseData <<@dataclass>>{
      + gateway_name: str
    }

    class TickData {

    }

    class BarData {

    }

    BaseData <|-- TickData
    BaseData <|-- BarData
    BaseData <|-- OrderData
    BaseData <|-- TradeData
    BaseData <|-- PositionData
    BaseData <|-- AccountData
    BaseData <|-- LogData
    BaseData <|-- ContractData


    class SubscribeRequest <<@dataclass>> {
    }

    class OrderRequest <<@dataclass>> {
    }

    class CancelRequest <<@dataclass>> {
    }
    
    class HistoryRequest <<@dataclass>> {
    }
    


  }

  package constant {

  }
}


{% endplantuml %}

# event engines

Anything who can deal with event is nominated "Engine".

Via these engines, vnpy assemble various components together. 


{% plantuml %}

package vnpy.trader {
  package event {
    class EventEngine {

    }
  }

  package engine {
    BaseEngine o-- MainEngine
    BaseEngine o-- EventEngine

    class BaseEngine {
        + engine_name
    }

    BaseEngine <|-- LogEngine
    BaseEngine <|-- OmsEngine
    BaseEngine <|-- EmailEngine
  }  

  package gateway {
    class BaseGateway {
        {abstract} void connect(setting: dict)
        {abstract} void close()
        {abstract} void subscribe(req: SubscribeRequest)
        {abstract} str send_order(req: OrderRequest)
        {abstract} void cancel_order(req: CancelRequest)
        {abstract} void query_account()
        {abstract} void query_position()
    }

    BaseGateway o-- EventEngine
  }
}

package vnpy.app.algo_trading {
    
  package " engine" {
    class AlgoEngine {
    }

    BaseEngine <|-- AlgoEngine
  }    
}


package vnpy.app.ctaext_strategy {
    
  package "  engine" {
    class CtaEngine {
    }

    BaseEngine <|-- CtaEngine
  }    
}


package vnpy.app.risk_manager {
    
  package "engine " {
    class RiskManagerEngine {
    }

    BaseEngine <|-- RiskManagerEngine
  }    
}


{% endplantuml %}