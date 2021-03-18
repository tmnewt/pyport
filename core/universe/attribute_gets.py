from pandas import Timestamp

# TODO what exactly was the crucial intent of this code?...

def _get_universe_attributes(instructions:dict) -> list:
    universe_section = instructions['universe']

    return [
        universe_section['related_dataset'],
        Timestamp(universe_section['analysis_start_date']),
        Timestamp(universe_section['analysis_end_date']),
        universe_section['interval'],
        universe_section['dropna_how'],
        universe_section['assets'],
    ]

def _get_command_attributes(instructions:dict) -> dict:
    commands = instructions['commands']

    return [
        Timestamp(commands['strategy_start']),
        commands['lookback_length'],
        commands['lookback_time_quantifier'],
        commands['rebalance'],
        commands['rebalance_frequency'],
        commands['shorting'],
        commands['short_limit'],
        commands['long_floor'],
        commands['long_ceiling'],
    ]

def _get_portfolio_timeline_attributes(timeline:dict) -> list:
    
    return [
        Timestamp(timeline['start_date']),
        Timestamp(timeline['end_date']),
        Timestamp(timeline['lookback_start']),
        Timestamp(timeline['lookback_end']),
    ]
