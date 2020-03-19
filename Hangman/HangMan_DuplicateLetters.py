
import string
import random

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
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


# Load the list of words into the variable wordlist so that it can be accessed from anywhere in the program
wordlist = load_words()


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


def get_guessed_word(secret_word,updated_word):
    """
    secret_word - string of lower case letters
    updated_word - list of lower case letters that have not been guessed yet
    Checks which letters in secret word have been guessed.
    Return guessed letters and "_ " for letters not guessed yet in a string. (in same order as the letters in secret_word)
    """
    word_array=[]
    index2=0
    for index in range(len(secret_word)):
        if index2<len(updated_word) and secret_word[index]==updated_word[index2]: #Letter not guessed yet
            word_array.append("_ ")
            index2+=1
        else:
            word_array.append(secret_word[index])
    return ''.join(word_array) 

def get_available_letters(already_guessed):
    """
    already_guessed - list of lower_case letters already guessed incorrectly by user
    Returns a string of all lower case English letters that are not in already guessed
    """
    list_alphabet=list(string.ascii_lowercase)
    for letter in string.ascii_lowercase:
        if letter in already_guessed:
            list_alphabet.remove(letter)
    return ''.join(list_alphabet)


def warning_messages(string,guesses,warnings,secret_word,updated_word):
    """
    string - An additional string to print to the user.
    guesses - number of guesses left 
    warnings - number of warnings left
    secret_word - the string that the user is trying to guess
    updated_word - the letters that have not been guessed yet by the user.
    Prints a message "Oops! " + string + number of warnings left if any: + the string that's been guessed so far 
    Subtracts one from warning. If no warnings left, subtract one from guess.
    """
    if warnings==0:
        guesses-=1
        print("Oops!  " + string + "  You don't have any warnings left, so you lose a guess: ",get_guessed_word(secret_word,updated_word))
    else:
        warnings-=1
        print("Oops!  " + string + "  You have",warnings,"warnings left: ",get_guessed_word(secret_word,updated_word))
    return (guesses,warnings)

def match_with_gaps(my_word,other_word,already_guessed):
    """
    my_word - what is guessed so far of the word (with blanks Ex: t _ _ t)
    other_word - normal English word
    already_guessed - list of letters that have already been guessed by user
    Returns true if my word matches the corresponding letters of other_word, and the words match length. Otherwise returns false.
    """
    match=True
    index=0
    other_word=other_word.strip() #Get rid of leading space characters
    my_word=my_word.replace(" ","") #Remove spaces in my word
    if len(my_word) != len(other_word): #Words have different lengths
        return False
    while match and index<len(other_word):
        if my_word[index]!="_":
            if other_word[index] != my_word[index]: #Letters don't match
                match=False
        else:
            if other_word[index] in already_guessed:
                match=False #Other word contains a letter that was already guessed.
            if other_word[index] in my_word[index:len(my_word)]:
                match=False #Letter was guessed correctly and it appears later in word. So this word is not possible. (guesses happen left to right)
        index+=1
    return match


def show_possible_matches(my_word,already_guessed):
    """
    my_word - what is guessed so far of the word (with blanks Ex: t _ _ t)
    already_guessed - list of letters that have already been guessed by user
    Prints out a list of possible matches in the wordlist.
    """
    matches=[] #List of words that might be a match
    for word in wordlist:
        if match_with_gaps(my_word,word,already_guessed):
            matches.append(word)
    if len(matches)==0:
        return "No matches found"
    else:
        return ' '.join(matches)


def unique_char(word):
    """
    word - string of characters in the alphabet
    Returns how many unique characters are in the word.
    """
    unique=[]
    for letter in word:
        if letter not in unique:
            unique.append(letter)
    return len(unique)


def hangman_duplicates(secret_word):
    """
    secret_word - string of lower case English characters
    Plays the game hangman with a user. User must guess the letters in secret word to win. 
    This game forces you to guess every letter even if there are two of the same letter in the word. 
    This version of hang man gives more specific hints. It eliminates possibilities from the already guessed list.
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    """
    secret_word=secret_word.lower()  
    num_guesses=6 #Max guesses allowed for user.
    warnings=3    #Max number of warnings allowed
    updated_word=list(secret_word) #Make a copy of the word. The copy contains an array of characters
    already_guessed=[] #Holds letters that user guessed multiple times even though they already got it wrong
    print("Welcome to the game of hangman!")
    print("I am thinking of a word that is",len(secret_word),"letters long.")
    print("You have",num_guesses,"guesses and",warnings,"warnings total.")
    
    #Loop until the user used all guesses or they guessed the correct word.
    while (num_guesses>0 and len(updated_word)>0):
        print("-------------")
        print("You have",num_guesses," guesses left.")
        print("Available letters: ",get_available_letters(already_guessed))
        guess=input("Please guess a letter:  ")
        guess=guess.lower() #Make the guess lower case
        if guess=="*": #User wants a hint.
            print("Possible word matches are:")
            print(show_possible_matches(get_guessed_word(secret_word,updated_word),already_guessed))
        elif not guess.isalpha():
            message="You entered an invalid character (only alphabetic characters allowed)."
            (num_guesses,warnings)=warning_messages(message,num_guesses,warnings,secret_word,updated_word) 
        elif (guess in updated_word):
            updated_word.remove(guess) #Remove the guessed letters.
            print("Good guess: ",get_guessed_word(secret_word,updated_word))
        elif guess in already_guessed: #Letter already guessed once incorrectly
            message="You already guessed that letter."
            (num_guesses,warnings)=warning_messages(message,num_guesses,warnings,secret_word,updated_word)  
        #Guess is in secret word, but user already guessed the correct number of this letter.
        elif (guess in secret_word):  
            already_guessed.append(guess) #Add to the already guessed list (if user guesses again it results in a warning rather than a missed guess)
            print("Oops! You already guessed the correct number of this letter: ",get_guessed_word(secret_word,updated_word))
            num_guesses-=1
        else:
            already_guessed.append(guess)
            print("Oops! That letter is not in my word:  ",get_guessed_word(secret_word,updated_word))
            if guess in "aeiou":
                num_guesses-=2 #Lose an extra guess (two guesses) if the user guessed a vowel.
            else:
                num_guesses-=1 #Lose one guess if the user guessed a consonant.

    print("-------------") 
    if len(updated_word)==0: #All letters were guessed
        print("Congratulations! You won the game of hangman!")
        #Score is number of guesses left multiplied by the number of unique characters.
        score=num_guesses*unique_char(secret_word) 
        print("Your score is",str(score)+".")
    else:
        print("Sorry, you lost of the game of hangman. The word was",secret_word+".")

if __name__ == "__main__":
    secret_word = choose_word(wordlist)
    hangman_duplicates(secret_word)