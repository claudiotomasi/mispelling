import codecs, collections, sys
import numpy as np
import glob


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
    for filename in glob.glob('training/*.txt'):
        with codecs.open(filename, 'r', 'utf-8-sig') as tweets:
            for line in tweets:
                line = convert(line)
                for character in line:
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
    state_list = states()
    length_state = len(state_list)
    prior_prob= np.full(length_state, 0.0)
    numb_of_char, total = count_character()
    s = 0.0

    #Transform in frequences numb_of_char
    for k,v in numb_of_char.iteritems():
        prior_prob[state_list.index(k)]=numb_of_char[k]/total
    #Verify if prior_probability sums to 1
    #for i in range(0,length_state):
        #s+=prior_probability[i]
    #print s
    return np.matrix(prior_prob)
def states():
    numb_of_char, total = count_character()
    list_of_states = numb_of_char.keys()
    #print list_of_states
    return list_of_states

def calc_probabilities_transictions(row):
    sum = np.sum(row)
    return row / sum

def transition_model():
    numb_of_char , total= count_character()
    list_of_states = states()
    n_states = len(list_of_states)
    transitions = np.asmatrix(np.full((n_states, n_states), 1.0/sys.maxint))

    for filename in glob.glob('training/*.txt'):
        with codecs.open(filename, 'r', 'utf-8-sig') as tweets:
            for line in tweets:
                line = convert(line)
                for i in range(0, len(line)-1):
                    if line[i]!='\n' and line[i+1]!='\n':
                        row_index = list_of_states.index(line[i])
                        col_index = list_of_states.index(line[i+1])
                        transitions[row_index,col_index]+=1
    transitions = np.apply_along_axis( calc_probabilities_transictions, axis=1, arr=transitions )
    #'print' transitions
    return transitions

def observation():
    observations = states()
    return observations

def emission_probability(adj_list):
    obs = observation()
    n_obs = len(obs)
    print obs
    epsilon = 1.0/1000
    emissions = np.asmatrix(np.full((n_obs, n_obs), 0.0))
    likelihood = 0.8
    for k,v in adj_list.iteritems():
        state = obs.index(k)
        emissions[state, state] += likelihood
        if k != ' ' and k!= '.':
            indexCapital = v.index(k.upper())
            if k.islower():
                low = v[1 : indexCapital]
                up = v[indexCapital :]
                weightLow = 0.15
                weightUp = 0.03
                probLow = weightLow/len(low)
                probUp= weightUp/len(up)
            else:
                low = v[: indexCapital]
                up = v[indexCapital+1 :]
                weightLow = 0.03
                weightUp = 0.15
                probLow = weightLow/len(low)
                probUp= weightUp/len(up)
            for el in low:
                obs_index = obs.index(el)
                emissions[state, obs_index] += probLow
            for el in up:
                obs_index = obs.index(el)
                emissions[state, obs_index] += probUp
        else:
            if k == ' ':
                emissions[state, state]  = 0.9
                weight= 0.08
            else:
                weight= 0.18
            elements= v[1 : ]
            prob = weight/len(elements)
            for el in elements:
                obs_index = obs.index(el)
                emissions[state, obs_index] += prob

        epsilon=0.02/(len(obs)-len(v))
        for j in range(0,len(obs)):
            if emissions[state,j]==0:
                    emissions[state,j] = epsilon

    #print np.sum(emissions, axis=1)
    return emissions
