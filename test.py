import generate_data as gd
import fol_model as fol
import natural_logic_model as nlm
import data_util
import json
if __name__ == '__main__':
    data, _, _ = gd.process_data(1.0)
    if True:
        #fol.build_simple_file("simple_solutions")
        fol.build_boolean_file("boolean_solutions")
        with open("simple_solutions","r") as f:
            simple_solutions = json.loads(f.read())
        for encoding in simple_solutions:
            encoding = json.loads(encoding)
            premise, hypothesis = gd.encoding_to_example(data,encoding)
            if gd.example_to_encoding(premise,hypothesis) != encoding:
                print("We have a problem with the simple encoding")
            nlm_label = nlm.get_label(nlm.compute_simple_relation(premise, hypothesis))
            if simple_solutions[json.dumps(encoding)] != nlm_label:
                print("We have a problem with the simple file")
        print("simple file is good")
        with open("boolean_solutions","r") as f:
            boolean_solutions = json.loads(f.read())
        simple1 = [(data_util.parse_sentence(data, "some wizard eats some flute")[0],data_util.parse_sentence(data, "some wizard eats some flute")[0])]
        simple1.append((data_util.parse_sentence(data, "every wizard eats every flute")[0],data_util.parse_sentence(data, "some wizard eats some flute")[0]))
        simple1.append((data_util.parse_sentence(data, "some wizard eats some flute")[0],data_util.parse_sentence(data, "every wizard eats every flute")[0]))
        simple1.append((data_util.parse_sentence(data, "no wizard eats some flute")[0],data_util.parse_sentence(data, "some wizard eats every flute")[0]))
        simple1.append((data_util.parse_sentence(data, "no wizard eats some flute")[0],data_util.parse_sentence(data, "some wizard eats some flute")[0]))
        simple1.append((data_util.parse_sentence(data, "some wizard eats some flute")[0],data_util.parse_sentence(data, "no wizard eats every flute")[0]))
        simple1.append((data_util.parse_sentence(data, "no wizard eats some tree")[0],data_util.parse_sentence(data, "some wizard eats every flute")[0]))
        simple2 = [(data_util.parse_sentence(data, "some mailman eats some flute")[0],data_util.parse_sentence(data, "some mailman eats some flute")[0])]
        simple2.append((data_util.parse_sentence(data, "every mailman eats every flute")[0],data_util.parse_sentence(data, "some mailman eats some flute")[0]))
        simple2.append((data_util.parse_sentence(data, "some mailman eats some flute")[0],data_util.parse_sentence(data, "every mailman eats every flute")[0]))
        simple2.append((data_util.parse_sentence(data, "no mailman eats some flute")[0],data_util.parse_sentence(data, "some mailman eats every flute")[0]))
        simple2.append((data_util.parse_sentence(data, "no mailman eats some flute")[0],data_util.parse_sentence(data, "some mailman eats some flute")[0]))
        simple2.append((data_util.parse_sentence(data, "some mailman eats some flute")[0],data_util.parse_sentence(data, "no mailman eats every flute")[0]))
        simple2.append((data_util.parse_sentence(data, "no mailman eats some tree")[0],data_util.parse_sentence(data, "some mailman eats every flute")[0]))
        etemp = [[0,0,0,0,0,0,0]] * 7
        ctemp = [[0,0,0,0,0,0,0]] * 7
        ptemp = [[0,0,0,0,0,0,0]] * 7
        for encoding in boolean_solutions:
            encoding = json.loads(encoding)
            if boolean_solutions[json.dumps(encoding)] == "permits":
                ptemp[encoding[2]][encoding[3]] += 1
            if boolean_solutions[json.dumps(encoding)] == "entails":
                etemp[encoding[2]][encoding[3]] += 1
            if boolean_solutions[json.dumps(encoding)] == "contradicts":
                ctemp[encoding[2]][encoding[3]] += 1
            conjunctions = ["or", "and", "then"]
            premise_conjunction = conjunctions[encoding[0]]
            hypothesis_conjunction = conjunctions[encoding[1]]
            premise1, hypothesis1 = simple1[encoding[2]]
            premise2, hypothesis2 = simple2[encoding[3]]
            nlm_label = nlm.get_label(nlm.compute_boolean_relation(premise1, premise_conjunction, premise2, hypothesis1, hypothesis_conjunction, hypothesis2))
            if boolean_solutions[json.dumps(encoding)] != nlm_label:
                print(boolean_solutions[json.dumps(encoding)], nlm_label)
                print("We have a problem with the boolean file")
        print("boolean file is good")
        print(etemp)
        print(ctemp)
        print(ptemp)
    examples = gd.generate_balanced_data("simple_solutions", "boolean_solutions", 100, 100, data,simple_sampling = "level 2", boolean_sampling = "level 1")
    gd.save_data(examples, "test")
    examples = []
    with open("test", "r") as f:
        lines = f.readlines()
        for line in lines:
            examples.append(json.loads(line))
    for example in examples:
        premise = data_util.parse_sentence(data,example["sentence1"])
        hypothesis = data_util.parse_sentence(data,example["sentence2"])
        if len(premise) == 1:
            fol_label = fol.get_label(premise[0], hypothesis[0])
            nlm_label = nlm.get_label(nlm.compute_simple_relation(premise[0], hypothesis[0]))
            if example["gold_label"] != fol_label or fol_label != nlm_label:
                print("We have a problem with simple generation")
        else:
            premise1 = premise[0]
            premise_conjunction = premise[1]
            premise2 = premise[2]
            hypothesis1 = hypothesis[0]
            hypothesis_conjunction = hypothesis[1]
            hypothesis2 = hypothesis[2]
            nlm_label = nlm.get_label(nlm.compute_boolean_relation(premise1, premise_conjunction, premise2, hypothesis1, hypothesis_conjunction, hypothesis2))
            if example["gold_label"] != nlm_label:
                print("We have a problem with boolean generation")
    print("generation is good")
