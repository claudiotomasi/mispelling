from hmm import hmm_init
from utility import utility
import hidden_markov as hmlib
import codecs

prior = hmm_init.prior_probability()
transitions = hmm_init.transition_model()
states=hmm_init.states()
possible_obs = hmm_init.observation()
emissions = hmm_init.emission_probability(utility.adjacents())

print len(states),len(emissions)

model = hmlib.hmm(states, possible_obs, prior, transitions, emissions)
string_tweets = ""
with codecs.open("training/test.txt" , "r", 'utf-8-sig') as f:
    for tweet in f:
        tweet = hmm_init.convert(tweet)
        string_tweets+=tweet
obs = list(string_tweets)
print ''.join(model.viterbi(obs[:len(obs)-1]))
