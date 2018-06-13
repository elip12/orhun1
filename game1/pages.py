from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


# instructions for game 1
class Instructions1(Page):
    pass

# wait page before game 1
class Game1WaitPage(WaitPage):
    
    def after_all_players_arrive(self):
        pass

# game 1 task
class Game1(Page):
    pass

class Results1WaitPage(WaitPage):
    
    def after_all_players_arrive(self):
        pass

# game 1 results
class Results1(Page):
    pass


page_sequence = [
    Instructions1,
    Game1WaitPage,
    Game1,
    Results1WaitPage,
    Results1
]
