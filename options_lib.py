import numpy as np
from stochastic.processes.continuous import GeometricBrownianMotion


class MarketOption:

    def __init__(self,stock,strike,expiration,current_stock_price,risk_free_rate):
        self.stock = stock
        self.strike = strike
        self.expiration = expiration
        self.current_stock_price = current_stock_price
        self.risk_free_rate = risk_free_rate
        self.fair_price = None
        
        
        # Getters
    def stock(self):
        return self.stock
        
    def expiration(self):
        return self.expiration
        
    def strike(self):
        return self.strike
        
    def current_stock_price(self):
        return self.current_stock_price
        
    def risk_free_rat(self):
        return self.risk_free_rate
        
    def fair_price(self):
        return self.fair_price
        
        
        # Setters
    def stock(self,stock):
        self.stock=stock
        return self.stock
        
    def strike(self,strike):
        self.strike=strike
        return self.strike
        
    def expiration(self,expiration):
        self.expiration=expiration
        return self.expiration
        
    def current_stock_price(self,current_stock_price):
        self.current_stock_price=current_stock_price
        return self.current_stock_price
        
    def risk_free_rate(self,risk_free_rate):
        self.risk_free_rate=risk_free_rate
        return self.risk_free_rate


class EuropeanCall(MarketOption):


    def compute_fair_price(self,number_scenarios=10000,debug=0):
        # array of stock price scenarios at expiration time
        prices_at_expiration = np.array([self.stock.sample_at([self.expiration],self.current_stock_price) for i in range(number_scenarios)])
        if debug==1:
            print('Prices at expiration: {}'.format(prices_at_expiration))
        # values in exercising the option at expiration time
        exercise_value_at_expiration = prices_at_expiration-self.strike
        if debug==1:
            print('Exercise values at expiration: {}'.format(exercise_value_at_expiration))
        # values of the option in each scenario
        values_at_expiration = np.array(list(map(lambda x: max(0,x),exercise_value_at_expiration)), dtype="object")
        if debug==1:
            print('Values at expiration: {}'.format(values_at_expiration))
        # fair price of the option as the discounted average of the values of the option at maturity
        self.fair_price = values_at_expiration.mean()*np.exp(-self.risk_free_rate*self.expiration)
        if debug==1:
            print('Fair price: {}'.format(self.fair_price))
        return self.fair_price
        
        
class EuropeanPut(MarketOption):


    def compute_fair_price(self,number_scenarios=10000,debug=0):
        # array of stock price scenarios at expiration time
        prices_at_expiration = np.array([self.stock.sample_at([self.expiration],self.current_stock_price) for i in range(number_scenarios)])
        # values in exercising the option at expiration time
        exercise_value_at_expiration = self.strike-prices_at_expiration
        # values of the option in each scenario
        values_at_expiration = np.array(list(map(lambda x: max(0,x),exercise_value_at_expiration)))
        # fair price of the option as the discounted average of the values of the option at maturity
        self.fair_price = values_at_expiration.mean()*np.exp(-self.risk_free_rate*self.expiration)
        return self.fair_price
        
        
class AsianCallFixedStrike(MarketOption):


    def compute_fair_price(self,number_scenarios=10000,check_times=[],number_check_times=100):
        if check_times == []:
            # values in exercising the option at expiration time
            exercise_value_at_expiration = np.array([self.stock.sample(number_check_times,self.current_stock_price) for i in range(number_scenarios)]).mean(axis=1)-self.strike
        else:
            # values in exercising the option at expiration time
            exercise_value_at_expiration = np.array([self.stock.sample_at(check_times,self.current_stock_price) for i in range(number_scenarios)]).mean(axis=1)-self.strike
        # values of the option in each scenario
        values_at_expiration = np.array(list(map(lambda x: max(0,x),exercise_value_at_expiration)))
        # fair price of the option as the discounted average of the values of the option at maturity
        self.fair_price = values_at_expiration.mean()*np.exp(-self.risk_free_rate*self.expiration)
        return self.fair_price
        
        
class AsianPutFixedStrike(MarketOption):


    def compute_fair_price(self,number_scenarios=10000,check_times=[],number_check_times=100):
        if check_times == []:
            # values in exercising the option at expiration time
            exercise_value_at_expiration = self.strike-np.array([self.stock.sample(number_check_times,self.current_stock_price) for i in range(number_scenarios)]).mean(axis=1)
        else:
            # values in exercising the option at expiration time
            exercise_value_at_expiration = self.strike-np.array([self.stock.sample_at(check_times,self.current_stock_price) for i in range(number_scenarios)]).mean(axis=1)
        # values of the option in each scenario
        values_at_expiration = np.array(list(map(lambda x: max(0,x),exercise_value_at_expiration)))
        # fair price of the option as the discounted average of the values of the option at maturity
        self.fair_price = values_at_expiration.mean()*np.exp(-self.risk_free_rate*self.expiration)
        return self.fair_price
        

class AsianCallFixedPrice(MarketOption):

### For fixed price options the strike is the number which is used to multiply the stock mean price in the calculation of the value of the option
### at maturity

    def compute_fair_price(self,number_scenarios=10000,check_times=[],number_check_times=100):
        if check_times == []:
            # Values in exercising the option at expiration time
            scenarios = np.array([self.stock.sample(number_check_times,self.current_stock_price) for i in range(number_scenarios)])
            exercise_value_at_expiration = scenarios[:,-1]-scenarios.mean(axis=1)*self.strike
            # Scenarios can be pretty big, better delete it
            del scenarios
        else:
            # Values in exercising the option at expiration time
            scenarios = np.array([self.stock.sample_at(check_times,self.current_stock_price) for i in range(number_scenarios)])
            exercise_value_at_expiration = scenarios[:,-1]-scenarios.mean(axis=1)*self.strike
            # Scenarios can be pretty big, better delete it
            del scenarios
        # Values of the option in each scenario
        values_at_expiration = np.array(list(map(lambda x: max(0,x),exercise_value_at_expiration)))
        # Fair price of the option as the discounted average of the values of the option at maturity
        self.fair_price = values_at_expiration.mean()*np.exp(-self.risk_free_rate*self.expiration)
        return self.fair_price
        
class AsianPutFixedPrice(MarketOption):
### For fixed price options the strike is the number which is used to multiply the stock mean price in the calculation of the value of the option
### at maturity

    def compute_fair_price(self,number_scenarios=10000,check_times=[],number_check_times=100):
        if check_times == []:
            # Values in exercising the option at expiration time
            scenarios = np.array([self.stock.sample(number_check_times,self.current_stock_price) for i in range(number_scenarios)])
            exercise_value_at_expiration = scenarios.mean(axis=1)-scenarios[:,-1]*self.strike
            # Scenarios can be pretty big, better delete it
            del scenarios
        else:
            # Values in exercising the option at expiration time
            scenarios = np.array([self.stock.sample_at(check_times,self.current_stock_price) for i in range(number_scenarios)])
            exercise_value_at_expiration = scenarios[:,-1]-scenarios.mean(axis=1)
            # Scenarios can be pretty big, better delete it
            del scenarios
        # Values of the option in each scenario
        values_at_expiration = np.array(list(map(lambda x: max(0,x),exercise_value_at_expiration)))
        # Fair price of the option as the discounted average of the values of the option at maturity
        self.fair_price = values_at_expiration.mean()*np.exp(-self.risk_free_rate*self.expiration)
        return self.fair_price

##class CustomOption(MarketOption):
##### For custom options the strike price is the constant term in the option payoff: P = f(S,T) + k, where P is the payoff function,
##### S is the list of the stocks S0,S1,...,Sn and T is the list of check times t0,t1,t2,...,tm.
##### f is a string that represent a function with +-*/^ operations of S0(t0),S0(t1),...,S0(tm),S1(t0),...S1(tm),...Sn(t0),...,Sn(tm).
##### example of f: S0(t0)+S0(t1)*3-2*S1(t0)*S0(t3)^2/S2(t2)
##
##    def evaluate_function():
##
##
##    def compute_fair_price(self,number_scenarios=10000,check_times=[],function='',):
##
##
##
##
##    def compute_fair_price_with_functor(self,number_scenarios=10000,check_times=[],functor):
