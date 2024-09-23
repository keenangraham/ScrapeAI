from anthropic import AsyncAnthropic


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

    def __init__(self, api_key=None):
        if api_key is None:
            raise ValueError('`cred` is None. Specify your Anthropic API credentials.')
        self.api_key = api_key
        self.client = AsyncAnthropic(
            api_key=api_key
        )

    def get_prompt(self, document, question):
        return generate_prompt(document, question)

    def ask(self, files, question):
        prompts = [
            self.get_prompt(f.content, question)
            for f in files
        ]

#loop = asyncio.get_event_loop()
#group1 = asyncio.gather(*[coro("group 1.{}".format(i)) for i in range(1, 6)])
# loop.run_until_complete(all_groups)
