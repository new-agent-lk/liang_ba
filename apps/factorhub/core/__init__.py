"""
FactorHub Core Modules
Lazy imports to avoid startup errors with missing dependencies.
Use these functions to access the modules when needed.
"""


def get_data_provider():
    """Get AKShareDataProvider instance"""
    from apps.factorhub.core.data_provider import AKShareDataProvider
    return AKShareDataProvider()


def get_factor_library():
    """Get FactorLibrary instance"""
    from apps.factorhub.core.factor_lib import FactorLibrary
    return FactorLibrary()


def get_factor_calculator():
    """Get FactorCalculator instance"""
    from apps.factorhub.core.factor_calculator import FactorCalculator
    return FactorCalculator()


def get_factor_analyzer():
    """Get FactorAnalyzer instance"""
    from apps.factorhub.core.factor_analyzer import FactorAnalyzer
    return FactorAnalyzer()


def get_backtester(**kwargs):
    """Get Backtester instance"""
    from apps.factorhub.core.backtester import Backtester
    return Backtester(**kwargs)
