# coding: utf-8


def decoupe(soundfile, start, end, output=None):
    import shlex
    import subprocess
    import sys
    import operator

    commande = "sox {input} {output} trim {start} {duration}"

    print(
        soundfile,
        file=sys.stderr
    )

    if output is None:
        output = ".".join(["_".join([soundfile, str(start)]), "wav"])

    subprocess.Popen(
        shlex.split(
            commande.format(
                input=soundfile,
                output=output,
                start=str(start),
                duration=str(operator.sub(float(end), float(start)))
            )
        )
    )


def main():
    s = "banana.mp3"
    decoupe(s, 0, 100.324)

if __name__ == '__main__':
    main()