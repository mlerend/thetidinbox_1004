import pandas as pd

def urgent_vocab_dict():
    urgent_vocab_words =  {
    'urgent_dic': ['urgent', 'urgently', 'critical', 'serious', 'crucial', 'grave', 'priority', 'emergency', 'principal', 'vital', 'essential','top-priotity', 'hurry-up', 'life-and-death', 'life-or-death', 'far-reaching', 'swift', 'time-sensitive', 'all-important', 'most crucial', 'desperate', 'demanding',
    'implore', 'demand', 'request', 'require', 'exhort', 'urge', 'demand', 'beg', 'asap', 'insist', 'key',
    'pressing', 'imperiously', 'vitally', 'emergently', 'desperately', 'extremely', 'primary', 'burning', 'impelling', 'urgently', 'demand',
    'important', 'rapid', 'acute', 'extreme', 'quick', 'fast', 'insistent', 'persistent', 'compelling', 'immediate', 'instant'],

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

#def unique_values(input_list):
    #flat_list = [item for sublist in input_list for item in sublist]
    #unique_set = set(flat_list)
    #unique_list = list(unique_set)
    #return unique_list

def unique_values(df, column_name):
    unique_set = set(df[column_name].tolist())
    unique_list = list(unique_set)
    return unique_list

def urgent_categories(df, urgent_df=urgent_vocab_dict()):
    type(urgent_df)
    df['body'] = df['body'].astype(str)
    df["present"] = df.body.apply(lambda x: is_word_present(urgent_df, x))
    df["wordspresent"] = df.body.apply(lambda x: which_word_present(urgent_df, x))
    df["columnspresent"] = df.body.apply(lambda x: which_column_present(urgent_df, x))
    return df
