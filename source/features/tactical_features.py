import pandas as pd

def create_tactical_features(match_data):

    tactical_data = match_data.copy()

    tactical_data['goal_difference'] = (tactical_data['home_team_goal'] - tactical_data['away_team_goal'])

    tactical_data['attack_balance'] = (tactical_data['home_attack'] - tactical_data['away_defense'])

    tactical_data['defense_balance'] = (tactical_data['home_defense'] - tactical_data['away_defense'])

    tactical_data['form_balance'] = (tactical_data['home_form'] - tactical_data['away_form'])

    tactical_data['goal_potential'] = (tactical_data['home_attack'] + tactical_data['away_attack'])


    return tactical_data