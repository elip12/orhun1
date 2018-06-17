from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random
import inflect
from django.conf import settings

# wait page before game 1
class Game1WaitPage(WaitPage):
    group_by_arrival_time = True
    
    def after_all_players_arrive(self):
        pass

# one player in each group chooses firm A or firm B
class ChooseFirm(Page):
    form_model = 'player'
    form_fields = ['firm', 'time_ChooseFirm']

    timeout_seconds = 60
    timeout_submission = {'firm': 'B'}

    def is_displayed(self):
        return self.player.id_in_group == 1

    def vars_for_template(self):
        return {'choice': 1 if random.random() >= .5 else 2}

    def before_next_page(self):
        for p in self.group.get_players():
            p.participant.vars['firm'] = self.player.firm
            p.firm = self.player.firm

# wait page for all 3 group members
class Instructions1WaitPage(WaitPage):
    pass

# instructions for game 1
class Instructions1(Page):
    form_model = 'player'
    form_fields = ['time_Instructions1']
    timeout_seconds = 60
    
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
    form_fields = ['game1_score', 'attempted', 'time_Game1']

    # timer until page automatically submits itself
    timeout_seconds = settings.SESSION_CONFIGS[0]['time_limit']
    
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

        # in case 2 players have a tied score, chance decides how bonuses are distributed
        p1 = self.group.get_player_by_id(1)
        p2 = self.group.get_player_by_id(2)
        p3 = self.group.get_player_by_id(3)

        # sorted() is guaranteed to be stable, so the list is shuffled first to ensure randomness
        players = sorted(random.sample([p1, p2, p3], k=3), key=lambda x: x.game1_score, reverse = True)

        for i in range(3):
            if players[i].game1_score == 0:
                players[i].game1_rank = 3
                players[i].participant.vars['game1_rank'] = 3
                players[i].game1_bonus = 0
                players[i].participant.vars['game1_bonus'] = 0
            else:
                players[i].game1_rank = i + 1
                players[i].participant.vars['game1_rank'] = i + 1
                players[i].game1_bonus = 2 - i
                players[i].participant.vars['game1_bonus'] = 2 - i
                players[i].payoff = c(2 - i)

# game 1 results
class Results1(Page):
    form_model = 'player'
    form_fields = ['time_Results1']
    timeout_seconds = 60
    
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
