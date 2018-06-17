from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random
import inflect

# wait page before game 1
class Game2WaitPage(WaitPage):
    
    def after_all_players_arrive(self):
        pass

# instructions for game 2
class Instructions2(Page):
    
    def vars_for_template(self):
        you = self.player.id_in_group
        opponent1 = self.group.get_player_by_id((you) % 3 + 1)
        opponent2 = self.group.get_player_by_id((you + 1) % 3 + 1)

        return {
            'firm': self.player.firm,
            'baseline': self.player.participant.vars['baseline_score'],
            'opponent1': opponent1.participant.vars['baseline_score'],
            'opponent2': opponent2.participant.vars['baseline_score']
        }

# game 1 task
class Game2(Page):
    form_model = 'player'
    form_fields = ['game2_score', 'attempted']

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
        self.player.participant.vars['game2_score'] = self.player.game2_score

class Results2WaitPage(WaitPage):
    
    def after_all_players_arrive(self):

        # in case 2 players have a tied score, chance decides which one gets $2
        # and which one gets $1
        i1 = random.randint(1,3)
        i2 = i1 % 3 + 1
        i3 = (i1 + 1) % 3 + 1

        p1 = self.group.get_player_by_id(i1)
        p2 = self.group.get_player_by_id(i2)
        p3 = self.group.get_player_by_id(i3)

        scores = sorted([p1, p2, p3], key=lambda x: x.game2_score, reverse=True)

        scores[0].payoff = 2
        scores[0].participant.vars['game2_rank'] = 1
        scores[0].participant.vars['game2_bonus'] = 2
        scores[1].payoff = 1
        scores[1].participant.vars['game2_rank'] = 2
        scores[1].participant.vars['game2_bonus'] = 1
        scores[2].payoff = 0
        scores[2].participant.vars['game2_rank'] = 3
        scores[2].participant.vars['game2_bonus'] = 0


# game 2 results
class Results2(Page):
    
    # variables that will be passed to the html and can be referenced from html or js
    def vars_for_template(self):
        return {
            'attempted': self.player.attempted,
            'correct': self.player.game2_score,

            # automoatically pluralizes the word 'problem' if necessary
            'problems': inflect.engine().plural('problem', self.player.attempted)
        }

# overall results
class Results(Page):

    # variables that will be passed to the html and can be referenced from html or js
    def vars_for_template(self):
        bl_attempted = self.player.participant.vars['baseline_attempted']
        bl_score = self.player.participant.vars['baseline_score']
        bl_problems = inflect.engine().plural('problem', bl_attempted)

        g1_attempted = self.player.participant.vars['game1_attempted']
        g1_score = self.player.participant.vars['game1_score']
        g1_problems = inflect.engine().plural('problem', g1_attempted)
        g1_rank = self.player.participant.vars['game1_rank']
        g1_bonus = self.player.participant.vars['game1_bonus']

        g2_attempted = self.player.attempted
        g2_score = self.player.game2_score
        g2_problems = inflect.engine().plural('problem', g2_attempted)
        g2_rank = self.player.participant.vars['game2_rank']
        g2_bonus = self.player.participant.vars['game2_bonus']

        return {
            'bl_attempted': bl_attempted,
            'bl_score': bl_score,
            'bl_problems': bl_problems,
            'g1_attempted': g1_attempted,
            'g1_score': g1_score,
            'g1_problems': g1_problems,
            'g1_rank': g1_rank,
            'g1_bonus': g1_bonus,
            'g2_attempted': g2_attempted,
            'g2_score': g2_score,
            'g2_problems': g2_problems,
            'g2_rank': g2_rank,
            'g2_bonus': g2_bonus
        }


page_sequence = [
    Game2WaitPage,
    Instructions2,
    Game2,
    Results2WaitPage,
    Results2,
    Results
]
