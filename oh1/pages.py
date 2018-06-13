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
    Instructions,
    BaselineWaitPage,
    Baseline,
    ResultsBL,
    Instructions1,
    Game1WaitPage,
    Game1,
    Results1WaitPage,
    Results1,
    Instructions2,
    Game2WaitPage,
    Game2,
    Results2WaitPage,
    Results2,
    Results
]