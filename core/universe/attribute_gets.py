def _get_universe_attributes(instructions:dict) -> list:
    universe_section = instructions['universe']

    return [
        universe_section['related_dataset'],
        universe_section['analysis_start_date'],
        universe_section['analysis_end_date'],
        universe_section['interval'],
        universe_section['dropna_how'],
        universe_section['assets'],
    ]

def _get_command_attributes(instructions:dict) -> dict:
    commands = instructions['commands']

    return [
        commands['strategy_start'],
        commands['lookback_length'],
        commands['lookback_time_quantifier'],
        commands['rebalance'],
        commands['rebalance_frequency'],
        commands['shorting'],
        commands['short_limit'],
        commands['long_floor'],
        commands['long_ceiling'],
        commands['bounds'],
        commands['constraints'],
    ]



def _get_description(instructions:dict) -> str:
    return instructions['description']

