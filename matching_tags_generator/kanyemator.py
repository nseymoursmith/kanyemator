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
            # get tags. WDT and PRP, and containing POS at start
            # will need special treatment
            tags = []
            for leaf in subtree.leaves():
                tags.append(nltk.tag.str2tuple(leaf)[1])
            if subtree not in np_set:
                np_set.append((str(subtree), tags))
    subs_dict = {}
    for np in np_set:
        matches = []
        for obj in np_collection:
            tree = nltk.Tree.fromstring(obj)
            tags = []
            for leaf in tree.leaves():
                tags.append(nltk.tag.str2tuple(leaf)[1])
            if tags == np[1]:
                matches.append(obj)
        subs = random.choice(matches)
        subs_dict[np[0]] = subs
    context_str = str(context).split("\n")
    replaced = []
    for string in context_str:
        stripped = string.strip()
        if stripped in dict.keys(subs_dict):
            replaced.append(subs_dict[stripped])
        else:
            replaced.append(stripped)
    replaced_str = " ".join(replaced)
    replacedTree = nltk.Tree.fromstring(replaced_str)
    newtext = []
    for leaf in replacedTree.leaves():
        newtext.append(nltk.tag.str2tuple(str(leaf))[0])
    newname = "generated_" + str(n) + ".txt"
    newfile = file(newname, 'w')
    newfile.write(" ".join(newtext))
    newfile.close()
                
