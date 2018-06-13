from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

# overall instructions & baseline instructions
class Instructions(Page):
    pass

# wait page before baseline task starts
class BaselineWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass

# baseline task
class Baseline(Page):
    pass

# baseline results
class ResultsBL(Page):
    pass


page_sequence = [
    Instructions,
    BaselineWaitPage,
    Baseline,
    ResultsBL
]