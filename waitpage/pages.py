from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

# the first 12 players that arrive at this page will be grouped together, then a toggle will be
# flipped that prevents others from continuing

class FirstWaitPage(WaitPage):
    group_by_arrival_time = True
    body_text = 'When 12 players finish the baseline task, you will continue.'

    def is_displayed(self):
        return self.session.vars['players_allowed']


class TooLate(Page):
    
    def is_displayed(self):
        return not self.session.vars['players_allowed']

# This will be processed instantly and is only needed to flip the toggle after TooLate's 
# is_displayed already executes
class SecondWaitPage(WaitPage):

     def after_all_players_arrive(self):
        self.session.vars['players_allowed'] = False



page_sequence = [
    FirstWaitPage,
    TooLate,
    SecondWaitPage
]
