from hmm import hmm_init
from utility import utility
import hidden_markov as hmlib
import codecs, pickle, argparse
from sklearn import metrics

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--train', help='Training or not', action='store_true')
args = parser.parse_args()
if args.train:
    print "With Training"
    prior = hmm_init.prior_probability()
    transitions = hmm_init.transition_model()
    states=hmm_init.states()
    possible_obs = hmm_init.observation()
    emissions = hmm_init.emission_probability(utility.adjacents())
    model = hmlib.hmm(states, possible_obs, prior, transitions, emissions)
    afile = open('training/model', 'wb')
    pickle.dump(model, afile)
    afile.close()

else:
    print "Without Training"
    afile = open('training/model', 'rb')
    model = pickle.load(afile)
    afile.close()
#print len(states),len(emissions)


states = model.states
tweet = ""
with codecs.open("test/Pontifex_testing.txt" , "r", 'utf-8-sig') as f:
    for tweets in f:
        tweet += hmm_init.convert(tweets)
#elimino newline
tweet = tweet.replace('\n','')
list_of_words = tweet.split('.')
correct = ""
pred = []
real = []
pert = []
for word in list_of_words:
    #se frase non vuota aggiungo un punto alla fine
    if word!= '':
        word+='. '
    obs = list(word)
    #print obs
    if obs!=[]:
        if obs[0]==' ':
            obs = obs[1:]
        if obs[0]!='\n':
            pred += model.viterbi(obs)
            pert += obs
correct += ''.join(pred)

with codecs.open('test/correct.txt', 'w', 'utf-8-sig') as f:
    correct = unicode(correct)
    f.write(correct)


#####BOH
#calcolo liste testo .testo perturbato
tweet = ""
with codecs.open("training/Pontifex_original.txt" , "r", 'utf-8-sig') as f:
    for tweets in f:
        tweet += hmm_init.convert(tweets)
#elimino newline
tweet = tweet.replace('\n','')
list_of_words = tweet.split('.')

for word in list_of_words:
    #se frase non vuota aggiungo un punto alla fine
    if word!= '':
        word+='. '
    obs = list(word)
    #print obs
    if obs!=[]:
        if obs[0]==' ':
            obs = obs[1:]
        if obs[0]!='\n':
            real+= obs
# Funzione duplicata sopare mettere in una funzione
diff_orig_pred = 0
diff_orig_pert = 0
diff_pred_pert = 0
for i in range(0 , len(pred)):
    if real[i] != pred[i]:
        diff_orig_pred+=1
    if pert[i] != real[i]:
        diff_orig_pert+=1
    if pert[i] != pred[i]:
        diff_pred_pert+=1
print "Difference original-predetto: " + str(diff_orig_pred), len(real), len(pred)
print "Difference original-perturbato: " + str(diff_orig_pert)
print "Difference predetto-perturbato: " + str(diff_pred_pert)

#confusion_matrix(real, pred, states, sample_weight=None)
#Si potrebbe calcolare viterbi sulle parole e non sulle frasi
