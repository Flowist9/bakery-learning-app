[app]
title = Bakery Training App
package.name = bakerytrainingapp
package.domain = org.example
source.dir = .
source.include_exts = py
source.exclude_dirs = tests, .venv, venv, env, .git, __pycache__, work
version = 0.1.0
requirements = python3,kivy==2.3.0
orientation = portrait
fullscreen = 0
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = False

[buildozer]
log_level = 2
warn_on_root = 1
