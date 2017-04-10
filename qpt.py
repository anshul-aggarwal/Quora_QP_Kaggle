import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
snb = SnowballStemmer("english")
from nltk.corpus import wordnet

f_Tr = open("test.csv").read().split("\n")
testQP = f_Tr[1:-1]
#print(testQP)
for i in range(0, len(testQP)):
    testQP[i] = testQP[i].split(',"')
    for j in range(0,len(testQP[i])):
        testQP[i][j] = testQP[i][j].strip('"')

#print(testQP)
punct = ['?', '.', ',']
tgs = ['N','V','J','R']
#vldc = 0
ot = open("results_test.csv", 'w')

'''
def similarity(tagl1, tagl2):
    ft1 = [(word,tag) for (word,tag) in tagl1 if word not in stopwords.words('english') and word not in punct and (tag.startswith('J') or tag.startswith('V') or tag.startswith('N') or tag.startswith('R'))]
    ft2 = [(word,tag) for (word,tag) in tagl2 if word not in stopwords.words('english') and word not in punct and (tag.startswith('J') or tag.startswith('V') or tag.startswith('N') or tag.startswith('R'))]
    #print(ft1)
    #print(ft2)
    sim_c = 0
    dsim_c = 0
    for (w1,t1) in ft1:
        for (w2,t2) in ft2:
            #print("\n\n")
            #print(w1,t1,w2,t2)
            ws1 = wordnet.synsets(w1)
            ws2 = wordnet.synsets(w2)
            synsim = 0
            #print(ws1,ws2)
            if ws1 and ws2:
                synsim = ws1[0].wup_similarity(ws2[0])
            if synsim is None:
                synsim = 0.0
            #print(synsim)
            if (w1.lower() == w2.lower() or synsim >= 0.5):
                if t1[0] == t2[0]:
                    #print("1")
                    sim_c = sim_c + 1.0
                else:
                    #print("0.7")
                    sim_c = sim_c + 0.7
                #ft1.remove((w1,t1))
                #ft2.remove((w2,t2))    
            else:
                #print("-1")
                dsim_c = dsim_c + 1.0
            #print(sim_c, dsim_c)
    #print("\n\n\n\n")     
    #print(sim_c, dsim_c)       
    dsim_c = dsim_c - (len(ft1) - 1)*(len(ft2) - 1)
    if sim_c >= min(len(ft1),len(ft2)):
        return 1
    
    if dsim_c > 1:
        if sim_c >= dsim_c*2.5:
            return 1
        else:
            return 0
    else:
        return 1
'''    


def similarity(tagl1, tagl2):
    for (word,tag) in tagl1:
        if tag.startswith('J'):
            tag = 'J'
        elif tag.startswith('V'):
            tag = 'V'
        elif tag.startswith('N'):
            tag = 'N'
        elif tag.startswith('R'):
            tag = 'R'
    for (word,tag) in tagl2:
        if tag.startswith('J'):
            tag = 'J'
        elif tag.startswith('V'):
            tag = 'V'
        elif tag.startswith('N'):
            tag = 'N'
        elif tag.startswith('R'):
            tag = 'R'
    #print(tagl1, tagl2)
    ft1 = [(word,tag) for (word,tag) in tagl1 if word not in stopwords.words('english') and word not in punct and tag[0] in tgs]
    ft2 = [(word,tag) for (word,tag) in tagl2 if word not in stopwords.words('english') and word not in punct and tag[0] in tgs]
    #print(ft1)
    #print(ft2)
    sim_c = 0
    dsim_c = 0
    s1 = set(ft1)
    s2 = set(ft2)
    com_set = s1 & s2
    rs1 = s1 - com_set
    rs2 = s2 - com_set
    
    sim_c = sim_c + len(com_set)
    #print(sim_c)
    for (w1,t1) in rs1:
        found = 0 
        for (w2,t2) in rs2:
            ws1 = wordnet.synsets(w1)
            ws2 = wordnet.synsets(w2)
            synsim = 0
            if ws1 and ws2:
                synsim = ws1[0].wup_similarity(ws2[0])
            if synsim is None:
                synsim = 0.0
            if (w1.lower() == w2.lower() or synsim >= 0.5):
                found = 1
                sim_c = sim_c + 1
                #rs1.remove((w1,t1))
                #rs2.remove((w2,t2))    
        if found == 0:
            dsim_c = dsim_c + 1
    #print(sim_c, dsim_c)
    if (sim_c >= min(len(ft1),len(ft2)) - 1) and dsim_c <= 1:
        return 1
    #elif sim_c >= dsim_c:
     #   return 1
    else:
        return 0


pc = 0
ot.write("test_id,is_duplicate\n")
for i in range(0, len(testQP)):
    try:
        if (i%23458) == 0:
            print(pc)
            pc = pc + 1
        q1 = testQP[i][1]
        q2 = testQP[i][2]
        tok1 = nltk.word_tokenize(q1)
        tok2 = nltk.word_tokenize(q2)
        for token in tok1:
            token = token.lower()
        for token in tok2:
            token = token.lower()
        pos1 = nltk.pos_tag(tok1)
        pos2 = nltk.pos_tag(tok2)
        sim = similarity(pos1, pos2)
        '''
        vld = 0
        if int(testQP[i][5]) == sim:
            vld = 1
            vldc = vldc + 1
        '''
        ot.write(testQP[i][0] + "," + str(sim) + "\n")
    except:
        ot.write(str(i) + ",0\n")
        continue
    
#print("\n" + str(vldc*100/len(testQP)))
ot.close()
