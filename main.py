import spacy
from rich import print
from rich.tree import Tree
import re
nlp = spacy.load("en_core_web_sm")

text = """
A vacuole is a membrane-bound organelle which is present in plant and fungal cells and some protist, animal, and bacterial cells.[1][2] Vacuoles are essentially enclosed compartments which are filled with water containing inorganic and organic molecules including enzymes in solution, though in certain cases they may contain solids which have been engulfed. Vacuoles are formed by the fusion of multiple membrane vesicles and are effectively just larger forms of these.[3] The organelle has no basic shape or size; its structure varies according to the requirements of the cell.
"""
text = re.sub(r"\[\d+]", '', text) # for wikipedia
doc = nlp(text)
sentences = doc.sents
for sentence in sentences:
    tokens = [i for i in sentence if i.pos_ not in ["SPACE","PUNCT"]]
    roots = [i for i in sentence if i.dep_ == "ROOT"]
    for root in roots:
        tree = Tree(f"{root.text}\t{root.lemma_}")

        def add_branch(upstream, parent):
            for token in tokens:
                if token.head == parent and token != parent:
                    branch_text = f"{token.text}\t{token.dep_}\t{token.pos_}"
                    branch = upstream.add(branch_text)

                    add_branch(branch, token)
        add_branch(tree, root)
        print(tree)
