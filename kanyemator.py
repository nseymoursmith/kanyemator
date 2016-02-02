import nltk, re, pprint, glob, random
from nltk import word_tokenize

filelist = glob.glob("./np_chunks/*.npch")
collfile = file("np_collection.npch", 'r')
np_collection = collfile.read().split("~")
collfile.close()
for (n, txtfile) in enumerate(filelist):
    print "====== processing chunk file: ", txtfile, " ======"
    np_chunked = file(txtfile, 'r')
    raw = np_chunked.read()
    np_chunked.close()
    context = nltk.Tree.fromstring(raw)
    np_set = []
    for subtree in context.subtrees():
        if subtree.label() == "NP":
            if subtree not in np_set:
                np_set.append(str(subtree))
    for np in np_set:
        subs = random.choice(np_collection)
        newTree = nltk.Tree.fromstring(subs)
        for (m, subtree) in enumerate(context.subtrees()):
            if str(context[m]) == np:
                context[m] = newTree
    print context.leaves()

                
