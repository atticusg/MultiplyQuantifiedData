## Multiply Quantified Natural Language Inference Data
We provide code to automatically generate NLI data. See the paper for details.

## How to Generate Data

Import the file generate_data.py and use the function create_corpus to make data. Then run make_subphrase_labels.py to generate labels for the semantic relation between each aligned subphrase. The data named "0gendata.\*" is the most difficult fair generalization task, and the higher the number in front the easier the task.

Here is a image describing the order of the labels for each example:

![image](labeltree.png)

## Important Information About This Data
The data generated from this program is not intended to contain sentences that are genuinely natural language. Instead, this data is intended to isolate the task of learning the first order logical structure that occurs in natural language.
Several steps were taken to intentionally make my examples less natural for that purpose.  

* Firstly, the lexical items in this data are not intended to correspond to English words. As such, neural models making use of distributed representations should use randomly initialized word vectors, not pretrained vectors like GloVe or BERT so that, from the model's perspective, the words are just arbitrary tokens. However, the examples generated will contain English words like "singer" instead of arbitrary strings like "noun_token1". This is to improve the readability of examples when one manual inspects examples during error analysis. The meanings of the English words is not taken into account when labels are assigned, they are treated as arbitrary tokens where any pair of distinct tokens have independent unrelated meanings. For instance, the example:

Premise: some antagonistic singer doesnot emptystring reddens no emptystring rat

Hypothesis: no antagonistic singer doesnot blindly reddens notevery red rat

could have just as easily been:

Premise: some adjective_token1 noun_token1 negation_token emptystring verb_token no emptystring noun_token2

Hypothesis: no adjective_token1 noun_token1 negation_token adverb_token1 verb_token1 notevery adjective_token2 noun_token2

* There is no morphological variation. For example, in the two sentences "Some man eats every pizza" and "Some man does not eat every pizza" the presence or absence of negation results in a different verb form for "eat". I only have one form per verb token.
* We collapse "not every" and "does not" into single tokens.
* We provide empty string tokens when adjective, adverbs, or negation are not present. This results in uniformly structured sentences of the same length.

These changes were all made to make this task simpler, so when a model fails on the task we can attribute this failure exclusively to being stressed with the task of learning first order logic. All that being said, it would certainly be interesting to revert some of these changes to see if the task becomes more difficult, however that is not in the scope of the question being asked here.
