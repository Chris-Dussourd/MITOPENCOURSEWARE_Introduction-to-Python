# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Chris Dussourd
# Time spent    : 4 hours 30 minutes

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*': 0
}


WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    wordlen=len(word)
    word=word.lower() #Make word lower case (dictionary stores letters as lower case)
    sum_word_points=0 #Sum of points for letters in word
    for letter in word:
        sum_word_points+=SCRABBLE_LETTER_VALUES[letter]

    word_length_points=7*wordlen-3*(n-wordlen)
    if word_length_points<1:
        word_length_points=1 #Second component must be at least 1 point
    return sum_word_points*word_length_points


def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n-1 lowercase letters and one wildcard (*).
    ceil(n/3)-1 letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))-1

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    hand['*']=1 #Add  wild-card

    for i in range(num_vowels+1, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    #Copy hand, don't modify hand
    hand_updated=hand.copy()
    word=word.lower()
    #For each letter in word, decrease the updated hand by one (delete if updated hand would be zero)
    for letter in word:
        if (letter in hand_updated):
            if hand_updated.get(letter,0)>1:
                hand_updated[letter]=hand_updated.get(letter,0)-1
            else:
                del(hand_updated[letter])
    return hand_updated


#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    valid=False
    hand_temp=hand.copy() #Make copy to prevent mutating
    word=word.lower()
    for vowel in VOWELS:
        word_vowel=word.replace("*",vowel) #Replace wildcard with vowel
        if word_vowel in word_list:
            valid=True
    for letter in word:
        if hand_temp.get(letter,0)>0:
            hand_temp[letter]=hand_temp.get(letter,0)-1
        else:
            valid=False #All letters are not composed in the hand
    return valid



#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    return sum(hand.values())


def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    # Keep track of the total score
    total=0
    # As long as there are still letters left in the hand:
    while(calculate_handlen(hand)>0):
        # Display the hand
        print("\nCurrent hand:",end=' ')
        display_hand(hand)
        # Ask user for input
        word=input('Enter a word, or "!!" to indicate that you are finished:  ')
        # If the input is two exclamation points:
        if word=="!!":
            # End the game (break out of the loop)
            break
            
        # Otherwise (the input is not two exclamation points):
        else:
            # If the word is valid:
            if is_valid_word(word,hand,word_list):
                # Tell the user how many points the word earned,
                # and the updated total score
                score=get_word_score(word,calculate_handlen(hand))
                total+=score
                print('"'+word+'" earned',str(score),"points.  Total: ",total)

            # Otherwise (the word is not valid):
            else:
                # Reject invalid word (print a message)
                print("That is not a valid word. Please choose another word.")
            # update the user's hand by removing the letters of their inputted word
            hand=update_hand(hand,word)

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score
    if calculate_handlen(hand)==0:
        print("You ran out of letters.")
    print("Total score for this hand: ",total)
    # Return the total score for hand as result of function
    return total



#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    #Create a list from consonants and vowels
    str_letters= VOWELS + CONSONANTS
    #Loop through letters in hand and remove them from the list (using the replace function)
    for hand_letters in hand:
        str_letters=str_letters.replace(hand_letters,'')
    #Choose random consonant or vowel from string
    new_letter = random.choice(str_letters)
    #Copy hand
    sub_hand=hand.copy()
    #In sub_hand, set the new random letter to the value of the letter passed in by user
    sub_hand[new_letter]=hand.get(letter,0)
    #Delete the letter passed in by user from sub_hand
    del(sub_hand[letter])
    #Return the substitute hand
    return sub_hand


def is_int(x):
    """
    Tries to cast x as an integer. Returns a false if unable to.
    """
    try:
        int(x)
        return True
    except ValueError:
        return False
   
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    #Ask user to input the number of hands
    num_hands_input=input("Please input the number of hands to play:  ")
    while not is_int(num_hands_input) or math.isnan(int(num_hands_input)):
        num_hands_input=input("You did not enter an integer. Please input the number of hands to play:  ")
    num_hands=int(num_hands_input)
    #Initialize substitute hands. User is allowed to sub a letter this many times per game
    num_sub_hands=1
    #Initialize the number of replays allowed (user replays hand and keeps better score)
    num_replays=1
    #Initialize the total score counter (total score for all hands)
    total=0
    #Loop through and play the number of hands inputed by the user
    for i in range(num_hands):
        #Deal a hand out
        hand=deal_hand(HAND_SIZE)
        if num_sub_hands>0:
            #Display hand to user
            print("Current hand:",end=' ')
            display_hand(hand)
            #Ask user if he wants to substitute hands
            sub_hand_yn=input('Would you like to substitute hands (Enter "yes" if so):  ')
            #If user entered yes, sub hand and decrement from total num_sub_hands allowed
            if sub_hand_yn=="yes":
                #Ask user what letter to substitute
                letter=input("Which letter would you like to substitute: ")
                #Check to make sure letter is in hand
                while letter not in hand:
                    letter=input("The letter you entered is not in your hand. Please enter a letter to substitute:  ")
                #Substitute letter for a random new one
                hand=substitute_hand(hand,letter)
                num_sub_hands-=1
        
        #Copy hand (in case user wants to replay it) and then play it
        current_hand=hand.copy()
        score=play_hand(current_hand,word_list)
        print("----------")
        #Ask user if they want a replay (if they have replays left and this is not a current replay)
        if num_replays>0:
            #Ask user if they would like to replay the hand
            replay_hand_yn=input('Would you like to replay the hand (Enter "yes" if so): ')
            if replay_hand_yn=="yes":
                #Decrement number of replays allowed
                num_replays-=1
                score_old=score
                score_new=play_hand(hand,word_list)
                print("----------")
                #Take the best score for the two hands
                total+=max([score_old, score_new])
        else:
            #Add score to total if no replay
            total+=score
        
    #Print out the total score
    print("Total score over all hands: ",total)
    return total


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
