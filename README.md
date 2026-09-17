# Bakery Training App

I originally developed this Python/Kivy application as an internal learning tool for my colleagues, helping them learn bakery products and their associated baking programs. This public portfolio version preserves the core quiz, learning and program browsing features.

## Background and anonymization

For legal reasons, I have omitted the original product images, product names and baking program assignments from this public version. All product records and program assignments have been replaced with generic, fictional examples, and all dependencies on product and background images have been removed.

The examples do not reflect the original workplace's product catalog or operating procedures and are not intended as real baking instructions.

## Features

- Quiz: choose the baking program for a named product from up to four distinct answers. Correct answers advance automatically; incorrect answers allow another attempt.
- Learn / Search: browse product names, categories and programs. Case-insensitive name search and category filtering work together.
- Program Section: select a program to see its assigned products.
- Text-only product presentation with scrolling lists and no external assets.
- Pending quiz transitions are cancelled when returning to the menu.

The original image identification quiz has been adapted to program recall because this edition does not include product pictures.

## Run locally

Requires Python with a graphical desktop environment. The dependency is pinned to Kivy 2.3.0, the version used for local verification with Python 3.12.

Create a virtual environment from the project directory:

```sh
python -m venv .venv
```

On Windows PowerShell, install and run without activating the environment:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

On macOS or Linux:

```sh
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python main.py
```

## Example data

The `items` list in `main.py` contains three-field tuples:

```python
("Classic Baguette", "Baguettes", "Program 1")
```

Fields are **name**, **category**, and **baking program**. Use unique names and the `Program N` naming convention with an integer number. Categories and program choices are derived automatically from the data. Include multiple programs for a useful quiz.

All example records and program assignments are fictional demonstration data. They do not represent an employer's catalog, procedures or real baking instructions. No original product catalog, branding, product photos, background images, personal paths or credentials are included. Kivy supplies its own standard widget resources; no image files need to be added to this project.

## Files

- `main.py`: application and generic example data.
- `requirements.txt`: desktop dependency.
- `.gitignore`: Python, Kivy, build output and local credential exclusions.
- `buildozer.spec`: minimal Android configuration adapted from the existing project configuration.

## Optional Android build

The configuration uses the neutral application identifier `org.example.bakerytrainingapp`. Replace it with your own identifier before distribution.

Use a separately configured Buildozer environment on Linux or WSL, with its required Android build dependencies installed. From that environment and the project directory:

```sh
buildozer android debug
```

Buildozer is an optional packaging tool, not a desktop runtime dependency. No custom icons, splash images, storage access or network permissions are configured. An Android APK has not been built or tested for this edition; the specification is a starting point, not a verified release build configuration.

## Publishing

Publish only this sanitized project directory. Review any future data additions before committing. No license is assumed on the author's behalf; add a license of your choice before offering reuse permissions.
