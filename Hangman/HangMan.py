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


def is_word_guessed(secret_word,letters_guessed):
    """
    secret_word - string of lower case letters
    letters_guessed - array of lower case letters
    Returns True if all the letters in secret word are in letters guessed. Otherwise false.
    """
    contains=True
    for letter in secret_word:
        if letter not in letters_guessed:
            contains=False
    return contains


def get_guessed_word(secret_word,letters_guessed):
    """
    secret_word - string of lower case letters
    letters_guessed - array of lower case letters
    Checks which letters in secret word have been guessed.
    Return guessed letters and "_ " for letters not guessed yet in a string. (in same order as the letters in secret_word)
    """
    word_array=[]
    for letter in secret_word:
        if letter in letters_guessed:
            word_array.append(letter)
        else:
            word_array.append("_ ")
    return ''.join(word_array) 


def get_available_letters(letters_guessed):
    """
    letters_guessed - list of lower_case letters
    Returns a string of all lower case English letters that are not in letters_guessed
    """
    list_alphabet=list(string.ascii_lowercase)
    for letter in string.ascii_lowercase:
        if letter in letters_guessed:
            list_alphabet.remove(letter)
    return ''.join(list_alphabet)


def warning_messages(string,guesses,warnings,secret_word,letters_guessed):
    """
    string - An additional string to print to the user.
    guesses - number of guesses left 
    warnings - number of warnings left
    secret_word - the string that the user is trying to guess
    letters_guessed - the letters that have already been guessed by the user.
    Prints a message "Oops! " + string + number of warnings left if any: + the string of letters that's been guessed so far 
    Subtracts one from warning. If no warnings left, subtract one from guess.
    """
    if warnings==0:
        guesses-=1
        print("Oops!  " + string + "  You don't have any warnings left, so you lose a guess: ",get_guessed_word(secret_word,letters_guessed))
    else:
        warnings-=1
        print("Oops!  " + string + "  You have",warnings,"warnings left: ",get_guessed_word(secret_word,letters_guessed))
    return (guesses,warnings)


def unique_char(word):
    """
    word - string of characters in the alphabet
    Returns int, how many unique characters are in the word.
    """
    unique=[]
    for letter in word:
        if letter not in unique:
            unique.append(letter)
    return len(unique)


def hangman(secret_word):
    """"
    secret_word - string of lower case English characters
    Plays the game hangman with a user. User must guess the letters in secret word to win.
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
    secret_word=secret_word.lower() #Make the secret word lowercase
    num_guesses=6 #Numer of guesses allowed for user.
    warnings=3 #Number of warnings allowed for invalid entries or duplicate entries before taking off one guess.
    letters_guessed=[]
    print("Welcome to the game of hangman!")
    print("I am thinking of a word that is",len(secret_word),"letters long.")
    print("You have",num_guesses,"guesses and",warnings,"warnings total.")


    while (num_guesses>0 and not is_word_guessed(secret_word,letters_guessed)):
        print("-------------")
        print("You have",num_guesses," guesses left.")
        print("Available letters: ",get_available_letters(letters_guessed))
        guess=input("Please type a letter to guess:  ")
        guess=guess.lower()
        if not guess.isalpha():
            message="You entered an invalid character (only alphabetic characters allowed)."
            (num_guesses,warnings)=warning_messages(message,num_guesses,warnings,secret_word,letters_guessed) 
        elif guess in letters_guessed:
            message="You already guessed that letter."
            (num_guesses,warnings)=warning_messages(message,num_guesses,warnings,secret_word,letters_guessed) 
        elif guess in secret_word:
            letters_guessed.append(guess)
            print("Good guess:  ",get_guessed_word(secret_word,letters_guessed))
        else:
            letters_guessed.append(guess)
            print("Oops! That letter is not in my word:  ",get_guessed_word(secret_word,letters_guessed))
            if guess in "aeiou":
                num_guesses-=2 #Lose an extra guess (two guesses) if the user guessed a vowel.
            else:
                num_guesses-=1 #Lose one guess if the user guessed a consonant.

    print("-------------")
    if is_word_guessed(secret_word,letters_guessed):
        print("Congratulations! You won the game of hangman!")
        #Score is number of guesses left multiplied by the number of unique characters.
        score=num_guesses*unique_char(secret_word) 
        print("Your score is",str(score)+".")
    else:
        print("Sorry, you lost of the game of hangman. The word was",secret_word+".")


if __name__ == "__main__":
    secret_word = choose_word(wordlist)
    hangman(secret_word)