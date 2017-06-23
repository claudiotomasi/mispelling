from hmm import hmm_init
from utility import utility
import hidden_markov as hmlib
import codecs

prior = hmm_init.prior_probability()
transitions = hmm_init.transition_model()
states=hmm_init.states()
possible_obs = hmm_init.observation()
emissions = hmm_init.emission_probability(utility.adjacents())


model = hmlib.hmm(states, possible_obs, prior, transitions, emissions)
string_tweets = ""
with codecs.open("training/Pontifex_testing.txt" , "r", 'utf-8-sig') as f:
    for tweet in f:
        tweet = hmm_init.convert(tweet)
        string_tweets+=tweet
obs = string_tweets.split()
print model.viterbi(obs)
