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

for sentence in doc.sents:
    tokens = [i for i in sentence if i.pos_ not in ["SPACE"]]
    root = sentence.root
    def create_tree():
        colors = {
            "NOUN": "yellow",
            "PROPN": "yellow",
            "ADJ": "green",
            "ADV": "green",
            "VERB": "blue",
            "PRON": "dark_orange",
        }
        tree = Tree(f"[bold {colors.get(root.pos_,"")}]{root.text}[/bold {colors.get(root.pos_,"")}]\t{root.lemma_}\t{root.pos_}/{root.tag_}")
        def add_branch(upstream, parent):
            for token in tokens:
                if token.head == parent and token != parent:

                    branch_text = f"[bold {colors.get(token.pos_,"")}]{token.text}[/bold {colors.get(token.pos_,"")}]\t{token.dep_}\t{token.pos_}/{token.tag_}"
                    branch = upstream.add(branch_text)
                    add_branch(branch, token)
        add_branch(tree, root)
        print(tree)
    create_tree()
    # print([i for i in sentence.noun_chunks])
    def classify_sentence():
        match root.pos_:
            case "NOUN"|"PROPN":
                print("Answer")
            case "VERB":
                if nsubj := next((i for i in tokens if i.dep_ in ["nsubj","nsubjpass"]), None):
                    if (punct := next((i for i in reversed(tokens) if i.dep_ in ["punct"]), None)) and punct.text == "?":
                        print("Question")
                    else:
                        print("Declaration")
                else:
                    print("Command")
            case "AUX":
                if (punct := next((i for i in reversed(tokens) if i.dep_ in ["punct"]), None)) and punct.text == "?":
                    print("Question")
                else:
                    print("Declaration")

    # if root.pos_ == "AUX":
    #     subj = next((i for i in tokens if i.dep_ == "nsubj"), None)
    #     if subj:
    #         subj_topic = Topic(subj.lemma_)
    #
    #         adj = next((i for i in tokens if i.dep_ == "acomp"), None)
    #         if adj:
    #             adj_topic = Topic(adj.lemma_)
    #             # adj_topic.mod.append()
    #             relations.append(Relation(subj_topic, adj_topic))
    # print([str(i) for i in relations])
