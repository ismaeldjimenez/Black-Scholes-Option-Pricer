import QuantLib as ql
import numpy as np
import seaborn as sns
import time

class BlackScholes:
    def __init__(self):
        pass
    
    def get_bs_price(self, option_type, calculation_date, expiration_date,
                              spot_price, strike_price, volatility,
                              risk_free_rate, dividend_rate=0,
                              binomial=True, steps=range(5,200)
    ):
        def get_binomial_price(option, bsm_process, steps):
            binomial_engine = ql.BinomialVanillaEngine(bsm_process, "crr", steps)
            option.setPricingEngine(binomial_engine)
            return option.NPV()
        
        #Get day Count and Calendar
        day_count = ql.Actual365Fixed()
        calendar = ql.UnitedStates(ql.UnitedStates.NYSE)

        # Get Option type
        option_type = ql.Option.Call if option_type.lower() == 'call' else ql.Option.Put

        maturity_date = ql.DateParser.parseISO(expiration_date)
        calculation_date = ql.DateParser.parseISO(calculation_date)

        payoff = ql.PlainVanillaPayoff(option_type, strike_price)

        spot_handle = ql.QuoteHandle(ql.SimpleQuote(spot_price))

        # term structure
        rf_rate_ts = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date,risk_free_rate,day_count))
        div_ts = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date,dividend_rate,day_count))
        vol_ts = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(calculation_date, calendar, volatility, day_count))

        bsm_process = ql.BlackScholesMertonProcess(spot_handle, div_ts, rf_rate_ts, vol_ts)

        eu_exercise = ql.EuropeanExercise(maturity_date)
        european_option = ql.VanillaOption(payoff, eu_exercise)

        european_option.setPricingEngine(ql.AnalyticEuropeanEngine(bsm_process))

        bs_price = european_option.NPV()

        if binomial:
            am_exercise = ql.AmericanExercise(calculation_date, maturity_date)
            american_option = ql.VanillaOption(payoff, am_exercise)
            am_prices = [get_binomial_price(american_option, bsm_process, step) for step in steps]

            eu_exercise = ql.EuropeanExercise(maturity_date)
            european_option = ql.VanillaOption(payoff, eu_exercise)
            eu_prices = [get_binomial_price(european_option, bsm_process, step) for step in steps]

            return bs_price, eu_prices, am_prices

        return bs_price

    def get_date(self):
        current_time = time.time()

        time_struct = time.localtime(current_time)

        year = time_struct.tm_year
        month = time_struct.tm_mon
        day = time_struct.tm_mday

        return f"{year}-{month}-{day}"


    def __str__(self):
        return f"call value = {str(self.C)}"
