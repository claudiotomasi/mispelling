from hmm import hmm_init
from utility import utility
import hidden_markov as hmlib
import codecs, pickle, argparse, glob, csv
from sklearn import metrics
import numpy as np
from flask import Flask, request, jsonify, render_template

def confusion(states):
    real = ""
    with codecs.open('remain/Pontifex_test_of_remains.txt' , "r", 'utf-8-sig') as f:
        for s in f:
            real+=s
    real = list(real)
    pred = ""
    with codecs.open('test/Pontifex_test_of_remains.txt_correct' , "r", 'utf-8-sig') as f:
        for s in f:
            #print s
            pred+=s
    pred = list(real)

    matrix = metrics.confusion_matrix(real,pred,states)
    with open('csv/confusion.csv', 'wb') as f:
        writer = csv.writer(f)

        writer.writerow(states)
        for i in range(0, matrix.shape[0]):
            writer.writerows(matrix[i:])

if __name__ == '__main__':
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
        print "End of training\n"

    else:
        print "Without Training\n"
        afile = open('training/model', 'rb')
        model = pickle.load(afile)
        afile.close()
    for filename in glob.glob('remain/Pontifex_test_of_remains.txt'):
        tweet = ""
        with codecs.open(filename , "r", 'utf-8-sig') as f:
            print "Start prediction of "+filename+"..."
            for tweets in f:
                tweet += hmm_init.convert(tweets)
        #elimino newline
        tweet = tweet.replace('\n','')
        #separo per frasi

    states = model.states
        # list_of_words = tweet.split('.')
    list_of_words = tweet.split()

    correct = ""

    for word in list_of_words:
        pred = []
        #se frase non vuota aggiungo un punto alla fine
        if word!= '':
            word+=' '
        obs = list(word)
        #print obs
        if obs!=[]:
            # Rimuovo spazi all'inizio
            if obs[0]==' ':
                obs = obs[1:]
            if obs[0]!='\n':
                pred += model.viterbi(obs)
    #trasformo lista predizioni in stringa

        correct += ''.join(pred)
    with codecs.open(filename+'_correct', 'w', 'utf-8-sig') as f:
        correct = unicode(correct)
        f.write(correct)
    print "End prediction of "+filename+"\n"

    #eeconfusion(states)
