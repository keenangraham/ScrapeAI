def generate_prompt(document, question):
    return f'''
    Examine the following document and see if there is information to answer the question {question}. If
    there is then print the title of the document, a hyphen, and a succinct but useful summary that answers the
    question. Otherwise print the title of the document, a hypen, and say that there isn't enough information to
    answer the question in the document. Don't say anything else.

    Document:
    {document}
    '''


class AnthropicClient:

    def __init__(self, cred=None):
        if cred is None:
            raise ValueError('`cred` is None. Specify your Anthropic API credentials.')
        self.cred = cred
        self.client = None

    def get_prompt(self, document, question):
        return generate_prompt(document, question)

    def ask(self, files, question):
        prompts = [
            self.get_prompt(f.content, question)
            for f in files
        ]
