# -*- coding: utf-8 -*-

from __future__ import division

from vnpy.trader.vtObject import VtBarData
from vnpy.trader.vtConstant import  EMPTY_STRING,EMPTY_INT,EMPTY_FLOAT
from vnpy.trader.app.ctaStrategy.ctaTemplate import (CtaTemplate, 
                                                     BarManager, 
                                                     ArrayManager)
                                                     
########################################################################
                                                     
class turtleStrategy(CtaTemplate):
    
    className = 'turtleStrategy'
    
    #策略参数
    shortInDate = 20
    longInDate = 55
    shortOutDate = 10
    longOutDate = 20
    loss = 0.1
    adjust = 0.8
    numberDays =20
    unitLimit = 4
    ratio = 0.8
    
    #策略变量
    unit = 10
    N = []
    days = 0
    breakPrice1 = 0
    breakPrice2 = 0
    sys1 = 0
    sys2 = 0
    system1 = True
    
    # 参数列表，保存了参数的名称
    paramList = ['name',
                 'className',
                 'author',
                 'vtSymbol',
                 'shortInDate',
                 'longInDate',
                 'shortOutDate',
                 'longOutDate',
                 'loss',
                 'adjust',
                 'numberDays',
                 'unitLimit',
                 'ratio']    
    
    # 变量列表，保存了变量的名称
    varList = ['inited',
               'trading',
               'pos',
               'unit',
               'N',
               'days',
               'breakPrice1',
               'breakPrice2',
               'sys1',
               'sys2',
               'system1']  

    #----------------------------------------------------------------------
    def __init__(self, ctaEngine, setting):
        """Constructor"""
        super(turtleStrategy, self).__init__(ctaEngine, setting)
        
        self.bm = BarManager(self.onBar)
        self.am = ArrayManager()
        
        # 注意策略类中的可变对象属性（通常是list和dict等），在策略初始化时需要重新创建，
        # 否则会出现多个策略实例之间数据共享的情况，有可能导致潜在的策略逻辑错误风险，
        # 策略类中的这些可变对象属性可以选择不写，全都放在__init__下面，写主要是为了阅读
        # 策略时方便（更多是个编程习惯的选择）
        
    #----------------------------------------------------------------------
    def onInit(self):
        """初始化策略（必须由用户继承实现）"""
        self.writeCtaLog(u'双EMA演示策略初始化')
        
        initData = self.loadBar(self.initDays)
        for bar in initData:
            self.onBar(bar)
        
        self.putEvent()
        
    #----------------------------------------------------------------------
    def onStart(self):
        """启动策略（必须由用户继承实现）"""
        self.writeCtaLog(u'双EMA演示策略启动')
        self.putEvent()
    
    #----------------------------------------------------------------------
    def onStop(self):
        """停止策略（必须由用户继承实现）"""
        self.writeCtaLog(u'双EMA演示策略停止')
        self.putEvent()
        
    #----------------------------------------------------------------------
    def onTick(self, tick):
        """收到行情TICK推送（必须由用户继承实现）"""
        self.bm.updateTick(tick)
        
    #----------------------------------------------------------------------
    def onBar(self, bar):
        """收到Bar推送（必须由用户继承实现）"""
        def handleData(context,data):
            dt = context.current_dt
            current_price = data[security].price
            if dt.hour == 9 and dt.minute == 30:
                days += 1
                calculate_N()
            if days > numberdays:
                value = context.portfolio.portfolio_value
                cash = context.portfolio.cash
                
                if sys1 == 0 and sys2 == 0:
                    if value < (1-loss)*context*portfolio.starting_cash:
                        cash *= adjust
                        value = adjust
                        
                    dollarvolatility = dollarPerShare*N[-1]
                    unit = value*0.01/dollarvolatility
                    
                    system1 = True
                    if sys1 == 0:
                        marketIn(current_price,ratio*cash,shortInDate)
                    else:
                        stopLoss(current_price)
                        marKetAdd(current_price,ratio*cash,shortInDate)
                        marketOut(current_price,shortOutDdate)
                        
                    system1 = False
                    if sys == 0:
                        marketIn(current_price,ratio*cash,longInDate)
                    else:
                        stopLoss(current_price)
                        marKetAdd(current_price,ratio*cash,longInDate)
                        marketOut(current_price,longOutDdate)
                        
        def calculate_N():
            if days <= numberDays:
                price = attribute_history(g.security, g.days, '1d',('high','low','close'))
                lst = []
                for i in range(0,days):
                    hl = price['high'][i] - price['low'][i]
                    hc = price['high'][i] - price['close'][i]
                    cl = price['close'][i] - price['low'][i]
                    
                    trueRange = max(hl,hc,cl)
                    lst.append(trueRange)
                currentN = np.mean(np.array(lst))
                N.append(currentN)
                
            else:
                price = attribute_history(g.security, 1, '1d',('high','low','close'))
            
                h_l = price['high'][0]-price['low'][0]
                h_c = price['high'][0]-price['close'][0]
                c_l = price['close'][0]-price['low'][0]
                
                trueRange = max(hl,hc,cl)
                current_N = (True_Range + (g.number_days-1)*(g.N)[-1])/g.number_days
                (g.N).append(current_N)
                
        def marketIn(current_price,cash,in_date):
            price = attribute_history(g.security, in_date, '1d', ('close'))
            
            if current_price > max(price['close']):
                num_of_shares = cash/current_price
                if num_of_shares >= g.unit:
                    print "买入"
                    print current_price
                    print max(price['close'])
                    if g.system1 == True:
                        if g.sys1 < int(g.unit_limit*g.unit):
                            order(g.security, int(g.unit))
                            g.sys1 += int(g.unit)
                            g.break_price1 = current_price
                    else:
                        if g.sys2 < int(g.unit_limit*g.unit):
                            order(g.security, int(g.unit))
                            g.sys2 += int(g.unit)
                            g.break_price2 = current_price
                            
        def market_add(current_price, cash, in_date):
            if g.system1 == True:
                break_price=g.break_price1
            else:
                break_price=g.break_price2
            # 每上涨0.5N，加仓一个单元
            if current_price >= break_price + 0.5*(g.N)[-1]: 
                num_of_shares = cash/current_price
                # 加仓
                if num_of_shares >= g.unit: 
                    print "加仓"
                    print g.sys1
                    print g.sys2
                    print current_price
                    print break_price + 0.5*(g.N)[-1]
               
                    if g.system1 == True:
                        if g.sys1 < int(g.unit_limit*g.unit):
                            order(g.security, int(g.unit))
                            g.sys1 += int(g.unit)
                            g.break_price1 = current_price
                    else:
                        if g.sys2 < int(g.unit_limit*g.unit):
                            order(g.security, int(g.unit))
                            g.sys2 += int(g.unit)
                            g.break_price2 = current_price
    
    
    #8
    # 离场函数
    # 输入：当前价格-float, 天数-int
    # 输出：none
        def market_out(current_price, out_date):
            # Function for leaving the market
            price = attribute_history(g.security, out_date, '1d', ('close'))
            # 若当前价格低于前out_date天的收盘价的最小值, 则卖掉所有持仓
            if current_price < min(price['close']):
                print "离场"
                print current_price
                print min(price['close'])
                if g.system1 == True:
                    if g.sys1>0:
                        order(g.security, -g.sys1)
                        g.sys1 = 0
                else:
                    if g.sys2>0:
                        order(g.security, -g.sys2)
                        g.sys2 = 0
        
        
        #9
        # 止损函数
        # 输入：当前价格-float
        # 输出：none
        def stop_loss(current_price):
            # 损失大于2N，卖出股票
            if g.system1 == True:
                break_price = g.break_price1
            else:
                break_price = g.break_price2
            # If the price has decreased by 2N, then clear all position
            if current_price < (break_price - 2*(g.N)[-1]):
                print "止损"
                print current_price
                print break_price - 2*(g.N)[-1]
                if g.system1 == True:
                    order(g.security, -g.sys1)
                    g.sys1 = 0  
                else:
                    order(g.security, -g.sys2)
                    g.sys2 = 0

                        
                
                
                
                
                    
                
                        
                        
    
    
    
                                                     
                                     
