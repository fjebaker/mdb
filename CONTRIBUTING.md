# How to contribute

Awesome :sunglasses:, you want to help make `mdb` better. Please read these guidelines on how to get involved!

## Reporting Bugs

1. Use the GitHub issue search -- check if the issue has already been reported.
2. Check if the issue has been fixed -- try to reproduce it with the latest `main` branch.
3. Isolate the problem -- ideally create a [minimal reproducible example](https://stackoverflow.com/help/minimal-reproducible-example) (MWE).
4. Raise an issue with as much information as possible (including your MWE) and label it as `bug`.

A good bug report should contain all the information necessary to allow a developer to reproduce the issue, without needing to
ask for further information. Please try to be as detailed as possible in your report. What is your environment? What steps will
reproduce the issue? What gdb version, MPI library, python version and OS experience the problem? What is the expected outcome?
All of these details assist the process of investigating and fixing bugs.

## Requesting Features

Feature requests are welcome, `mdb` is under active development. My personal ambition is to make `mdb` a powerful debugger for
MPI applications, whilst also trying to take advantage of as much of `gdb`'s built-in features as possible.

Raise an issue and label it as `enhancement`.

## Submitting Pull Requests

Good pull requests—patches, improvements, new features—are a fantastic help. They should remain focused in scope and avoid
containing unrelated commits.

Always write a clear log message for your commits. One-line messages are fine for small changes, but bigger changes should look
like this:

    $ git commit -m "A brief summary of the commit
    > 
    > A paragraph describing what changed and its impact."


**Please ask first** before embarking on any significant pull request (e.g. implementing features, refactoring code), otherwise
you risk spending a lot of time working on something that may not be suitable for this project. (If you feel you want to take
`mdb` in a vastly different direction, feel free to make a fork).

Please adhere to the [coding conventions](#Coding-Conventions) used in this project.

Before merging, pull requests are required to pass all continuous integration.

## Testing

:flushed: currently the tests are not pushed into main yet, and they are nowhere near complete. This is a great place to start
if you want to help with something small.

## Coding conventions

I use [black](https://black.readthedocs.io/en/stable/index.html) and [flake8](https://flake8.pycqa.org/en/latest/) to enforce
consistent style. In general I try to use _sensible_ naming conventions although I appreciate that is hard to condense into
words. Please use your best judgement and look at the rest of the code for inspiration.

Thanks, Tom