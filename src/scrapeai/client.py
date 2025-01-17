import asyncio

import re

from anthropic import AsyncAnthropic


MODEL = 'claude-3-5-sonnet-20240620'


def generate_prompt(name, document, question):
    return f'''Examine the following document named <name>{name}</name> and see if there is information to answer the question <question>{question}</question>. Print the title of the document (in <title> tags) if applicable, and a succinct but useful summary that answers the question or say there isn't enough information to answer the question (in <answer> tags).
Document:
<document>{document}</document>'''


async def get_completion(client, prompt):
    r = await client.messages.create(model=MODEL, max_tokens=1024, messages=[{'role': 'user', 'content': prompt}])
    return r.content[0].text


class PrettyAnswers:

    def __init__(self, raw):
        self.raw = raw

    def __repr__(self):
        return '\n'.join(
            [
                f'{i}. [{y[0]}] {y[1]}, {y[2]}'
                for i, y in enumerate(self.raw)
            ]
        )


class AnthropicClient:

    def __init__(self, api_key=None):
        if api_key is None:
            raise ValueError('`cred` is None. Specify your Anthropic API key.')
        self.api_key = api_key
        self.client = AsyncAnthropic(
            api_key=api_key
        )

    def get_prompt(self, name, document, question):
        return generate_prompt(name, document, question)

    async def async_ask(self, files, question):
        prompts = [
            self.get_prompt(f.path.name, f.content(), question)
            for f in files
        ]
        answers = await asyncio.gather(
            *[
                get_completion(self.client, prompt)
                for prompt in prompts
            ]
        )
        final_answers = []
        for i, result in enumerate(answers):
            title = re.search(r'<title>(.*?)</title>', result, re.DOTALL)
            if title:
                title = title.group(1)
            else:
                title = 'None'
            answer = re.search(r'<answer>(.*?)</answer>', result, re.DOTALL)
            if answer:
                answer = answer.group(1)
            else:
                answer = result
            final_answers.append((files[i].path.name, f'Title: {title}', f'Answer: {answer}'))
        return PrettyAnswers(final_answers)

    def ask(self, files, question):
        loop = asyncio.get_event_loop()
        answers = loop.run_until_complete(self.async_ask(files, question))
        return answers
