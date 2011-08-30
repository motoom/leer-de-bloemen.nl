# -*- coding: utf-8 -*-

# mchoiceapp.py - Software by Michiel Overtoom, motoom@xs4all.nl

# Ideas/TODOs:
#
# - Rotating logfile.
# - Templatize everything, translate all strings (en/nl template hierarchy).
# - English version / internationalisation.
# - Extra flowers (madelief, distel, etc...).
# - Online highscore list, enter your name when you get a high score.
# - Show high score rankings.
# - Feedback form when complete: which were the flowers you had most problems with?.
# - Meticulous logging (or analysis of logs afterwards) so we can see how people play the quiz.
# - Decorator to automatically persist/restore state to/from session.

import sys
import os
import cherrypy
from cherrypy import expose
import random
import time
import socket
from ovotemplate import Ovotemplate
import logging
import autoreload
import imp
import inspect


threshold = 2 # (3) The number of times the user has to answer an item correctly in a row before it's considered a known item. (suggestion: 3)
tolearnsize = 7 # (10) Number of items currently being learned.
lowatermark = 5 # (5) When the learning has shrunken to 'lowatermark' or less items, refill it from the items to learn.
alternatives = 4 # (4) Nr. of alternatives to show at each multiple-choice question.

def clamp(value, lower, upper):
    if value < lower: return lower
    if value > upper: return upper
    return value


# For multiple choice nomenclature, see http://en.wikipedia.org/wiki/Multiple_choice
class Item(object):
    def __repr__(self):
        return "%s: %s (%d correct in a row, %d correct total, %d incorrect total)" % (self.prompt, self.answer, self.correctrow, self.correct, self.incorrect)


class Mchoice(object):

    def __init__(self):
        self.language = cherrypy.config["language"]
        self.tem_site = self.loadtemplate("site.tpl")
        self.tem_levelstart = self.loadtemplate("levelstart.tpl")
        self.tem_correct = self.loadtemplate("correct.tpl")
        self.tem_wrong = self.loadtemplate("wrong.tpl")
        self.tem_progress = self.loadtemplate("progress.tpl")
        self.tem_verdict = self.loadtemplate("verdict.tpl")
        # Check whether itembank contains non-ascii characters.
        # Such characters should be specified as HTML entities.
        for _, itembank, _, _ in itembankdb.itembanks:
            for _, _, answer, hint, attribution, license in itembank:
                answer.encode("ascii")
                hint.encode("ascii")
                attribution.encode("ascii")
                # And also check the licensing of the pictures, Creative Commons or Public Domain.
                if license not in ("cc", "pd"): raise Exception("%s: license type must be 'cc' or 'pd'" % answer)


    def loadtemplate(self, fn):
        return Ovotemplate().fromfile(os.path.join("templates", self.language, fn)) 
               

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
        difficulty = clamp(difficulty, 0, len(itembankdb.itembanks) - 1)
        self.populatesession(difficulty)
        raise cherrypy.InternalRedirect('/')


    def randomcorrect(self):
        return random.choice(texts.corrects)


    def randomwrong(self):
        return random.choice(texts.wrongs)


    # Waaaah! Reduce the size of this routine. It's too long.
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
            tickets.add(ticket) # TODO: Protect against DoS, empty tickets when there are 20.000 in there (or some other high improbable number). Or remove the oldest entries.

            # If an answer is given, check whether it's correct.
            if answer is None or key is None:
                if not len(learned):
                    # Show an encouraging starting message at start of game:
                    message = itembankdb.itembanks[difficulty][2] # [2] is the item bank intro text
            elif answer == rightone:
                wascorrect = True
                key.correct += 1
                key.correctrow += 1
                correctanswer =  key.answer.lower()
                # See if the key has been sufficiently correctly answered; if so, remove it from the items to learn, add it to the learned items, and add a fresh key to the items to learn.
                known = False
                if key.correctrow >= threshold:
                    known = True
                    learned.append(key)
                    learning.remove(key)
                    if len(learning) <= lowatermark:
                        self.addtolearn(tolearn, tolearnsize, learning)
                    if not len(learning):
                        # The user knows all the itembank now.
                        # TODO: Review the items just learned, sorted on the most errors made.
                        done = True
                        message = ""
                if done:
                    message = ""
                else:
                    message = self.tem_correct.render(dict(correct=self.randomcorrect(), language=self.language, prompt=key.prompt, pronoun=key.pronoun, correctanswer=correctanswer, known=known))

            else:
                key.incorrect += 1
                key.correctrow = 0
                wronganswer = options[answer].answer.lower()
                correctanswer =  key.answer.lower()
                message = self.tem_wrong.render(dict(wrong=self.randomwrong(), wronganswer=wronganswer, language=self.language, prompt=key.prompt, pronoun=key.pronoun, correctanswer=correctanswer))

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
                progress = self.tem_progress.render(dict(percent=str(int(percent))))
            else:
                progress = texts.youknowthemall

        # Show narrator picture in which mood? -4 = angry, 0 = neutral, 4 = happy (and values in-between).
        feedbackmood=0
        if key and 0 < percent < 100:
            if wascorrect:
                feedbackmood = clamp(percent/20, 1,4)
            else:
                feedbackmood = clamp(key.correct - key.incorrect, -4, -1)

        if done:
            logmsg = "Level %d completed by %s" % (difficulty, cherrypy.request.remote.ip) # TODO: Also try to keep stats like how long it took, how many good/bad answers, etc.
            cherrypy.log(logmsg, "COMPLETE", logging.INFO)
            url = cherrypy.url("reset")
            urlagain = urlsame = urlnext = urlprev = None
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
            verdict = self.tem_verdict.render(dict(alldone=itembankdone,urlnext=urlnext, urlagain=urlagain, urlprev=urlprev, urlsame=urlsame))
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
                    raise Exception(texts.logicbug)
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
            message = self.tem_levelstart.render({})
            feedbackmood = 0
            feedback = True
        feedbackpicture = os.path.join("img", "feedback%d.gif" % feedbackmood)
        promptpicture = os.path.join("pictures", self.language, key.prompt)

        # License
        license = ""
        if key.license == "pd":
            license = "<a target=\"_new\" href=\"http://wiki.creativecommons.org/Public_domain\">public domain</a>"
        elif key.license == "cc":
            license = "<a target=\"_new\" href=\"http://creativecommons.org/licenses/by-sa/3.0/deed.nl\">creative commons</a>"
        vars = dict(answers=answers, weetje=key.hint, attribution=key.attribution, license=license, language=self.language, prompt=promptpicture, feedback=feedback, feedbackpicture=feedbackpicture, progress=progress, message=message, verdict=verdict)
        return self.tem_site.render(vars)


    # A list of all flowers, grouped by item bank.
    @cherrypy.expose
    def showall(self):
        s = "<a href=\"/\">%s</a>" % texts.toquiz
        for itembankname, itembank, _, _ in itembankdb.itembanks:
            s += "<h2>%s</h2><table>\n" % itembankname
            for nr, (key, pronoun, prompt, hint, attribution, license) in enumerate(itembank):
                s += "<tr>"
                src = os.path.join("pictures", self.language, key)
                acell = "<img src=\"%s\">" % src
                bcell = "<h3>%d. %s</h3><p>%s</p><p><small>%s (%s)</small></p>" % (nr, prompt, hint, attribution, license)
                if nr & 1:
                    acell, bcell = bcell, acell
                s += "<td align=\"right\" valign=\"top\">%s</td>\n" % acell
                s += "<td valign=\"top\">%s</td>\n" % bcell
                s += "</tr>"
            s += "</table>\n"
        return s


    # A list of all flowers, grouped by item bank, name hidden.
    # TODO: Show the name with jQuery when user clicks/hover on it!
    @cherrypy.expose
    def showallwithout(self):
        s = "<a href=\"/\">%s</a>" % texts.toquiz
        for itembankname, itembank, _, _ in itembankdb.itembanks:
            for nr, (key, pronoun, prompt, hint, attribution, license) in enumerate(itembank):
                s += "<tr>"
                src = os.path.join("pictures", self.language, key)
                acell = "<img src=\"%s\"><br><p><small>%s (%s)</small></p>" % (src, attribution, license)
                s += "<td align=\"right\" valign=\"top\">%s</td>\n" % acell
                s += "<td valign=\"top\">TEST</td>\n"
                s += "</tr>"
            s += "</table>\n"
        return s


def importbyname(modname):
    modf, modfn, moddesc = imp.find_module(modname, [os.path.join("templates", cherrypy.config["language"])])
    mod = imp.load_module(modname, modf, modfn, moddesc)
    modf.close()
    return mod
    
# Main program.
# Determine the language from from the path on which this script runs.
language = "nl" # Default dutch.
path = os.path.abspath(inspect.getsourcefile(Mchoice))
if "leer-de-bloemen.nl" in path: language = "nl"
if "learn-the-flowers.com" in path: language = "en"
cherrypy.log("Using language '%s'" % language, "ENGINE")
cherrypy.config["language"] = language

cfg = socket.gethostname()
if "." in cfg: cfg = cfg.split(".")[0]
cfg = os.path.join("cfg", cfg + "-" + language + ".cfg");
cherrypy.log("Using configuration file '%s'" % cfg, "ENGINE")
cherrypy.config.update(cfg)

    
# Import "templates/<language>/texts.py" which contains the translated strings.
# Also import the itembank database, which is also language-dependent.
texts = importbyname("texts")
itembankdb = importbyname("itembankdb")

# Instantiate and mount the app.
mchoice = Mchoice()
root = cherrypy.tree.mount(mchoice, "/", cfg)

# Drop privileges, if user/group given.
user, group = cherrypy.config.get("server.user"), cherrypy.config.get("server.group")
dropargs = {}
if user: dropargs["uid"] = user
if group: dropargs["gid"] = group
if dropargs:
    cherrypy.process.plugins.DropPrivileges(cherrypy.engine, **dropargs).subscribe()

if __name__ == "__main__":
    # Webapp started on the commandline.
    autoreload.addautoreloaddir("templates", True)
    cherrypy.quickstart(root)
else:
    # Webapp started by cherryd
    pass
