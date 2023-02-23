import pandas as pd

def action_dict():
    action_words = {
    'provide_information': ['inform', 'notify', 'advise', 'announce', 'communicate', 'explain', 'clarify', 'disclose', 'reveal', 'share', 'information', 'details', 'data', 'facts', 'figures', 'statistics', 'specifications', 'instructions', 'guidelines', 'knowledge'],
    'make_a_decision': ['decide', 'determine', 'choose', 'select', 'resolve', 'opt', 'commit', 'settle', 'conclude', 'judge', 'decision', 'choice', 'option', 'selection', 'resolution', 'commitment', 'plan', 'strategy', 'tactic', 'approach'],
    'confirm_approve': ['approve', 'confirm', 'validate', 'authorize', 'ratify', 'endorse', 'accredit', 'certify', 'sanction', 'affirm','confirmation', 'approval', 'validation', 'authorization', 'ratification', 'endorsement', 'accreditation', 'certification', 'sanction', 'affirmation'],
    'give_feedback': ['feedback', 'commenting', 'critique', 'evaluate', 'assess', 'appraise', 'review', 'suggest', 'propose', 'recommend','reply', 'comment', 'critiqued', 'evaluation', 'assessment', 'appraisal', 'review', 'suggestion', 'proposal', 'recommendation'],
}
    actions_df = pd.DataFrame.from_dict(action_words)
    return actions_df

def is_word_present(actions_df, body):
    for col in actions_df:
        for word in actions_df[col]:
            if word in body : return word in body 
    return False

def which_word_present(actions_df, body):
    wordlist = []
    for col in actions_df:
        for word in actions_df[col]:
            if word in body :wordlist.append(word)
    return wordlist

def which_column_present(actions_df, body):
    wordlist = []
    for col in actions_df:
        for word in actions_df[col]:
            if word in body :wordlist.append(col)
    return wordlist

def unique_values(input_list):
    flat_list = [item for sublist in input_list for item in sublist]
    unique_set = set(flat_list)
    unique_list = list(unique_set)
    return unique_list