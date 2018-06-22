To begin:
=============
    clone this repo and cd into it.
    $ pip install -r requirements_base.txt
    $ otree devserver/resetdb...

Notes:
=============

    - I do not have time to finish the survey. 
    Question 1 is implemented, along with questions 6-12 (5-11 in
    the email, I understand why you duplicated #4 but for the purpose of returning form fields they
    need different names).

    2 and 3 need to change slightly because I don't think it's
    possible to send players back a page. You will need to write some JS that checks their answer and
    compares it to the correct answer, then selectively displays some text if they are incorrect.

    4 and 5 (4 and 4 in the email) will not be at the same place in the experiment as I think you
    assume, because I wrote it such that the firm is chosen before the instructions for game 1, 
    and the score display (which depends on the firm) is in the same page as the instructions for
    game 1.

    I fixed the grouping in game 1, so players are now randomly grouped at the beginning of game 1.

    The bots do not work in game 2 because I did not have them yield the survey pages. If you want
    to do that it won't be much work, see the otree docs and the existing code.



    - IDK if it is possible to do MTurk in kiosk mode, but players refreshing their webpages can
    have unpredictable results and at the very least I recommend telling them not to in the
    initial instructions.

    - I am leaving the instructions for you to edit as you see fit. Right now, they are empty. There
    are 3 instruction pages that must be edited: Instructions.html, Instructions1.html, and
    Instructions2.html.  

    - All configurable settings are in SESSION_CONFIGS in settings.py
    Configurable settings:
        - upper and lower bounds for the numbers in the arithmetic tasks, default [0, 25]
        - minimum number of players needed to advance to game 1, default 6
        - time limit (s) for arithmetic pages, default 120
        - option to use browser bots to test, default False

Overview:
=============
    This expeiment consists of 4 independent apps in sequence: baseline, waitpage, game1, game2.
    Each app has its own data and formfields. The only way to pass data between apps is with
    participant.vars. The only data that is passed between apps is:
        - score in baseline
        - problems attemtpted in baseline
        - score in game 1
        - problems attempted in game 1
        - rank in game 1
        - bonus in game 1
    These data are needed in the final results page, at the end of game 2. The initial instructions
    are at the beginning of baseline.

    Baseline, game 1, and game 2 all use a similar html page for the arithmetic task itself.
    
    In models.py for each app, a data structure is created, holding 500 doubles, each one holding
    a triple containing 3 word-numbers, and a single holding the sum of those numbers.
    ex: [(('one', 'two', 'three'), 6), (('four', 'five', 'six'), 15) ...]
    
    That data structure is the same for all players in that app (baseline, game 1, or game 2).
   
    That data structure gets referenced in pages.py and passed to the html template.
    Each app is 1 round, so players answer as many questions as they can on a single page that
    automatically submits after 2 minutes (or whatever you set it to in settings.SESSION_CONFIGS).

    This means that when a player presses the submit button in one of the tasks, they are not
    submitting the page or any forms. Pressing the submit button calls a function that compares
    their answer to the correct answer, and selectively increments a correct counter and
    and attempted counter. These counters automatically submit when the page time runs out.

## Experiment progression (each bullet represents a page players will see):
    baseline:
    - Initial/baseline instructions
        1 page with both the initial instrucitons for the whole experiment, and the instructions
        specific to the baseline.
        60 second timer until page submits automatically.
    - Baseline task
        Lasts for 120 seconds (or time_limit, configurable in settings.py)
    - Baseline results
        60 second timer until page submits automatically.

    waitpage
    - Wait page while the first 6 (or min_players, configurable in settings.py) players finish the 
      baseline task
        Once the first 6 players arrive at the wait page, they are grouped together, then 
        advance to game 1.
        After those 6 players leave the wait page, all subsequent players who finish the baseline
        task are redirected to a Too Late page that tells them the experiment is over.

    - Another wait page
        This page's only purpose is to set the toggle to prevent other players from continuing to
        game 1. Since all players arrive here after the previous wait page, this should be
        instantaneous.

    game1
    - Wait page before game 1
        Groups players into groups of 3 by order of arrival. Since all players arrive here after the
        previous wait page, this should be instantaneous. Note that this group is put together in
        order of arrival at the first wait page (that grouped the first 6
        players), so groups of 3 here are not randomly generated. 
        Furthermore, the IDs within these groups are determined the same serial way, to the first
        person to finish the baseline task will be player 1. 
        This is difficult to prevent because otree does weird things when you switch group sizes
        between apps and don't group by arrival time.
    - Choose firm
        Only player 1 will see this page, other players will skip it.
        The additional task has been implemented, so players have a 50% chance of seeing a simple
        radio choice, and a 50% chance of having to choose how much money they are willing to pay
        to get firm A. Note that they do not actually pay this amount if chosen.
    - Wait page while player 1 chooses the firm
    - Game 1 instructions
        This is where the outcome of firm choice is displayed, where players either
        see only their own or everyone in their group's baseline scores.
    - Game 1 arithmetic task
    - Game 1 results

    game2
    - Game 2 wait page
        Switches player's firms to match their reformed groups.
        IDs in group stay the same, but players 2 and 3 are randomly distributed between groups.
    - Game 2 instructions
        same as game 1 instructions
    - Game 2 arithmetic task
    - Game 2 Results
    - Overall Results

License
===============

Copyright 2018 Eli Pandolfo

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



