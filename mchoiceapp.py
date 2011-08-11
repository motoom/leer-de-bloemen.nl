# -*- coding: utf-8 -*-

# Software by Michiel Overtoom, motoom@xs4all.nl

# Ideas:
# - Extra flowers (madelief, distel, etc...)
# - English version / internationalisation.
# - online highscore list, enter your name when you get a high score.
# - show high score ranking.
# - feedback form when complete: which were the flowers you had most problems with?.
# - meticulous logging (or analysis of logs afterwards) so we can see how people play the quiz.
# - decorator om state automatisch te persisteren van/naar session object?

# TODO: Engelse namen+weetjes van de bestaande voorbeeldbloemen.
# Als moeilijk vindbaar is in NL/EN Wikipedia -> Overslaan
# Als geen goeie bloem-achtige plant is -> Overslaan
# Alleen CC-BY-SA en PD licensie typen gebruiken.

import sys
import cherrypy
from cherrypy import expose, engine
import random
import time
import ovotemplate
import itembankdb

langcode = 'nl'

threshold = 2 # (3) The number of times the user has to answer an item correctly in a row before it's considered a known item. (suggestion: 3)
tolearnsize = 7 # (10) Number of items currently being learned
lowatermark = 5 # (5) When the learning has shrunken to 'lowatermark' or less items, refill it from the items to learn.
alternatives = 4 # (4) Nr. of alternatives to show at each multiple-choice question.

def clamp(value, lower, upper):
    if value < lower: return lower
    if value > upper: return upper
    return value


class Item(object):
    def __repr__(self):
        return "%s: %s (%d correct in a row, %d correct total, %d incorrect total)" % (self.prompt, self.answer, self.correctrow, self.correct, self.incorrect)


class Mchoice(object):
    def __init__(self):
        self.tem_site = ovotemplate.Ovotemplate(unicode(open("site.tpl").read(), "utf-8"))
        # Check whether itembank contains non-ascii characters.
        for _, itembank, _, _ in itembankdb.itembanks:
            for _, _, answer, hint, attribution, license in itembank:
                answer.encode("ascii")
                hint.encode("ascii")
                attribution.encode("ascii")
                if license not in ("cc", "pd"): raise Exception("%s: license type must be 'cc' or 'pd'" % answer)

    def populatesession(self, difficulty=0):
        itembankname, itembank, _, _ = itembankdb.itembanks[difficulty]
        tolearn = list(itembank) # Pool of items still to learn.
        learned = []  # Questions which have been answered 'threshold' times more correct than incorrect
        learning = [] # Items currently being learned
        tickets = set() # Submit tickets seen (to prevent reloads from messing up the game)
        random.shuffle(tolearn)
        options = key = rightone = None
        done = False
        cherrypy.session["items"] = difficulty, learning, learned, tolearn, options, key, rightone, done, tickets

    def addtolearn(self, tolearn, tolearnsize, learning):
        while len(learning) < tolearnsize and tolearn:
            item = Item()
            item.prompt, item.pronoun, item.answer, item.hint, item.attribution, item.license = tolearn.pop()
            item.correctrow = item.correct = item.incorrect = 0
            learning.append(item)

    def generateticket(self):
        return "%f" % time.time()

    @expose
    def reset(self, *args, **kwargs):
        difficulty = int(kwargs.get("difficulty", 0))
        self.populatesession(difficulty)
        raise cherrypy.InternalRedirect('/')

    def randomgood(self):
        return random.choice(("Goed!", "Ja!", "Inderdaad!", "Correct!"))

    def randomfout(self):
        return random.choice(("Nee", "Helaas", "Jammer", "Sorry"))

    @expose
    def index(self, *args, **kwargs):
        # Is there an answer specified on the URL? If so, what is it? (None, 0, 1, ... alternatives-1)
        answer = kwargs.get("a")
        if answer is not None:
            answer = clamp(int(answer), 0, alternatives-1)

        # Session initialisation (if first visit) or retrieving current progress from session (on subsequent visits).
        visits = cherrypy.session.get("visits")
        if visits is None:
            # if answer is not None: print "Note: This website only works when you have cookies enabled in your webbrowser"
            visits = 1
            self.populatesession()
        visits = visits + 1
        cherrypy.session["visits"] = visits

        difficulty, learning, learned, tolearn, options, key, rightone, done, tickets = cherrypy.session["items"]

        message = ""
        wascorrect = False
        ticket = kwargs.get("t")
        if not ticket in tickets: # Protect against resubmits with same parameters.
            tickets.add(ticket)

            # If an answer is given, check if it's correct.
            if answer is None or key is None:
                if not len(learned):
                    # encouraging starting message only at start of game
                    message = itembankdb.itembanks[difficulty][2] # [2] is the item bank intro text
            elif answer == rightone:
                wascorrect = True
                key.correct += 1
                key.correctrow += 1
                correctanswer =  key.answer.lower()
                # TODO: 'good'-template
                message = "<h2 class=\"yes\">%s</h2><p><img class=\"blackshadow\" src=\"pictures/%s/%s\"></p><p>Dit is %s %s</p>" % (self.randomgood(), langcode, key.prompt, key.pronoun, correctanswer)
                # See if the key has been sufficiently correctly answered; if so, remove it from the items to learn, add it to the learned items, and add a fresh key to the items to learn.
                if key.correctrow >= threshold:
                    message += "<p>Je kent deze bloem nu</p>"
                    learned.append(key)
                    learning.remove(key)
                    if len(learning) <= lowatermark:
                        self.addtolearn(tolearn, tolearnsize, learning)
                    if not len(learning):
                        # The user knows all the itembank now.
                        # IDEA: Review the items just learned, sorted on the most errors made.
                        done = True
                        message = ""
            else:
                key.incorrect += 1
                key.correctrow = 0
                wronganswer = options[answer].answer.lower()
                correctanswer =  key.answer.lower()
                # TODO: 'wrong'-template
                message = "<h2 class=\"no\">%s</h2><p>Dat was geen %s.</p><p><img class=\"blackshadow\" src=\"pictures/%s/%s\"></p><p>Dit is %s %s</p>" % (self.randomfout(), wronganswer, langcode, key.prompt, key.pronoun, correctanswer)

        # Calculate progress
        completed = len(learned)
        itembankname, itembank, itembankintro, itembankdone = itembankdb.itembanks[difficulty]
        total = len(itembank)
        if total:
            percent = (100.0 * completed) / total
        else:
            percent = 0.0

        # Only show the progress bar if somewhere between 0 and 100%.
        progress = ""
        if percent > 0:
            if percent < 100:
                # TODO: Progress-template.
                progress = """
                    <div class="meter-wrap">
                        <div class="meter-value" style="background-color: #0a0; width: %.0f%%;">
                            <div class="meter-text">
                                %.0f%%&nbsp;voltooid
                            </div>
                        </div>
                    </div>
                    """ % (percent, percent)
            else:
                progress = "Gefeliciteerd, je kent ze allemaal!"

        # Show which flower character?
        feedbackmood=0
        if key and 0 < percent < 100:
            if wascorrect:
                feedbackmood = clamp(percent/20, 1,4)
            else:
                feedbackmood = clamp(key.correct - key.incorrect, -4, -1)

        if done:
            url = cherrypy.url("reset")
            urlagain = urlsame = urlnext = urlprev = None
            verdict = itembankdone
            if difficulty == 0: # First level.
                urlsame = cherrypy.url("reset", "difficulty=%d" % (difficulty,))
                urlnext = cherrypy.url("reset", "difficulty=%d" % (difficulty + 1,))
            elif difficulty == len(itembankdb.itembanks) - 1: # Last level.
                urlagain = cherrypy.url("reset", "difficulty=0")
                urlsame = cherrypy.url("reset", "difficulty=%d" % (difficulty))
            else: # Intermediate levels.
                urlprev = cherrypy.url("reset", "difficulty=%d" % (difficulty - 1,))
                urlsame = cherrypy.url("reset", "difficulty=%d" % (difficulty,))
                urlnext = cherrypy.url("reset", "difficulty=%d" % (difficulty + 1,))
            # TODO: 'done'-subtemplate.
            if urlnext:
                verdict += "<p class=\"next shadow rounded\"><a href=\"%s\">Ga verder <img src=\"img/arrow-forward.png\"></a></p>" % urlnext
                verdict += "<p>of...</p><p>"
            if urlagain: verdict += "<a href=\"%s\">Begin overnieuw</a><br>" % urlagain
            if urlsame: verdict += "<a href=\"%s\">Zelfde bloemen nog eens</a><br>" % urlsame
            if urlprev: verdict += "<a href=\"%s\">Makkelijkere bloemen</a><br>" % urlprev
            verdict += "</p>"

            answers = None
            key = Item()
            key.prompt = key.hint = key.attribution = key.license = ""
        else:
            verdict = None
            self.addtolearn(tolearn, tolearnsize, learning)

            # Choose 'alternative' random items (or less, if there aren't enough anymore) from the current learning set,
            # appoint one the key (the other will be used as distractors) and do a multiple choice question with those.
            options = random.sample(learning, min(alternatives, len(learning)))
            if len(options) < alternatives:
                options.extend(random.sample(learned, alternatives - len(learning)))
                random.shuffle(options)

            # Select one to be the key, preferably different than the previous
            # key (i.e., avoid asking the same question immediately again)
            safety = 0
            while True:
                safety += 1
                if safety > 200:
                    raise Exception("<p>BUG: Safety tripped! Consult log.</p>")
                rightone = random.randint(0, alternatives-1) # Appoint a random item.
                candidatekey = options[rightone]
                if candidatekey in learned: continue # If the item is already learned, select an other.
                if key is None or candidatekey.prompt != key.prompt: break # If the item chosen is different than the previous item, we're done.
                if len(learning) == 1: break # In the case the user learned all items except the last one, we're done too.

            # Found a usable key.
            key = options[rightone]
            question = key.prompt
            answers = []
            for nr, option in enumerate(options):
                url = cherrypy.url("", "a=%d&t=%s" % (nr, self.generateticket()))
                answers.append(dict(answer=option.answer, url=url))

        # Persist the whole state back into the session.
        cherrypy.session["items"] = difficulty, learning, learned, tolearn, options, key, rightone, done, tickets

        # Choose a 'narrator' picture with his mood (negative, positive, neutral)
        feedback = bool(progress) or bool(message)
        if not message and not done:
            # TODO: 'levelstart'-subtemplate
            message = "<p>Welke bloem is dit?</p><p>Maak je keuze door &eacute;&eacute;n van<br>de mogelijkheden te kiezen.</p>"
            feedbackmood = 0
            feedback = True
        feedbackpicture = "img/feedback%d.gif" % feedbackmood
        promptpicture = "pictures/%s/%s" % (langcode, key.prompt)
        
        # License
        license = ""
        if key.license == "pd":
            license = "<a target=\"_new\" href=\"http://wiki.creativecommons.org/Public_domain\">public domain</a>"
        elif key.license == "cc":
            license = "<a target=\"_new\" href=\"http://creativecommons.org/licenses/by-sa/3.0/deed.nl\">creative commons</a>"
        vars = dict(answers=answers, weetje=key.hint, attribution=key.attribution, license=license, langcode=langcode, prompt=promptpicture, feedback=feedback, feedbackpicture=feedbackpicture, progress=progress, message=message, verdict=verdict)
        return self.tem_site.render(vars)


    # A list of all flowers, grouped by item bank.
    @cherrypy.expose
    def showall(self):
        s = "<a href=\"/\">naar Quiz</a>"
        for itembankname, itembank, _, _ in itembankdb.itembanks:
            s += "<h2>%s</h2><table>\n" % itembankname
            for nr, (key, pronoun, prompt, hint, attribution, license) in enumerate(itembank):
                s += "<tr>"
                acell = "<img src=\"pictures/%s/%s\">" % (langcode, key)
                bcell = "<h3>%d. %s</h3><p>%s</p><p><small>%s (%s)</small></p>" % (nr, prompt, hint, attribution, license)
                if nr & 1:
                    acell, bcell = bcell, acell
                s += "<td align=\"right\" valign=\"top\">%s</td>\n" % acell
                s += "<td valign=\"top\">%s</td>\n" % bcell
                s += "</tr>"
            s += "</table>\n"
        return s


    # A list of all flowers, grouped by item bank, name hidden.
    # show the name with jQuery when user clicks/hover on it!
    @cherrypy.expose
    def showallwithout(self):
        s = "<a href=\"/\">naar Quiz</a>"
        for itembankname, itembank, _, _ in itembankdb.itembanks:
            for nr, (key, pronoun, prompt, hint, attribution, license) in enumerate(itembank):
                s += "<tr>"
                acell = "<img src=\"pictures/%s/%s\"><br><p><small>%s (%s)</small></p>" % (langcode, key, attribution, license)
                s += "<td align=\"right\" valign=\"top\">%s</td>\n" % acell
                s += "<td valign=\"top\">TEST</td>\n"
                s += "</tr>"
            s += "</table>\n"
        return s


# Choose a config file depending on platform (OSX, Windows, Unix, etc)
if "win32" in sys.platform:
    cfg="mchoiceapp-win.conf"
elif "darwin" in sys.platform:
    cfg="mchoiceapp-osx.conf"
else:
    raise Exception("Unrecognized platform: %s" % sys.platform)
cherrypy.log("Using configuration file '%s'" % cfg)


# Main program.
mchoice = Mchoice()
cherrypy.config.update(cfg)
root = cherrypy.tree.mount(mchoice, "/", cfg)
cherrypy.engine.autoreload.files.add("site.tpl")
cherrypy.quickstart(root)
