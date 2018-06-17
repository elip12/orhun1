from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Eli Pandolfo'

""" notes

The only reason this app exists is because players_per_group must remain constant within apps,
so we need a 12 players_per_group app then a 3 players_per_group app.
"""


class Constants(BaseConstants):
    name_in_url = 'waitpage'
    players_per_group = 12
    num_rounds = 1


class Subsession(BaseSubsession):
    
    def creating_session(self):
        self.session.vars['players_allowed'] = True


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass