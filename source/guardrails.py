INJECTION_PATTERNS = [

    "ignore previous instructions",
    "ignore all previous instructions",
    "forget previous instructions",
    "forget the document",
    "ignore the document",
    "system prompt",
    "developer message",
    "reveal your instructions",
    "act as",
    "jailbreak",
    "bypass safety",
    "pretend to be"
]


def validate_input(query):

    query_lower = query.lower()

    for pattern in INJECTION_PATTERNS:

        if pattern in query_lower:

            return (
                False,
                "Prompt injection attempt detected. Please ask questions related to the uploaded document."
            )

    return (
        True,
        None
    )