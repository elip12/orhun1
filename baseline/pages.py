from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import inflect

# overall instructions & baseline instructions
class Instructions(Page):
    pass

# baseline task
class Baseline(Page):
    form_model = 'player'
    form_fields = ['baseline_score', 'attempted']

    # timer until page automatically submits itself
    timeout_seconds = 120
    
    # variables that will be passed to the html and can be referenced from html or js
    def vars_for_template(self):
        return {
            'problems': Constants.problems
        }

    # is called after the timer runs out and this page's forms are submitted
    # sets the participant.vars to transfer to next round
    def before_next_page(self):
        self.player.participant.vars['baseline_score'] = self.player.baseline_score

# baseline results
class ResultsBL(Page):
    
    # variables that will be passed to the html and can be referenced from html or js
    def vars_for_template(self):
        return {
            'attempted': self.player.attempted,
            'correct': self.player.baseline_score,

            # automoatically pluralizes the word 'problem' if necessary
            'problems': inflect.engine().plural('problem', self.player.baseline_score)
        }


# sequence in which pages are displayed
page_sequence = [
    Instructions,
    Baseline,
    ResultsBL
]