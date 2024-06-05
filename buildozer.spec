[app]

# (str) Title of your application
title = NAXODKA

# (str) Package name
package.name = naxodka

# (str) Version of your application
version = 1.0

# (str) Main module name.
main = APP

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ogg,ttf

# (list) List of inclusions using pattern matching
source.include_patterns = images/*.png, scr_AdminMain.py, scr_ChooseOrg.py, scr_EntitySelector.py, scr_Loading.py, scr_LoginSelector.py, scr_MainUser.py, scr_NewThing.py, scr_Registration.py, db.py, constants.py, OpenSans_SemiCondensed-BoldItalic.ttf

# (str) Source code where the main.py live
source.dir = .

# (str) Supported orientation (one of landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET