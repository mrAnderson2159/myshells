import sys, os

os.system('cls|clear') # print("\033c",end='')

try:
    arg = sys.argv[1]

    if arg == '--edit':
        os.system(f"atom {sys.argv[0]}")
    else:
        try:
            t = float(arg)
            print("%.1f° F    ->\t%.1f° C\n\n" % (t, (t - 32) * 5 / 9))
            print("%.1f° C    ->\t%.1f° F\n" % (t, t * 9 / 5 + 32))
        except ValueError:
            print("Errore: devi inserire un numero non qualsiasi altra cosa tu abbia deciso di inserire!")

except IndexError:
    print("Errore: devi inserire una temperatura per vedere le conversioni")
finally:
    print()
