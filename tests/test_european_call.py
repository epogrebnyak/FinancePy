import numpy as np

from financepy.finutils.FinGlobalTypes import FinOptionTypes
from financepy.products.equity.FinEquityVanillaOption import FinEquityVanillaOption
from financepy.market.curves.FinDiscountCurveFlat import FinDiscountCurveFlat
from financepy.models.FinModelBlackScholes import FinModelBlackScholes

from financepy.finutils.FinDate import FinDate
from financepy.finutils.FinError import FinError

valueDate = FinDate(2015, 1, 1)
expiryDate = FinDate(2015, 7, 1)
stockPrice = 100
volatility = 0.30
interestRate = 0.05
dividendYield = 0.01

european_call = FinEquityVanillaOption(
            expiryDate = expiryDate,
            strikePrice = 100.0,
            optionType = FinOptionTypes.EUROPEAN_CALL)

valuation_args = dict(
        valueDate=valueDate, 
        stockPrice=stockPrice, 
        discountCurve=FinDiscountCurveFlat(valueDate, interestRate),
        dividendCurve=FinDiscountCurveFlat(valueDate, dividendYield), 
        model=FinModelBlackScholes(volatility)
        )

def test_value_method():
    value = european_call.value(
        valueDate=valueDate, 
        stockPrice=stockPrice, 
        discountCurve=FinDiscountCurveFlat(valueDate, interestRate),
        dividendCurve=FinDiscountCurveFlat(valueDate, dividendYield), 
        model=FinModelBlackScholes(volatility)
    )
    assert round(value, 4) == 9.3021

def test_value_mc_method_with_sobol():
    value = european_call.valueMC(        valueDate=valueDate, 
        stockPrice=stockPrice, 
        discountCurve=FinDiscountCurveFlat(valueDate, interestRate),
        dividendCurve=FinDiscountCurveFlat(valueDate, dividendYield), 
        model=FinModelBlackScholes(volatility)
        , numPaths=1000
        , useSobol=True)
    assert round(value, 4) == 9.2431

def test_value_mc_method_no_sobol():
    value = european_call.valueMC(        valueDate=valueDate, 
        stockPrice=stockPrice, 
        discountCurve=FinDiscountCurveFlat(valueDate, interestRate),
        dividendCurve=FinDiscountCurveFlat(valueDate, dividendYield), 
        model=FinModelBlackScholes(volatility)
        , numPaths=1000
        , useSobol=False)
    assert round(value, 4) == 9.3136

def test_greeks():
    # can split to four tests and add values
    delta = european_call.delta(**valuation_args)
    vega = european_call.vega(**valuation_args)
    theta = european_call.theta(**valuation_args)
    rho = european_call.rho(**valuation_args)
    assert (delta, vega, theta, rho) # this just checks the 

# EP: Observations:

# 1.  Can take some import to base level - import financepy as fpy, then use something like fpy.FinDate
#     or from financepy import FinDate, this will require imports inside __init__.py

# 2. There are strong reasons to EuropeanCall and EuropeanPut classes 
#    - Even an existing docstring reads "this class is actually european calls and puts":
#        Class for managing plain vanilla European calls and puts on equities.
#        For American calls and puts see the FinEquityAmericanOption class. 
#    - Now for user to enact a european call she needs to import two and use three values:
#      FinEquityVanillaOption, FinOptionTypes and EUROPEAN_CALL, 
#      this is so much to keep in mind as compared EuropeanCall (or EquityVanillaEuropeanCall).
#    - With a flag and if's the branching goes back and forth, without it the code is more 
#      simplified, more straight, single resposibility.
#    - Flags can be used with there are many product types, in put vs call if's add up to the clutter.
#    - There is a logic where contract type is a class, and contract details used to create a class instance.

# 3.  Why value date has a signature of a tuple? (<class 'financepy.finutils.FinDate.FinDate'>, <class 'list'>),
#     is this needed for numba? If we tolerate the annotation is not meaningful (not ot be checked by mypy),
#     the original type is ok, and all of vectorisation is done outside. If we want to be strict and use mypy
#     as additional check then it should perhaps be Union[FinDate, List[FinDate]], or wait until mypy gives error
#     messages.  

# 4.  The analytic .value() and simulation .value_mc() functions are of type signature Contract -> Conditions -> Model -> Estimator -> Float,
#     We kind of separate Contract on one side and whole of (Conditions -> Model -> Estimator) on other side. 
#     This may have implications for further refactoring, if needed. This is not todo item.

# 5. Keeping number of optins outside class simplfies it, makes it signle resposibility (the user can multiply by 
#    number of contracts when she wants), avoids a default value.

# 6. dataclass allows for clean constructors and provide __repr__, __eq__ methods by default. 
