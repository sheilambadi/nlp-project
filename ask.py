import spacy
import sys


class Ask:
    """
    Class that generates questions from articles
    """

    def __init__(self, text_file, nquestions):
        """
        Initialize class
        """
        self.text_file = text_file
        self.nquestions = nquestions

        # Load English tokenizer, tagger, parser, NER and word vectors
        self.nlp = spacy.load("en_core_web_sm")

        content = self.parse_file()
        print(content)

    def parse_file(self):
        """
        Analyze an article
        :return: list with file content
        """
        file_content = []

        f = open(self.text_file, "r")
        for line in f:
            file_content.append(line)

        return file_content


if __name__ == "__main__":
    # Ensure exactly two arguments
    if len(sys.argv) != 3:
        print("Usage: python3 ask.py article.txt nquestions")
        sys.exit(1)

    article = sys.argv[1]
    nquestions = sys.argv[2]

    # Check input file type
    if not article.endswith(".txt"):
        print("Error: article must be .txt files")
        sys.exit(1)

    ask = Ask(article, nquestions)

"""
# Process whole documents
text = (
    "When Sebastian Thrun started working on self-driving cars at "
    "Google in 2007, few people outside of the company took him "
    "seriously. “I can tell you very senior CEOs of major American "
    "car companies would shake my hand and turn away because I wasn’t "
    "worth talking to,” said Thrun, in an interview with Recode earlier "
    "this week."
)
doc = nlp(text)

# Analyze syntax
print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

# Find named entities, phrases and concepts
for entity in doc.ents:
    print(entity.text, entity.label_)
"""
