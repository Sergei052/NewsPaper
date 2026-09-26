from django import template

register = template.Library()

# Список нежелательных слов
FORBIDDEN_WORDS = ['плохо', 'скучно', 'плохой', 'ужас', 'ужасный']


@register.filter
def censor(text):
    if not text:
        return text

    result = text
    for word in FORBIDDEN_WORDS:
        replacement = word[0] + '*' * (len(word) - 1)

        result = replace_case_insensitive(result, word, replacement)

    return result


def replace_case_insensitive(text, old, new):
    import re
    pattern = re.compile(re.escape(old), re.IGNORECASE)

    def replacer(match):
        matched_text = match.group(0)
        if matched_text[0].isupper():
            return new[0].upper() + new[1:]
        return new

    return pattern.sub(replacer, text)