# voldemot

[![Build Status](https://travis-ci.org/dasanchez/voldemot.svg?branch=master)](https://travis-ci.org/dasanchez/voldemot)

voldemot takes a set of letters (such as a name) and assembles combinations of words based on it.

It uses the English word list from [SCOWL](http://wordlist.aspell.net/).  

## Command Line Interface

### Requirements
- Python >= 3.6

### Usage

`voldemot.py [-h] [-d DICTIONARY] [-c COUNT] [-v] [-p] input`

`input`  
the letters to de-scramble

`-h, --help`  
show this help message and exit

`-d DICTIONARY, --dictionary DICTIONARY`  
dictionary file: newline must separate all words

`-c COUNT, --count COUNT`  
number of words to split the letters into

`-v, --verbose`  
show progress

`-p, --print`  
print results

### Example

`python voldemot.py albertcamus -c 2 -v -p`

This command will print:
- `-v` => the number of letters being analyzed
- `-v` => the number of matching words found in the dictionary
- `-v` => a progress bar
- `-p` => 113 results, beginning with _ablate scrum_ and ending with _tsamba ulcer_.  

