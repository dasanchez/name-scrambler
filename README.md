# voldemot

Takes a set of letters (such as a name) and assembles combinations of words based on it.
Using English word list from SCOWL.
The results are output to a text file: [input]-iter.txt

## Usage:

`python name-scrambler letters [filename] [slots]`

## Example

`python voldemot albertcamus words/voldemot-dict.txt 2`

The above example will yield a text file called **albert-camus.iter** that contains 1125 combinations, beginning with _a clubmaster_ and ending with _tsamba ulcer_. It is up to the user to find the real gems, such as _cabal muster_ and _macabre slut_ in this case. 