from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random
import inflect

# wait page before game 1
class Game1WaitPage(WaitPage):
    
    def after_all_players_arrive(self):
        pass

# one player in each group chooses firm A or firm B
class ChooseFirm(Page):
    form_model = 'player'
    form_fields = ['firm']

    def is_displayed(self):
        return self.player.id_in_group == 1

    def before_next_page(self):
        for p in self.group.get_players():
            p.participant.vars['firm'] = self.player.firm
            p.firm = self.player.firm

# wait page for all 3 group members
class Instructions1WaitPage(WaitPage):
    pass

# instructions for game 1
class Instructions1(Page):
    
    def vars_for_template(self):
        you = self.player.id_in_group
        opponent1 = self.group.get_player_by_id((you) % 3 + 1)
        opponent2 = self.group.get_player_by_id((you + 1) % 3 + 1)

        return {
            'firm': self.player.participant.vars['firm'],
            'baseline': self.player.participant.vars['baseline_score'],
            'opponent1': opponent1.participant.vars['baseline_score'],
            'opponent2': opponent2.participant.vars['baseline_score']
        }

# game 1 task
class Game1(Page):
    form_model = 'player'
    form_fields = ['game1_score', 'attempted']

    # timer until page automatically submits itself
    timeout_seconds = 20
    
    # variables that will be passed to the html and can be referenced from html or js
    def vars_for_template(self):
        return {
            'problems': Constants.problems
        }

    # is called after the timer runs out and this page's forms are submitted
    # sets the participant.vars to transfer to next round
    def before_next_page(self):
        self.player.participant.vars['game1_attempted'] = self.player.attempted
        self.player.participant.vars['game1_score'] = self.player.game1_score

class Results1WaitPage(WaitPage):
    
    def after_all_players_arrive(self):

        # in case 2 players have a tied score, chance decides which one gets $2
        # and which one gets $1
        i1 = random.randint(1,3)
        i2 = i1 % 3 + 1
        i3 = (i1 + 1) % 3 + 1

        p1 = self.group.get_player_by_id(i1)
        p2 = self.group.get_player_by_id(i2)
        p3 = self.group.get_player_by_id(i3)

        scores = sorted([p1, p2, p3], key=lambda x: x.game1_score, reverse = True)

        scores[0].payoff = 2
        scores[0].participant.vars['game1_rank'] = 1
        scores[0].participant.vars['game1_bonus'] = 2
        scores[1].payoff = 1
        scores[1].participant.vars['game1_rank'] = 2
        scores[1].participant.vars['game1_bonus'] = 1
        scores[2].payoff = 0
        scores[2].participant.vars['game1_rank'] = 3
        scores[2].participant.vars['game1_bonus'] = 0


# game 1 results
class Results1(Page):
    
    # variables that will be passed to the html and can be referenced from html or js
    def vars_for_template(self):
        return {
            'attempted': self.player.attempted,
            'correct': self.player.game1_score,

            # automoatically pluralizes the word 'problem' if necessary
            'problems': inflect.engine().plural('problem', self.player.attempted)
        }


page_sequence = [
    Game1WaitPage,
    ChooseFirm,
    Instructions1WaitPage,
    Instructions1,
    Game1,
    Results1WaitPage,
    Results1
]
