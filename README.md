#To begin
    clone this repo and cd to it.
    $ pip install -r requirements_base.txt
    $ otree devserver/resetdb...

#Notes:
    The logical aspects all work.
    I do not have an MTurk account, so I cannot test this with the MTurk interface.
    The MTurk settings have been inserted, but a description of the experiment needs to be added in
    settings.py

    I'm not sure what you want for dealing with inattentiveness/dropouts. The biggest issue is that
    there is no way to 'eject' a participant once they start playing the game. They can close the
    web page, but otree doesn't know the difference between that and them simply doing nothing.
    If they open the web page again, it will resume where they left off.

    So if a group is already formed and someone stops playing, there is no way
    to add a new player to that group. That means if some people have finished the baseline task
    and are in a wait page waiting for the rest of the 12, 
    and one of the people in that wait page exits chrome,
    everyone else is stuck. This is unfortunate but otree's group_players_by_arrival, which is how
    I group the first 12 players to finish the baseline together, adds a player to the group when
    they arrive at the wait page, not when they leave it.

    Instead of 'ejecting' players, it is possible to make them see a specific end of experiment page
    that has no next button. To cause this: if you want a timer that appears on a wait page after a 
    certain amount of time, how much time should pass before players see it, and how long do they
    have to respond? 

    This doesn't really solve the problem described above since otree thinks
    they're still in the group and to my knowledge otree has no 'remove from group' feature.
    
    There is also and issue with custom bonuses on mechanical turk. I have not used and and am not
    sure how payment is done with mturk.

    https://otree.readthedocs.io/en/latest/mturk.html
    https://otree.readthedocs.io/en/latest/multiplayer/waitpages.html