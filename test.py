from enchant.checker import SpellChecker # keeping all non-english words
from enchant.tokenize import EmailFilter, URLFilter

spellChcker = SpellChecker("en_US", filters = [EmailFilter,URLFilter])
def grab_license_plate(wea360ch, desc):
    license_plate = ''
    
    modifier = '' #' https://www.youtube.com/watch?v=vdhCzy4Ibps' # dummy code :) :) :) :) :)
    # wea360ch = nltk.tokenize.word_tokenize(wea360ch + modifier, language='english') # use NLTK because it splits everything everything.
    # desc = nltk.tokenize.word_tokenize(desc + modifier, language='english')
    
    # wea360ch = wea360ch.split()
    # desc = desc.split()
    
    spellChcker.set_text(wea360ch + ' ' + desc)
    for err in spellChcker:
        print('BAD: ', err.word)
    
    print ('SOURCE: ', wea360ch, desc)
    
    return license_plate

wea360ch, desc = 'WEA 360CH EN: 1B3CZ46B7VN501000 Golden Alert: Call Law Enforcement if you have seen Jim Nicholson from Union County KY.  Jim is 5 foot 9 inches tall with white hair.  He is driving a silver Chevy Impala, KY License plate 108ZRK. For more details go to  https://tinyurl.com/mr3hctxn Initiated by Union County Emergency Management.', 'DESCRIPTION EN: 2007 DODGE CHARGER Golden Alert: Call Law Enforcement if you have seen Jim Nicholson from Union County KY.  Jim is 5 foot 9 inches tall with white hair.  He is driving a silver Chevy Impala, KY License plate 108ZRK. For more details go to  https://tinyurl.com/mr3hctxn Initiated by Union County Emergency Management.'
grab_license_plate(wea360ch, desc)