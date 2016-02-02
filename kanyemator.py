import nltk, re, pprint, glob, random, codecs
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
    for subtree in context.subtrees(lambda t: t.height() == 2):
        if subtree.label() == "NP":
            #add something to ignore WDT tags on their own
            if subtree not in np_set:
                subs = random.choice(np_collection)
                np_set.append(str(subtree))
    subs_dict = {}
    for np in np_set:
        subs = random.choice(np_collection)
        subs_dict[np] = subs
    context_str = str(context).split("\n")
    replaced = []
    for string in context_str:
        stripped = string.strip()
        if stripped in dict.keys(subs_dict):
            replaced.append(subs_dict[stripped])
        else:
            replaced.append(stripped)
            
    # for np in np_set:
    #     subs = random.choice(np_collection)
    #     newTree = nltk.Tree.fromstring(subs)
    #     context_str = str(context).split("\n")
    #     newstring = ""
    #     for m, string in enumerate(context_str):
    #         newstring = string.strip()
    #         if newstring == np:
    #             print newstring, "replaced with: ", subs
    #             context_str[m] = subs
                
        # for pos in context.treepositions(4):
        #     print context[pos]
        #     if str(context[pos]) == np:
        #         context[pos] = newTree
        # for (m, subtree) in enumerate(context.subtrees(lambda t: t.height() == 2)):
        #     if str(subtree) == np:
        #         context.subtrees(lambda t: t.height() == 2)[m] = newTree

    # for string in newtext:
    #     newtext.append(nltk.tag.str2tuple(string.strip())[0])
    # for leaf in context.leaves():
    #     newtext.append(nltk.tag.str2tuple(str(leaf))[0])
    print replaced
    replaced_str = " ".join(replaced)
    replacedTree = nltk.Tree.fromstring(replaced_str)
    newtext = []
    for leaf in replacedTree.leaves():
        newtext.append(nltk.tag.str2tuple(str(leaf))[0])
    newname = "generated_" + str(n) + ".txt"
    newfile = file(newname, 'w')
    newfile.write(" ".join(newtext))
    newfile.close()
                
