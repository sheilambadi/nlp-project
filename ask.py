import spacy
import sys

from spacy.pipeline import Tagger


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

        # print(self.tokenize())
        self.analyze()

    def parse_file(self):
        """
        Analyze an article
        :return: list with file content
        """
        file_content = []

        f = open(self.text_file, "r")
        for line in f:
            # ignore empty lines
            if line.strip():
                file_content.append(line)

        return file_content

    def sentencize(self):
        """
        Segment file in to “sentences”
        :return: multidimensional list of sentences
        """

        sentence_list = []

        content = self.parse_file()

        # Construction via create_pipe
        sentencizer = self.nlp.create_pipe("sentencizer")
        self.nlp.add_pipe(sentencizer)

        for c in content:
            doc = self.nlp(c)
            sentences = list(doc.sents)
            sentence_list.append(sentences)

        return sentence_list

    def tokenize(self):
        """
        Tokenize each sentence into words
        "return: tokenized list of sentences
        """
        sentences = self.sentencize()
        tokenized_sentence = []

        # Create a Tokenizer with the default settings for English
        # including punctuation rules and exceptions
        tokenizer = self.nlp.Defaults.create_tokenizer(self.nlp)

        for paragraph in sentences:
            # convert paragraph to string for tokenizer to work
            paragraph = [str(p) for p in paragraph]
            for sentence in tokenizer.pipe(paragraph):
                tokens = list(sentence)
                tokenized_sentence.append(tokens)

        return tokenized_sentence

    def analyze(self):
        """
        Run a part-of-speech tagger on tokens
        :return: analyzed words
        """

        sentence_list = self.sentencize()
        analysis_list = []

        for paragraph in sentence_list:
            for sentence in paragraph:
                sentence = " ".join([str(s) for s in sentence])

                # store constituents of the sentence
                sent_list = []
                doc = self.nlp(sentence)

                # analyze wach word in token
                for token in doc:
                    analyzed = {
                        token.text: {
                            "pos": token.pos_,
                            "tag": token.tag_,
                            "dep_parser": token.dep_,
                        }
                    }
                    sent_list.append(analyzed)
            analysis_list.append(sent_list)

        print(analysis_list)
        return analysis_list


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
