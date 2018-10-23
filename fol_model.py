import json
from nltk.sem.logic import *
from nltk.inference import *
from nltk import Prover9
from joblib import Parallel, delayed
from data_util import sentence

prover = Prover9()
prover.config_prover9(r"C:\Program Files (x86)\Prover9-Mace4\bin-win32")

def get_label(premise, hypothesis):
    #returns a label that is determined from using Prover9 on the first order logic representations
    premise_assumptions = Expression.fromstring(premise.assumptions)
    hypothesis_assumptions = Expression.fromstring(hypothesis.assumptions)
    premise_logical_form = Expression.fromstring(premise.logical_form)
    hypothesis_logical_form = Expression.fromstring(hypothesis.logical_form)
    negated_hypothesis_logical_form = Expression.fromstring("-" + "(" + hypothesis.logical_form + ")")
    if prover.prove(hypothesis_logical_form, [premise_logical_form, premise_assumptions,hypothesis_assumptions]):
        return "entails"
    if prover.prove(negated_hypothesis_logical_form, [premise_logical_form, premise_assumptions,hypothesis_assumptions]):
        return "contradicts"
    return "permits"

def build_simple_file(name):
    #This function builds a dictionary with encoded simple sentence NLI inputs
    #as keys and the correct label as values and saves it with filename name
    subject_noun = "man"
    subject_adjective1 = "tall"
    subject_adjective2 = "happy"
    adverb1 = "happily"
    adverb2 = "crazily"
    verb = ["eats", "eaten", "eat"]
    object_noun = "rock"
    object_adjective1 = "big"
    object_adjective2 = "rough"
    dets = ["every", "not every", "some", "no"]
    sentences = []
    encodings = []
    for pd1_index in range(4):
        pd1 = dets[pd1_index]
        for pd2_index in range(4):
            pd2 = dets[pd2_index]
            for hd1_index in range(4):
                hd1 = dets[hd1_index]
                for hd2_index in range(4):
                    hd2 = dets[hd2_index]
                    for subject_adjective_index in range(4):
                        if subject_adjective_index == 0:
                            padj1_word = subject_adjective1
                            hadj1_word = padj1_word
                        elif subject_adjective_index == 1:
                            padj1_word = ""
                            hadj1_word = subject_adjective2
                        elif subject_adjective_index == 2:
                            padj1_word = subject_adjective1
                            hadj1_word = ""
                        else:
                            padj1_word = subject_adjective1
                            hadj1_word = subject_adjective2
                        for object_adjective_index in range(4):
                            if object_adjective_index == 0:
                                padj2_word = object_adjective1
                                hadj2_word = padj2_word
                            elif object_adjective_index == 1:
                                padj2_word = ""
                                hadj2_word = object_adjective2
                            elif object_adjective_index == 2:
                                padj2_word = object_adjective1
                                hadj2_word = ""
                            else:
                                padj2_word = object_adjective1
                                hadj2_word = object_adjective2
                            for adverb_index in range(4):
                                if adverb_index == 0:
                                    padv_word = adverb1
                                    hadv_word = padv_word
                                elif adverb_index == 1:
                                    padv_word = ""
                                    hadv_word = adverb2
                                elif adverb_index == 2:
                                    padv_word = adverb1
                                    hadv_word = ""
                                else:
                                    padv_word = adverb1
                                    hadv_word = adverb2
                                for pnegation_value in range(2):
                                    for hnegation_value in range(2):
                                        sentences.append(
                                        [sentence(subject_noun, verb, object_noun, pnegation_value, padv_word, padj1_word, padj2_word, pd1,pd2),
                                        sentence(subject_noun, verb, object_noun, hnegation_value, hadv_word, hadj1_word, hadj2_word, hd1,hd2 )])
                                        encodings.append([pnegation_value, pd1_index,pd2_index, hnegation_value, hd1_index, hd2_index, subject_adjective_index, object_adjective_index, adverb_index])
    labels = Parallel(n_jobs=-1,backend="multiprocessing")(map(delayed(parallel_labels), sentences))
    result = dict()
    for i in range(len(labels)):
        final_encoding = encodings[i]
        result[json.dumps(final_encoding + [1,1,1])] = labels[i]
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    if i != 1 or j != 1 or k != 1:
                        result[json.dumps(final_encoding + [i,j,k])] = "permits"
    with open(name, "w") as f:
        f.write(json.dumps(result))


def parallel_labels(x):
    #a function to format getting labels for parallel processing
    label = get_label(x[0], x[1])
    return label

def build_boolean_file(name):
    #This function builds a dictionary with encoded compound sentence NLI inputs
    #as keys and the correct label as values and saves it with filename name
    logic_operators = ["|", "&", "->"]
    result = dict()
    for pindex in range(3):
        for hindex in range(3):
            for first_relation in range(7):
                for second_relation in range(7):
                    first_predicate = "A"
                    second_predicate = "B"
                    first_assumption = "(" + first_predicate+"(constant)"+logic_operators[pindex] + second_predicate+"(constant)" + ")"
                    first_predicate = "C"
                    second_predicate = "D"
                    conclusion = "(" + first_predicate+"(constant)"+logic_operators[hindex] + second_predicate+"(constant)" + ")"
                    assumptions = [Expression.fromstring(first_assumption)]
                    if first_relation == 1 or first_relation == 0:
                        assumptions.append(Expression.fromstring("A(constant)->C(constant)"))
                    if first_relation == 2 or first_relation == 0:
                        assumptions.append(Expression.fromstring("C(constant)->A(constant)"))
                    if first_relation == 3 or first_relation == 4:
                        assumptions.append(Expression.fromstring("-A(constant)|-C(constant)"))
                    if first_relation == 4 or first_relation == 5:
                        assumptions.append(Expression.fromstring("A(constant)|C(constant)"))
                    if second_relation == 1 or second_relation == 0:
                        assumptions.append(Expression.fromstring("B(constant)->D(constant)"))
                    if second_relation == 2 or second_relation == 0:
                        assumptions.append(Expression.fromstring("D(constant)->B(constant)"))
                    if second_relation == 3 or second_relation == 4:
                        assumptions.append(Expression.fromstring("-B(constant)|-D(constant)"))
                    if second_relation == 4 or second_relation == 5:
                        assumptions.append(Expression.fromstring("B(constant)|D(constant)"))
                    label = None
                    if prover.prove(Expression.fromstring(conclusion), assumptions):
                        label = "entails"
                    elif prover.prove(Expression.fromstring("-"+conclusion), assumptions):
                        label = "contradicts"
                    else:
                        label = "permits"
                    result[json.dumps((pindex, hindex, first_relation, second_relation))] = label
    with open(name,"w") as f:
        f.write(json.dumps(result))
