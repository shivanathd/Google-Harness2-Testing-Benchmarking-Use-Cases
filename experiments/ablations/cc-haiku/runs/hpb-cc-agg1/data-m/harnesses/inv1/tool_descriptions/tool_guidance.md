The shell is zsh. An unquoted word that starts with `=` is expanded as a command name: `echo ====` fails with `(eval):1: === not found` and the rest of that command line is skipped. Quote such tokens (`echo "===="`). Read the error line before re-running; fix the token that failed, once.

If the same shell error returns after one fix, stop using shell for that step and run a `python3 -c` one-liner instead.
