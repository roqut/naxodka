[app]

# (str) Title of your application
title = naxodka

# (str) Package name
package.name = naxodka

# (str) Package domain (needed for android/ios packaging)
package.domain = org.naxodka

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ogg,ttf

# (list) List of inclusions using pattern matching
source.include_patterns = images/*.png, scr_AdminMain.py, scr_ChooseOrg.py, scr_EntitySelector.py, scr_Loading.py, scr_LoginSelector.py, scr_MainUser.py, scr_NewThing.py, scr_Registration.py, db.py, constants.py, OpenSans_SemiCondensed-BoldItalic.ttf

# (str) Source code where the main.py live
source.dir = .

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,psycopg2,base64,PIL,webbrowser

# (list) Supported orientations
# Valid options are: landscape, portrait, portrait-reverse or landscape-reverse
orientation = portrait

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0
