#!/usr/bin/env python

import os, sys
import random
import string
import twitter


def make_chains(corpus1, corpus2, n):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""
    chains = {}
    n = int(n)

    input_text1 = corpus1.read() # one long string
    input_text2 = corpus2.read() # another long string

    mashup = input_text1 + input_text2
    #remove punctuation except . , ' ? 
    punctuation = """!#$%&\()*+-/:;<=>@[\\]^_{|}~"""
    for i in punctuation:
        if i in mashup:
            clean_text = mashup.replace(i, "")


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

    while len(sentence) <= 136:

          
        # Get new word (value of key)
        new_word = chains[seed_key] 

        # Randomly choose value from value list if there is more than one option
        new_word = new_word[random.randrange(len(new_word))] 

        #update sentence with current word
        sentence = sentence + " " + new_word

        #update seed key from old seed_key value
        new_key = []
        new_key = list(seed_key[1:])
        new_key.append(new_word)
        seed_key = tuple(new_key) 
        

    return sentence + "."

def post_to_twitter(tweet):
    print os.environ
    if os.environ.get("TWITTER_API_KEY", None) == None:
        print "You need twitter access keys in your shell environment to post to twitter."
        sys.exit()

    api = twitter.Api(consumer_key = os.environ.get("TWITTER_API_KEY"),
                       consumer_secret = os.environ.get("TWITTER_CONSUMER_KEY"),
                       access_token_key = os.environ.get("TWITTER_ACCESS_TOKEN_KEY"),
                       access_token_secret= os.environ.get("TWITTER_ACCESS_TOKEN_SECRET"))

    # api = twitter.Api(consumer_key=os.environ.get("TWITTER_CONSUMER_KEY",
    #     consumer_secret='TWITTER_CONSUMER_SECRET',
    #     access_token_key='TWITTER_ACCESS_TOKEN_KEY',
    #     access_token_secret='TWITTER_ACCESS_TOKEN_SECRET')

    print tweet
    post = raw_input("Do you want to post this to twitter? -->  y/n ")

    if "y" in post:
        return api.PostUpdate(tweet)


def main():
    args = sys.argv

    script, input_file1, input_file2, n = args

    # Change this to read input_text from a file
    corpus1 = open(input_file1)
    corpus2 = open(input_file2)

    chain_dict = make_chains(corpus1, corpus2, n)
    random_text = make_text(chain_dict)
    post_to_twitter(random_text)

if __name__ == "__main__":
    main()