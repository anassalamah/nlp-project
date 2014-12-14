
import re

if __name__ == "__main__":

    
    text = "this,\,nations,+2,gwrg"
    text2 = "ggwger gvgve rgvgre efefwe cdc this fewg"
    
    for word in text.split(','):
        try:
            finds = re.findall(word, text)
            print finds
        except:
            print "couldnt use", word, "as re"
