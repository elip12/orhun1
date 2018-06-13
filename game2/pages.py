from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


# instructions for game 2
class Instructions2(Page):
    pass

# wait page for game 2
class Game2WaitPage(WaitPage):
    
    def after_all_players_arrive(self):
        pass

# game 2 task
class Game2(Page):
    pass

class Results2WaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass

# results for game 2
class Results2(Page):
    pass

# overall results
class Results(Page):
    pass


page_sequence = [
    Instructions2,
    Game2WaitPage,
    Game2,
    Results2WaitPage,
    Results2,
    Results
]
