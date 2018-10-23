import json
from data_util import sentence

def strong_composition(signature1, signature2, relation1, relation2):
    #returns the stronger relation of the first relation/signature composed
    #with the second relation signature and vice sersa
    composition1 = relation_composition[(signature1[relation1], signature2[relation2])]
    composition2 = relation_composition[(signature2[relation2], signature1[relation1])]
    if composition1 == "independence":
        return composition2
    if composition2 != "independence" and composition1 != composition2:
        print("This shouldn't happen", composition1, composition2)
    return composition1

#creates MacCartney's join operator
relations = ["equivalence", "entails", "reverse entails", "contradiction", "cover", "alternation", "independence"]
relations2 = ["equivalence", "entails", "reverse entails", "contradiction", "cover", "alternation", "independence"]
relation_composition= dict()
for r in relations:
    for r2 in relations2:
        relation_composition[(r,r2)] = "independence"
for r in relations:
    relation_composition[("equivalence", r)] = r
    relation_composition[(r,"equivalence")] = r
relation_composition[("entails", "entails")] = "entails"
relation_composition[("entails", "contradiction")] = "alternation"
relation_composition[("entails", "alternation")] = "alternation"
relation_composition[("reverse entails", "reverse entails")] = "reverse entails"
relation_composition[("reverse entails", "contradiction")] = "cover"
relation_composition[("reverse entails", "cover")] = "cover"
relation_composition[("contradiction", "entails")] = "cover"
relation_composition[("contradiction", "reverse entails")] = "alternation"
relation_composition[("contradiction", "contradiction")] = "equivalence"
relation_composition[("contradiction", "cover")] = "reverse entails"
relation_composition[("contradiction", "alternation")] = "entails"
relation_composition[("alternation", "reverse entails")] = "alternation"
relation_composition[("alternation", "contradiction")] = "entails"
relation_composition[("alternation", "cover")] = "entails"
relation_composition[("cover", "entails")] = "cover"
relation_composition[("cover", "contradiction")] = "reverse entails"
relation_composition[("cover", "alternation")] = " reverse entails"
#create the signatures for negation
negation_signature = {"equivalence":"equivalence", "entails":"reverse entails", "reverse entails":"entails", "contradiction":"contradiction", "cover":"alternation", "alternation":"cover", "independence":"independence"}
emptystring_signature = {"equivalence":"equivalence", "entails":"entails", "reverse entails":"reverse entails", "contradiction":"contradiction", "cover":"cover", "alternation":"alternation", "independence":"independence"}
compose_contradiction_signature = {r:relation_composition[(r, "contradiction")] for r in relations }
#creates the signatures for determiners
determiner_signatures = dict()
symmetric_relation = {"equivalence":"equivalence", "entails":"reverse entails", "reverse entails":"entails", "contradiction":"contradiction", "cover":"cover", "alternation":"alternation", "independence":"independence"}
determiner_signatures[("some","some")] =(
{"equivalence":"equivalence", "entails":"entails", "reverse entails":"reverse entails", "independence":"independence"},
{"equivalence":"equivalence", "entails":"entails", "reverse entails":"reverse entails", "contradiction":"cover", "cover":"cover", "alternation":"independence", "independence":"independence"}
)
determiner_signatures[("every","every")] =(
{"equivalence":"equivalence", "entails":"reverse entails", "reverse entails":"entails", "independence":"independence"},
{"equivalence":"equivalence", "entails":"entails", "reverse entails":"reverse entails", "contradiction":"alternation", "cover":"independence", "alternation":"alternation", "independence":"independence"}
)
for key in determiner_signatures:
    signature1, signature2 = determiner_signatures[key]
    new_signature = dict()
    for key1 in signature1:
        for key2 in signature2:
            new_signature[(key1, key2)] = strong_composition(signature1, signature2, key1, key2)
    determiner_signatures[key] = new_signature

new_signature = dict()
for relation1 in ["equivalence", "entails", "reverse entails", "independence"]:
    for relation2 in relations:
        if (relation2 == "equivalence" or relation2 == "reverse entails") and relation1 != "independence":
            new_signature[(relation1, relation2)] = "reverse entails"
        else:
            new_signature[(relation1, relation2)] = "independence"
determiner_signatures[("some","every")] = new_signature
determiner_signatures[("some","every")][("entails", "contradiction")] = "alternation"
determiner_signatures[("some","every")][("entails", "alternation")] = "alternation"
determiner_signatures[("some","every")][("equivalence", "alternation")] = "alternation"
determiner_signatures[("some","every")][("equivalence", "contradiction")] = "contradiction"
determiner_signatures[("some","every")][("equivalence", "cover")] = "cover"
determiner_signatures[("some","every")][("reverse entails", "cover")] = "cover"
determiner_signatures[("some","every")][("reverse entails", "contradiction")] = "cover"

new_signature = dict()
for key in determiner_signatures[("some", "every")]:
    new_signature[(symmetric_relation[key[0]], symmetric_relation[key[1]])] = symmetric_relation[determiner_signatures["some", "every"][key]]
determiner_signatures[("every", "some")] = new_signature

#creates the signature for or
and_signature = dict()
for relation1 in relations:
    for relation2 in relations2:
        if relation2 in ["contradiction", "alternation"] or relation1 in ["contradiction", "alternation"]:
            and_signature[(relation1,relation2)] = "alternation"
        else:
            and_signature[(relation1,relation2)] = "independence"
and_signature[("equivalence", "equivalence")] = "equivalence"
and_signature[("equivalence", "entails")] = "entails"
and_signature[("equivalence", "reverse entails")] = "reverse entails"
and_signature[("entails", "equivalence")] = "entails"
and_signature[("entails", "entails")] = "entails"
and_signature[("reverse entails", "equivalence")] = "reverse entails"
and_signature[("reverse entails", "reverse entails")] = "reverse entails"

or_signature = dict()
for relation in relations:
    for relation2 in relations2:
        or_signature[(relation, relation2)] = negation_signature[and_signature[(negation_signature[relation], negation_signature[relation2])]]

if_signature = dict()
for relation in relations:
    for relation2 in relations2:
        if_signature[(relation, relation2)] = or_signature[(negation_signature[relation], relation2)]

def compose_signatures(f,g):
    #takes two signatures and returns a signature
    #that is the result of applying the first and then the second
    h = dict()
    for r in f:
        h[r] = g[f[r]]
    return h

def standard_lexical_merge(x,y):
    #merges nouns, adjective, verbs, or adverbs
    if  x == y:
        return "equivalence"
    if x == "":
        return "reverse entails"
    if y == "":
        return "entails"
    return "independence"


def determiner_merge(determiner1,determiner2):
    #merges determiners
    return determiner_signatures[(determiner1,determiner2)]

def negation_merge(negation1, negation2):
    #merges negation
    relations = ["equivalence", "entails", "reverse entails", "contradiction", "cover", "alternation", "independence"]
    if negation1 == negation2 and not negation2:
        return emptystring_signature
    if negation1 == negation2 and negation2 :
        return negation_signature
    if not negation1:
        return compose_contradiction_signature
    if negation1:
        return compose_signatures(negation_signature, compose_contradiction_signature)

def standard_phrase(relation1, relation2):
    #merges a noun relation with an adjective relation
    #or a verb relation with an adverb relation
    if relation2 == "equivalence":
        return relation1
    return "independence"

def determiner_phrase(signature, relation1, relation2):
    #applies a determiner signature to two relation arguments
    return signature[(relation1,relation2)]

def negation_phrase(negation_signature, relation):
    #applies a negation signature to a relation argument
    return negation_signature[relation]

def conjunction_phrase(conjunction_signature, relation1, relation2):
    #applies a conjunction signature to two relation arguments
    return conjunction_signature[(relation1, relation2)]

def get_label(relation):
    #converts MacCartney's relations to 3 class NLI labels
    if relation in ["cover", "independence", "reverse entails"]:
        return "permits"
    if relation in ["entails", "equivalence"]:
        return "entails"
    if relation in ["alternation", "contradiction"]:
        return "contradicts"

def compute_simple_relation(premise, hypothesis):
    #computes the relation between a premise and hypothesis simple sentence
    #leaves
    subject_negation_signature = negation_merge(premise.subject_negation, hypothesis.subject_negation)
    subject_determiner_signature = determiner_merge(premise.natlog_subject_determiner, hypothesis.natlog_subject_determiner)
    subject_noun_relation = standard_lexical_merge(premise.subject_noun,hypothesis.subject_noun)
    subject_adjective_relation = standard_lexical_merge(premise.subject_adjective,hypothesis.subject_adjective)
    verb_negation_signature = negation_merge(premise.verb_negation, hypothesis.verb_negation)
    verb_relation = standard_lexical_merge(premise.verb,hypothesis.verb)
    adverb_relation = standard_lexical_merge(premise.adverb,hypothesis.adverb)
    object_negation_signature = negation_merge(premise.object_negation, hypothesis.object_negation)
    object_determiner_signature = determiner_merge(premise.natlog_object_determiner, hypothesis.natlog_object_determiner)
    object_noun_relation = standard_lexical_merge(premise.object_noun,hypothesis.object_noun)
    object_adjective_relation = standard_lexical_merge(premise.object_adjective,hypothesis.object_adjective)

    #the nodes of the tree
    VP_relation = standard_phrase(adverb_relation, verb_relation)
    object_NP_relation = standard_phrase(object_adjective_relation, object_noun_relation)
    subject_NP_relation = standard_phrase(subject_adjective_relation, subject_noun_relation)
    object_DP_relation = determiner_phrase(object_determiner_signature, object_NP_relation, VP_relation)
    object_negDP_relation = negation_phrase(object_negation_signature, object_DP_relation)
    negverb_relation = negation_phrase(verb_negation_signature, object_negDP_relation)
    subject_DP_relation = determiner_phrase(subject_determiner_signature, subject_NP_relation, negverb_relation)
    subject_NegDP_relation = negation_phrase(subject_negation_signature, subject_DP_relation)
    return subject_NegDP_relation

def conjunction_to_negation(conjunction):
    if conjunction == "or":
        return False,False,False
    if conjunction == "and":
        return True,True,True
    if conjunction == "then":
        return True,False,False

def compute_boolean_relation(premise_sentence1, premise_conjunction,premise_sentence2, hypothesis_sentence1, hypothesis_conjunction,hypothesis_sentence2):
    #computes the relation between a premise and hypothesis compound sentence
    premise_sentence1_negation, premise_conjunction_negation, premise_sentence2_negation= conjunction_to_negation(premise_conjunction)
    hypothesis_sentence1_negation, hypothesis_conjunction_negation, hypothesis_sentence2_negation= conjunction_to_negation(hypothesis_conjunction)
    sentence1_negation_signature = negation_merge(premise_sentence1_negation,hypothesis_sentence1_negation)
    sentence1_relation = compute_simple_relation(premise_sentence1, hypothesis_sentence1)
    sentence2_negation_signature = negation_merge(premise_sentence2_negation,hypothesis_sentence2_negation)
    sentence2_relation = compute_simple_relation(premise_sentence2, hypothesis_sentence2)
    sentence1_negation_relation = negation_phrase(sentence1_negation_signature, sentence1_relation)
    sentence2_negation_relation = negation_phrase(sentence2_negation_signature, sentence2_relation)
    conjunction_signature = or_signature
    conjunction_relation = conjunction_phrase(conjunction_signature, sentence1_negation_relation, sentence2_negation_relation)
    conjunction_negation_signature = negation_merge(premise_conjunction_negation, hypothesis_conjunction_negation)
    conjunction_negation_relation = negation_phrase(conjunction_negation_signature, conjunction_relation)
    return conjunction_negation_relation

def compute_boolean_relation_test(sentence1_relation,sentence2_relation, premise_conjunction,hypothesis_conjunction):
    #computes the relation between a premise and hypothesis compound sentence
    premise_sentence1_negation, premise_conjunction_negation, premise_sentence2_negation= conjunction_to_negation(premise_conjunction)
    hypothesis_sentence1_negation, hypothesis_conjunction_negation, hypothesis_sentence2_negation= conjunction_to_negation(hypothesis_conjunction)
    sentence1_negation_signature = negation_merge(premise_sentence1_negation,hypothesis_sentence1_negation)
    sentence2_negation_signature = negation_merge(premise_sentence2_negation,hypothesis_sentence2_negation)
    sentence1_negation_relation = negation_phrase(sentence1_negation_signature, sentence1_relation)
    sentence2_negation_relation = negation_phrase(sentence2_negation_signature, sentence2_relation)
    conjunction_signature = or_signature
    conjunction_relation = conjunction_phrase(conjunction_signature, sentence1_negation_relation, sentence2_negation_relation)
    conjunction_negation_signature = negation_merge(premise_conjunction_negation, hypothesis_conjunction_negation)
    conjunction_negation_relation = negation_phrase(conjunction_negation_signature, conjunction_relation)
    return conjunction_negation_relation

def basemod(base, mod, relation):
    if relation == "equivalence":
        return "(" + base + "*" + mod + "+" + base + ")"
    if relation == "entails":
        return "(" +base + "*" + mod + ")"
    if relation == "reverse entails":
        return "(" +base + "*" + mod + ")"
    else:
        return "(" +base + "*" + base + "*" + "(" + "1 + " + mod + ")" + "*" + "(" + "1 + " + mod + ")" + "- 3*"+base + "*" + mod + "-" + base +  ")"

def test_simple():
    placerelations = ["equivalence", "entails", "reverse entails","alternation", "contradiction", "cover",  "independence"]
    conjs = ["or", "and", "then"]
    badbools = []
    for r in relations:
        for r2 in relations2:
            for c1 in ["or", "and", "then"]:
                for c2 in ["or", "and", "then"]:
                    if r == "independence" and get_label(compute_boolean_relation_test(r, r2,c1,c2)) == "permits" and (get_label(compute_boolean_relation_test("entails", r2,c1,c2)) != "permits" or get_label(compute_boolean_relation_test("alternation", r2,c1,c2)) != "permits" or get_label(compute_boolean_relation_test("reverse entails", r2,c1,c2)) != "permits"):
                        badbools.append((conjs.index(c1),conjs.index(c2),placerelations.index(r),placerelations.index(r2)))
                    if r2 == "independence" and get_label(compute_boolean_relation_test(r, r2,c1,c2)) == "permits" and (get_label(compute_boolean_relation_test(r,"entails", c1,c2)) != "permits" or get_label(compute_boolean_relation_test(r,"alternation", c1,c2)) != "permits" or get_label(compute_boolean_relation_test(r,"reverse entails", c1,c2)) != "permits"):
                        badbools.append((conjs.index(c1),conjs.index(c2),placerelations.index(r),placerelations.index(r2)))
    print(badbools)
    for x in badbools:
        print(x)



    x = {"permits":dict(), "contradicts":dict(), "entails":dict()}
    for k in x:
        for VP_relation in ["equivalence", "entails", "reverse entails", "independence"]:
            for object_NP_relation in ["equivalence", "entails", "reverse entails", "independence"]:
                for subject_NP_relation in ["equivalence", "entails", "reverse entails", "independence"]:
                    x[k][(VP_relation, object_NP_relation, subject_NP_relation)] = 0
    for VP_relation in ["equivalence", "entails", "reverse entails", "independence"]:
        for object_NP_relation in ["equivalence", "entails", "reverse entails", "independence"]:
            for subject_NP_relation in ["equivalence", "entails", "reverse entails", "independence"]:
                for subject_negation_signature in [negation_merge(x, y) for x in [True, False] for y in [True, False]]:
                    for object_negation_signature in [negation_merge(x, y) for x in [True, False] for y in [True, False]]:
                        for verb_negation_signature in [negation_merge(x, y) for x in [True, False] for y in [True, False]]:
                            for subject_determiner_signature in [determiner_merge(x, y) for x in ["every", "some"] for y in ["every", "some"]]:
                                for object_determiner_signature in [determiner_merge(x, y) for x in ["every", "some"] for y in ["every", "some"]]:
                                    object_DP_relation = determiner_phrase(object_determiner_signature, object_NP_relation, VP_relation)
                                    object_negDP_relation = negation_phrase(object_negation_signature, object_DP_relation)
                                    negverb_relation = negation_phrase(verb_negation_signature, object_negDP_relation)
                                    subject_DP_relation = determiner_phrase(subject_determiner_signature, subject_NP_relation, negverb_relation)
                                    subject_NegDP_relation = negation_phrase(subject_negation_signature, subject_DP_relation)
                                    x[get_label(subject_NegDP_relation)][(VP_relation, object_NP_relation, subject_NP_relation)] +=1
    count = 0
    count2 = 0
    for k in x["permits"]:
        if k[0] != "independence" and k[1] != "independence" and k[2] != "independence":
            count += x["permits"][k]
        count2 += x["permits"][k]
    print(count,count2,count/count2)
    expression = ""
    for k in x["entails"]:
        if x["entails"][k] != 0:
            expression += str(x["entails"][k]) + "*" + basemod("v", "r", k[0]) + "*" + basemod("o", "b", k[1]) +"*" + basemod("s", "a", k[2]) + "+"
    print(expression, "\n\n")
    expression = ""
    for k in x["contradicts"]:
        if x["contradicts"][k] != 0:
            expression += str(x["contradicts"][k]) + "*" + basemod("v", "r", k[0]) + "*" + basemod("o", "b", k[1]) +"*" + basemod("s", "a", k[2]) + "+"
    print(expression, "\n\n")
    expression = ""
    for k in x["permits"]:
        if x["permits"][k] != 0:
            expression += str(x["permits"][k]) + "*" + basemod("v", "r", k[0]) + "*" + basemod("o", "b", k[1]) +"*" + basemod("s", "a", k[2]) + "+"
    print(expression, "\n\n")
    expression = ""
    for k in x["entails"]:
        if x["entails"][k] != 0:
            expression += str(x["entails"][k]) + "*" + basemod("50", "50", k[0]) + "*" + basemod("50", "50", k[1]) +"*" + basemod("50", "50", k[2]) + "+"
    print(expression, "\n\n")
