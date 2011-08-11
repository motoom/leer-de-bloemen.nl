import glob
import Image
import os

convertimages = False


# TODO: Ook opslaan welke bloemen wel of niet aangesproken moeten worden met 'een'.

levels = [["easy",[]], ["medium",[]], ["hard",[]]]

levels[0][1] = (
    'Brandnetel', 'Boterbloem', 'Distel', 'Klaproos', 'Madeliefje', 'Narcis',
    'Paardenbloem', 'Sneeuwklokje', 'Tulp', 'Witte klaver', 'Zonnebloem'
    )

levels[1][1] = (
    'Akkerviooltje', 'Bieslook', 'Brem', 'Dahlia', 'Dille', 'Dovenetel',
    'Gewone berenklauw', 'Grote weegbree', 'Hyacinth', 'Kamille',
    'Kamperfoelie', 'Kerstster', 'Komkommer', 'Korenbloem', 'Margriet', 'Mimosa',
    'Pepermunt', 'Reuzenbereklauw', 'Rode klaver', 'Rozemarijn', 'Thijm', 'Tuinanjer', 'Vlas'
    )

levels[2][1] = (
    'Aardpeer', 'Anemoon', 'Aster', 'Dotterbloem', 'Echte kervel', 'Fluitenkruid', 'Freesia', 'Gember',
    'Gipskruid', 'Goudzuring', 'Groot hoefblad', 'Grote kattestaart', 'Gulden sleutelbloem', 'Guldenroede',
    'Hondsviooltje', 'Hortensia', 'Iris', 'Keizerskroon', 'Klein hoefblad', 'Lelietje van dalen', 'Muizenoor',
    'Orchidee', 'Phlox', 'Pioen', 'Ridderspoor', 'Ridderzuring', 'Rode zijdeplant', 'Ruige weegbree', 
    'Sint janskruid', 'Slaapbol', 'Smalle weegbree', 'Stengelloze sleutelbloem', 'Valeriaan', 'Vetkruid', 'Zeepkruid', 
    'Zevenblad', 'Zinkviooltje'
    )

articleless = (
    'Witte klaver',
    'Bieslook',
    'Brem',
    'Dille',
    'Mimosa',
    'Pepermunt',
    'Rode klaver',
    'Rozemarijn',
    'Thijm',
    'Vlas',
    'Echte kervel',
    'Fluitenkruid',
    'Gember',
    'Gipskruid',
    'Phlox',
    'Valeriaan',
    'Vetkruid',
    'Zeepkruid',
    )
    
    
def process(langcode, article):
    db = {}
    for nr, infile in enumerate(glob.glob(langcode + "/*.jpg")):
        bloemnaam = os.path.split(infile)[1]
        bloemnaam = os.path.splitext(bloemnaam)[0]
        bloemtitel = bloemnaam.capitalize().replace("-", " ")
        doeljpg = "%04d.jpg" % nr
        txtfilename = os.path.join(langcode, "%s.txt" % bloemnaam)
        lines = open(txtfilename, "rt").readlines()
        if len(lines) < 2:
            raise Exception("%s: missing license" % txtfilename)            
        weetje = lines[0].strip().replace("'", "''")
        attribution = lines[1].strip().replace("'", "''")
        user, licencestr = attribution.split(",")
        user = user.strip()
        licencestr = licencestr.strip()
        if not licencestr:
            raise Exception("%s: missing license" % txtfilename)
        licences = licencestr.split(" ")
        if len(licences) > 1:
            raise Exception("%s: multiple licenses, prefer 'cc' or 'pd'-only." % txtfilename)            
        for license in licences:
            license = license.strip()
            if not license: continue
            if license == "cc":
                pass
            elif license == "pd":
                pass
            else:
                raise Exception("%s: unrecognized license type '%s'" % (txtfilename, license))
        # 'pd' public domain, 'cc' = Create commons delen/remix/naamsvermelding/gelijk delen
        # nl: http://nl.wikipedia.org/wiki/Creative_Commons en 
        #     http://creativecommons.org/licenses/by-sa/3.0/deed.nl <==
        #     http://creativecommons.org/licenses/by-sa/3.0/nl/
        #     http://creativecommons.org/licenses/by/3.0/nl/
        #
        # en: http://en.wikipedia.org/wiki/Creative_Commons
        #     http://creativecommons.org/licenses/by-sa/3.0/deed.en
        #     http://creativecommons.org/licenses/by/3.0/
        #
        # GDFL
        # http://en.wikipedia.org/wiki/Wikipedia:Text_of_the_GNU_Free_Documentation_License
        # Creative Commons ShareAlike: http://creativecommons.org/licenses/by-sa/3.0/
        # "Naam, licentietype"
        #
        # fal: Free Art Libre, http://artlibre.org/licence/lal/en
        #
        if convertimages:
            im = Image.open(infile)
            im.thumbnail((400,300), Image.ANTIALIAS)
            im.save("../static/pictures/" + langcode + "/" + doeljpg, "jpeg")

        articlestr = article
        if bloemtitel in articleless:
            articlestr = ""
        db[bloemtitel]= "    ('%s', '%s', '%s', '%s', '%s', '%s')," % (doeljpg, articlestr, bloemtitel, weetje, user, license)

    for level, bloemtitels in levels:
        print "%s = (" % level
        for bloemtitel in bloemtitels:
            print db[bloemtitel]
        print ")\n"
    
process("nl", "een")
process("en", "a")
