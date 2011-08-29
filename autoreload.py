
import cherrypy
import os
import glob

def addautoreloaddir(root, verbose=False):
    for path, dirs, files in os.walk(root):
        for filename in glob.glob(os.path.join(path,"*")):
            if not ".svn" in filename:
                if verbose:
                    cherrypy.log("Adding %s to autoreload files" % filename, "ENGINE")
                cherrypy.engine.autoreload.files.add(filename)
