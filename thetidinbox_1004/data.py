import tarfile
import pandas as pd

def extract_emails(fname):
    """ Extract the zipped emails and load them into a pandas df """

    rows = []
    # tarfiles are used to read and write tar archives
    originalfile = tarfile.open(fname, 'r:gz')
    for member in originalfile.getmembers():
        if 'ham' in member.name:
            f = originalfile.extractfile(member)
            if f is not None:
                row = f.read()
                rows.append({'message': row, 'class': 'ham'})
        if 'spam' in member.name:
            f = originalfile.extractfile(member)
            if f is not None:
                row = f.read()
                rows.append({'message': row, 'class': 'spam'})
    originalfile.close()

    return pd.DataFrame(rows)

def populate_df(path: str):
    """ Populate the dataframe with all the emails """

    enron_files = path
    emails_df = pd.DataFrame({'message': [], 'class': []})

    unzipped_file = extract_emails(enron_files)
    emails_df = emails_df.append(unzipped_file)
    print("The dimensions of Dataframe created after extracting the tarfile:",emails_df.shape)

    # Dropping all the rows with NA values
    emails_df.dropna()
    # Dropping all the duplicates but keeping the first instance
    emails_df.drop_duplicates(keep='first',inplace=True)
    print("The dimensions of Dataframe after droping rows containing NA values and duplicates: ",emails_df.shape)

    return(emails_df)
