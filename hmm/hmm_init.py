import codecs, collections, sys
import numpy as np
def convert_keys_to_string(dictionary):
    """Recursively converts dictionary keys to strings."""
    if not isinstance(dictionary, dict):
        return dictionary
    return dict((str(k), convert_keys_to_string(v))
        for k, v in dictionary.items())

def convert(data):
    if isinstance(data, basestring):
        return data.encode('utf-8')
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

def count_character():
    number_of_characters = {}
    total_characters = 0.0
    with codecs.open('training/Pontifex_text.txt', 'r', 'latin') as tweets:
        for line in tweets:
            line = convert(line)
            for character in line:
                character=character.lower()
                if character != '\n':
                    if character in number_of_characters.keys():
                        number_of_characters[character]+=1
                    else:
                        number_of_characters[character]=1
                    total_characters +=1;
    #for k in number_of_characters:
    #    print repr(k), number_of_characters[k]
    #print total_characters, number_of_characters
    return number_of_characters, total_characters

def prior_probability():
    prior_prob={}
    numb_of_char, total = count_character()
    s = 0.0

    #Transform in frequences numb_of_char
    for k,v in numb_of_char.iteritems():
        prior_prob[k]=numb_of_char[k]/total
    #Verify if prior_probability sums to 1
    for k,v in prior_prob.iteritems():
        s+=v
    #print s

def states():
    numb_of_char, total = count_character()
    list_of_states = numb_of_char.keys()
    #print list_of_states
    return list_of_states

def calc_probabilities(row):
    sum = np.sum(row)
    return row / sum


def transition_model():
    numb_of_char , total= count_character()
    list_of_states = states()
    n_states = len(list_of_states)
    transitions = np.asmatrix(np.full((n_states, n_states), 1.0/sys.maxint))
    with codecs.open('training/Pontifex_text.txt', 'r', 'latin') as tweets:
        for line in tweets:
            line = convert(line).lower()
            for i in range(0, len(line)-1):
                if line[i]!='\n' and line[i+1]!='\n':
                    row_index = list_of_states.index(line[i])
                    col_index = list_of_states.index(line[i+1])
                    transitions[row_index,col_index]+=1
    transitions = np.apply_along_axis( calc_probabilities, axis=1, arr=transitions )
    print transitions
    # return transitions
