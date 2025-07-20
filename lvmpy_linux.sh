#!/usr/bin/bash
export MICROPYPATH=.frozen:~/.micropython/lib:/usr/lib/micropython:./lib:.
./micropython "$@"
