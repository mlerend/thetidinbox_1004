import pandas as pd

def urgent_vocab_dict():
    urgent_vocab_words =  {
    'urgent_syn_noun': ['urgent', 'urgently', 'critical', 'serious', 'crucial', 'grave', 'priority', 'emergency', 'principal', 'vital', 'essential'],
    'idioms_nouns': ['top-priotity', 'hurry-up', 'life-and-death', 'life-or-death', 'far-reaching', 'swift', 'time-sensitive', 'all-important', 'most crucial', 'desperate', 'demanding'],
    'urgent_verbs': ['implore', 'demand', 'request', 'require', 'exhort', 'urge', 'demand', 'beg', 'ask for', 'insist', 'key'],
    'urgent_adv': ['pressing', 'imperiously', 'vitally', 'emergently', 'desperately', 'extremely', 'primary', 'burning', 'impelling', 'urgently', 'demand'],
    'curgent_syn_noun2': ['important', 'rapid', 'acute', 'extreme', 'quick', 'fast', 'insistent', 'persistent', 'compelling', 'immediate', 'instant'],

}
    urgent_df = pd.DataFrame.from_dict(urgent_vocab_words)
    return urgent_df

def is_word_present(urgent_df, body):
    for col in urgent_df:
        for word in urgent_df[col]:
            if word in body : return word in body
    return False

def which_word_present(urgent_df, body):
    wordlist = []
    for col in urgent_df:
        for word in urgent_df[col]:
            if word in body :wordlist.append(word)
    return wordlist

def which_column_present(urgent_df, body):
    wordlist = []
    for col in urgent_df:
        for word in urgent_df[col]:
            if word in body :wordlist.append(col)
    return wordlist

def unique_values(input_list):
    flat_list = [item for sublist in input_list for item in sublist]
    unique_set = set(flat_list)
    unique_list = list(unique_set)
    return unique_list
