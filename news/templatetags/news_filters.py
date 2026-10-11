import re

from django import template

register = template.Library()

# Список нежелательных слов
FORBIDDEN_WORDS = ['плохо', 'скучно', 'плохой', 'ужас', 'ужасный']

# Длинные слова идут первыми: иначе «ужас» «съест» начало слова «ужасный»
_PATTERN = re.compile(
    '|'.join(re.escape(word) for word in sorted(FORBIDDEN_WORDS, key=len, reverse=True)),
    re.IGNORECASE,
)


def _mask(match):
    word = match.group(0)
    return word[0] + '*' * (len(word) - 1)


@register.filter
def censor(text):
    """Заменяет все буквы нежелательных слов, кроме первой, на «*»."""
    if not text:
        return text
    return _PATTERN.sub(_mask, str(text))