# voldemot

[![Build Status](https://travis-ci.org/dasanchez/voldemot.svg?branch=master)](https://travis-ci.org/dasanchez/voldemot)

voldemot takes a set of letters (such as a name) and assembles combinations of words based on it.

It uses the English word list from [SCOWL](http://wordlist.aspell.net/).  

## Command Line Interface

### Requirements

- Python >= 3.6

### Usage

`voldemot.py [-h] [-d DICTIONARY] [-c COUNT] [-v] [-p] [-o [OUTPUT]] input`

`input`  
the letters to de-scramble

`-h, --help`  
show this help message and exit

`-d DICTIONARY, --dictionary DICTIONARY`  
dictionary file: newline must separate all words  
default: **words/voldemot.dict.txt**

`-c COUNT, --count COUNT`  
number of words to split the letters into  
default: **2**

`-v, --verbose`  
show progress

`-p, --print`  
print results

`-o, --output [OUTPUT]`  
print results to file  
default: **voldemot.txt**

### Example

```sh
$ python voldemot.py "tom marvolo riddle" -c 3 -v -o marvolo.txt
Input (tommarvoloriddle) has 16 characters
Found 862 words.
 |██████████████████████████████████████████████████| 100.0%
10.37 seconds elapsed, there are 430 full matches.
Saving results to marvolo.txt...done.

$ head marvolo.txt
a milord voldemort
admired toll vroom
admit mod rollover
admit mol overlord
admit roll vroomed
admit rolled vroom
advert loom milord
advil dorm tremolo
advil dormer molto
advil drool mortem
```
