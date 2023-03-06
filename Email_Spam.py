import pandas as pd
import random
import re

# drop NaN columns
def drop_col(df):
    column = df.columns
    removed_col = []
    for c in column:
        if df[c].isnull().values.any():
            removed_col.append(c)
    df = df.drop(labels=removed_col, axis=1)
    df.head()

    return df

# remove empty string from the list of string in each email
def clean_list(line):
    removed_words = []
    for i in range(len(line) - 1):
        if line[i] == '':
            removed_words.append(line[i])
        else:
            for s in line[i]:
                if s < 'a' and s > 'Z':
                    #print(w)
                    removed_words.append(line[i])
                    break
                elif s > 'z':
                    #print(w)
                    removed_words.append(line[i])
                    break
                elif s < 'A':
                    #print(w)
                    removed_words.append(line[i])
                    break
                    
    last_word = line[len(line)-1]
    last_word = last_word[:-1]
    line[-1] = last_word
    
    if last_word == '':
        removed_words.append(last_word)
    else:
        for s in last_word:
            if s < 'a' and s > 'Z':
                #print(w)
                removed_words.append(last_word)
                break
            elif s > 'z':
                #print(w)
                removed_words.append(last_word)
                break
            elif s < 'A':
                #print(w)
                removed_words.append(last_word)
                break

    
    for i in removed_words:
        line.remove(i)
        
    return line


# Split the email string into a list of words
def clean_email(msg, label):
    data = {}
    
    line = re.split(r"[:,. ]", msg)
    line = clean_list(line)
    
    data['email'] = line
    data['label'] = label
    
    return data


# clean dataset from the df
def clean_data(df):
    email_list = []

    # iterate through all emails
    for i in range(len(df)):
        msg = df.iloc[i, 1]
        label = df.iloc[i, 0]
        email = clean_email(msg, label)
        
        email_list.append(email)

    print(f'first 2 emails')
    print(email_list[:2])
    return email_list


# split the dataset
def split_data(email_list):
    tot_email = len(email_list)
    mid = int(0.7*tot_email)

    # shuffle the dataset
    random.shuffle(email_list)

    train_data = email_list[:mid]
    test_data = email_list[mid:]

    print(f'70/30% split')
    print(f'train data: {len(train_data)}')
    print(f'test data: {len(test_data)}')

    return train_data, test_data


# find frequency of each word in the email
def find_freq(cur_dict, freq_list):
    for i in cur_dict['email']:
        if i not in freq_list:
            freq_list[i] = 1
        else:
            freq_list[i] += 1
            
    return freq_list


# find probability of each word
def find_prob(train_data):
    spam_freq = {}
    ham_freq = {}

    for i in train_data:
        if i['label'] == 'spam':
            spam_freq = find_freq(i, spam_freq)
        elif i['label'] == 'ham':
            ham_freq = find_freq(i, ham_freq)
            
    ham_word_cnt = 0
    spam_word_cnt = 0
    for i in spam_freq:
        spam_word_cnt += spam_freq[i]
    for i in ham_freq:
        ham_word_cnt += ham_freq[i]
        
    spam_prob = {}
    ham_prob = {}
    for i in spam_freq:
        spam_prob[i] = spam_freq[i] / spam_word_cnt
    for i in ham_freq:
        ham_prob[i] = ham_freq[i] / ham_word_cnt

    return spam_prob, ham_prob


# calculate accuracy
def check_spam_ham(spam_prob, ham_prob, test_data):
    num_right = 0
    # iterate through each email
    for email in test_data:
        check = ''
        prob_in_spam = 1
        prob_in_ham = 1
        for w in email['email']:
            if w in spam_prob and w in ham_prob:
                prob_in_spam *= spam_prob[w]
                prob_in_ham *= ham_prob[w]
        
        if prob_in_spam > prob_in_ham:
            check = 'spam'
        else:
            check = 'ham'
            
        if email['label'] == check:
            num_right += 1
        
    accuracy = num_right / len(test_data)
    return accuracy   



if __name__ == '__main__':
    df = pd.read_csv('spam.csv', encoding = 'latin')
    df = drop_col(df)

    email_list = clean_data(df)
    print()
    train_data, test_data = split_data(email_list)

    # find the probability of the all the words in email
    spam_prob, ham_prob = find_prob(train_data)

    # testing the probability of words from test_data
    accuracy = check_spam_ham(spam_prob, ham_prob, test_data)
    print()
    print(f'accuracy is: {accuracy * 100:.3f} %')


