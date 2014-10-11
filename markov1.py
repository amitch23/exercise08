#!/usr/bin/env python

import sys
import random
import string

def make_chains(corpus, n):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""
    chains = {}
    n = int(n)

    input_text = corpus.read() # one long string

    #remove punctuation except . , ' ? 
    punctuation = """!#$%&\()*+-/:;<=>@[\\]^_{|}~"""
    for i in punctuation:
        if i in input_text:
            clean_text = input_text.replace(i, "")


    word_list = clean_text.split() # store corpus in one long string

    #Loop through giant list and assign keys to empty dict
    for i in range(len(word_list)-n):
        key_tuple = []
        for j in range(n):
            key_tuple.append(word_list[i+j])

        key = tuple(key_tuple)
        #assign value from key
        value = word_list[i+n]
        
        #add values to multiple occurances of pair word keys
        if key not in chains:       # If word pair is not already in dictionary
            chains[key] = [value]
        else:                       # If word pair is in dictionary (append to value list)
            chains[key].append(value)

    # get chains, a dict of keys as strings in tuple and values as list of strings
    # print chains
    return chains

def make_text(chains):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""

    #assign key_list to key/tuple group
    keys_list = chains.keys()

    # Test random keys until a value with capital letter is found
    not_found = True    
    while not_found:
        option = random.choice(keys_list)# randomly selects a key from dictionary (key is a tuple)
       
        if chains[option][0][0] in string.ascii_uppercase:
            seed_key = option #tuple
            new_word = chains[seed_key] #list
            not_found = False
    
    sentence = ""

    # while new_word[-1] not in ".?!":

    while len(sentence) < 140:

          
        # Get new word (value of key)
        new_word = chains[seed_key] # values list
        # chooses value from value list if there is more than one option
        new_word = new_word[random.randrange(len(new_word))] 
        #update sentence string
        sentence = sentence + " " + new_word + "."

        #update seed key from old seed_key value
        new_key = []
        new_key = list(seed_key[1:])
        new_key.append(new_word)
        seed_key = tuple(new_key) #make list a tuple 
        
            

    return sentence 

def main():
    args = sys.argv

    script, input_file, n = args

    # Change this to read input_text from a file
    corpus = open(input_file)

    chain_dict = make_chains(corpus1, n)
    random_text = make_text(chain_dict)
    print random_text
#random comment to see if pushing works
if __name__ == "__main__":
    main()