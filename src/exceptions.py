
class NonoGramError(ValueError):
    ...


class NonoGramFlowControl(ValueError):
    ...


class NoSimilaritiesFound(NonoGramError):
    ...


class NoSpaceLeft(NonoGramError):
    ...


class InvalidLengths(NonoGramError):
    ...


class NotMatchingChars(NonoGramError):
    ...


class CannotSolve(NonoGramError):
    ...


class FullySolved(NonoGramFlowControl):
    ...
