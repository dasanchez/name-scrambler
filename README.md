# voldemot

[![Build Status](https://travis-ci.org/dasanchez/voldemot.svg?branch=master)](https://travis-ci.org/dasanchez/voldemot)

voldemot takes a set of letters (such as a name) and assembles combinations of words based on it.

It uses the English word list from [SCOWL](http://wordlist.aspell.net/).  

## Usage

`python voldemot.py input [filename] [word count]`

## Example

`python voldemot.py albertcamus words/voldemot-dict.txt 2`

The above example will yield 113 combinations, beginning with _ablate scrum_ and ending with _tsamba ulcer_.  
It is up to the user to find the real gems, such as _cabal muster_ and _lust macabre_ in this case.