import re
import nltk
# import enchant
# from enchant.checker import SpellChecker # keep all non-english words
# from enchant.tokenize import EmailFilter, URLFilter, get_tokenizer

exceptions = ['WEA', '360CH']
keywords = ['child', 'amber', 'plate', 'license', 'lic', 'reg']
rejects = ['tornado', 'weather']
# BAD
# spellChcker = SpellChecker("en_US", filters = [EmailFilter,URLFilter])
# for word in exceptions: # add exceptions to the spell checker
#     spellChcker.add(word)

# TYPE 2    
# dct = enchant.Dict("en_US") # dictionary for english words
# tknzr = get_tokenizer("en_US", filters = [EmailFilter,URLFilter])

def grab_license_plate(wea360ch, desc):
    license_plate = '' # license plate found from the description
    
    modifier = '' #' https://www.youtube.com/watch?v=vdhCzy4Ibps' # dummy code :) :) :) :) :)
    # wea360ch = nltk.tokenize.word_tokenize(wea360ch + modifier, language='english') # use NLTK because it splits everything everything.
    # desc = nltk.tokenize.word_tokenize(desc + modifier, language='english')
    
    # wea360ch = wea360ch.split()
    # desc = desc.split()
    
    # spellChcker.set_text(wea360ch + ' ' + desc)
    # for err in spellChcker:
    #     print('BAD: ', err.word)
    
    # for word in tknzr(wea360ch + ' ' + desc):
    #     if not dct.check(word[0]):
    #         print('TYPE2: ', word[0])
    
    regex = '^(?=.*[A-Z])(?=.*\\d).+$' # contains uppercase (A-Z) and numbers (\d)
    r = re.compile(regex)
    # word_list = wea360ch.split()
    word_list = nltk.tokenize.word_tokenize((wea360ch + desc), language='english')
    # print(word_list)
    
    valid = False
    for word in word_list: # validate word_list
        if word.casefold() in keywords:
            valid = True
            print('valid - contains: ', word)
            break
        if word.casefold() in rejects:
            print('rejected - contains: ', word)
            break
    if not valid: return ''
    
    for word in word_list:
        if (re.search(r, word)) and word not in exceptions and len(word) in [6,7,8]: # if the word is a license plate, aka if the word is 6-8 long (works for US), word is not an exception, and word has a number and a letter by regex
            license_plate = re.sub(r'[^\w\s]', '', word) # strip punctuation
    print("License Plate: " + license_plate)
    print(wea360ch, desc)
    return license_plate
    
        
    
    
    print ('SOURCE: ', wea360ch, desc)
    
    return license_plate

wea360ch, desc = 'WEA 360CH EN: I95 1B3CZ46B7VN501000 Golden Alert: Call Law Enforcement if you have seen Jim Nicholson from Union County KY.  Jim is 5 foot 9 inches tall with white hair.  He is driving a silver Chevy Impala, KY License plate 108ZRK. For more details go to  https://tinyurl.com/mr3hctxn Initiated by Union County Emergency Management.', 'DESCRIPTION EN: 2007 DODGE CHARGER Golden Alert: Call Law Enforcement if you have seen Jim Nicholson from Union County KY.  Jim is 5 foot 9 inches tall with white hair.  He is driving a silver Chevy Impala, KY License plate 108ZRK. For more details go to  https://tinyurl.com/mr3hctxn Initiated by Union County Emergency Management.'
grab_license_plate(wea360ch, desc)