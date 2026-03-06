# the dataset does not have proper xG, so approximate using goals and attack/Defense strength will be used

import pandas as pd

def create_expected_goals_targets(match_data):

    #simple proxy targets
    match_data['home_xG'] = (
        0.6 * match_data['home_attack']  + 0.4 * match_data['away_defense']
    )

    match_data['away_xG'] = (
        0.6 * match_data['away_attack'] + 0.4 * match_data['home_defense']
    )

    return match_data
