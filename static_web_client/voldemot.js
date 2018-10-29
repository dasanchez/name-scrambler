var process = document.querySelector('button'),
    input = document.querySelector('input'),
    count = document.querySelector('.slider-range'),
    results = document.querySelector('.results'),
    combinations = document.querySelector('.combinations');

var progressContainer = document.getElementById("progCon");
var progressBar = document.getElementById("progBar");
var progressText = document.querySelector(".prog-text");
var body = document.getElementsByTagName("BODY")[0];
var range = document.querySelector('input[type="range"]');

// progress:
var progress = 0;
var total = 0;
var totalRoots = 0;
var pauseInterval = 1000;
var pauseLength = 5; // milliseconds
var currentRequest = '';

// dictionary
var dictionary = []

var rangeValue = function () {
    var newValue = range.value;
    var target = document.querySelector('.slider-value');
    target.innerHTML = newValue;
}

range.addEventListener("input", rangeValue);

async function setProgress() {
    contW = progressContainer.clientWidth;
    var pixelValue = (contW * progress / 100);
    progressBar.style.width = pixelValue + "px";
    progressText.textContent = progress;
}

body.onresize = function () {
    setProgress()
};

input.addEventListener("keyup", function (event) {
    event.preventDefault();
    if (event.keyCode === 13) {
        process.click();
    }
});

function cleanInput(rawLetters) {
    cleanLetters = rawLetters.toLowerCase();
    cleanLetters = cleanLetters.replace(/[^a-z]/gi, '');
    cleanLetters = cleanLetters.slice(0, 16);
    return cleanLetters;
}

function wordIsPresent(candidate, letters) {
    for (var index = 0; index < letters.length; index++) {
        var c = letters.charAt(index);
        candidate = candidate.replace(c, '');
    }
    return !candidate;
}

function getRootWords(inputLetters) {
    var rootWords = []

    for (var index = 0; index < dictionary.length; index++) {
        if (wordIsPresent(dictionary[index], inputLetters)) {
            rootWords.push(dictionary[index]);
        }
    }
    return rootWords;
}

function getWordsEqualTo(candidates, targetLength) {
    var filteredList = [];
    for (var index = 0; index < candidates.length; index++) {
        if (candidates[index].length === targetLength) {
            filteredList.push(candidates[index]);
        }
    }
    return filteredList;
}

function getWordsUnder(candidates, targetLength) {
    var filteredList = [];
    for (var index = 0; index < candidates.length; index++) {
        if (candidates[index].length < targetLength) {
            filteredList.push(candidates[index]);
        }
    }
    return filteredList;
}

async function sleep(ms = 0) {
    return new Promise(r => setTimeout(r, ms));
}

function displayNewMatch(newWord) {
    var combo = document.createElement('div');
    combo.className = 'match';
    combo.textContent = newWord;
    combinations.appendChild(combo);
}

function displayResults(inputLetters, combinations) {
    if (combinations == 0) {
        results.textContent = inputLetters + ": " + 'No combinations found';
    } else if (combinations == 1) {
        results.textContent = inputLetters + ": " + '1 combination found';
    } else if (combinations >= 10000) {
        results.textContent = inputLetters + ": " + 'reached 10,000 limit';
    }    
    else {
        results.textContent = inputLetters + ": " + combinations + ' combinations found';
    }
}

async function findWordCombinations(candidates, inputLetters, wordCount) {
    var newPercent = 0;
    var wordList = []
    var pause = pauseInterval;
    totalRoots = 0;
    total = 0;
    rootList = getWordsUnder(candidates, inputLetters.length - (wordCount - 2));
    tempWords = rootList.slice();
    lettersLength = inputLetters.length;
    sortedLetters = inputLetters.split('').sort().join('');

    for (var rootIndex = 0; rootIndex < rootList.length; rootIndex++) {
        totalRoots += 1
        var prefixList = [rootList[rootIndex]];
        for (var baggageCounter = 2; baggageCounter <= wordCount; baggageCounter++) {
            var newPrefixList = [];
            for (var prefixIndex = 0; prefixIndex < prefixList.length; prefixIndex++) {
                var lastPrefix = prefixList[prefixIndex].split(' ').pop();
                var tempList = tempWords.slice(tempWords.indexOf(lastPrefix));
                var collapsedPrefix = prefixList[prefixIndex].replace(/ /g, '');
                var spotsAvailable = lettersLength - collapsedPrefix.length;

                if (baggageCounter === wordCount) {
                    var lastSet = getWordsEqualTo(tempList, spotsAvailable);
                    for (var lastSetIndex = 0; lastSetIndex < lastSet.length; lastSetIndex++) {
                        var sortedEntry = (collapsedPrefix + lastSet[lastSetIndex]).split('').sort().join('');
                        if (sortedEntry === sortedLetters) {
                            total += 1;
                            var newMatch = prefixList[prefixIndex] + ' ' + lastSet[lastSetIndex];
                            wordList.push(newMatch);
                            displayNewMatch(newMatch);
                            if (total >= 10000)
                            {
                                progress=100;
                                setProgress();
                                return wordList;
                            }
                            results.textContent = inputLetters + ": " + total + ' combinations found';
                        }
                    }
                }
                else {
                    var baggageLeft = spotsAvailable - (wordCount - baggageCounter - 1);
                    var baggageList = getWordsUnder(tempList, baggageLeft);
                    for (var baggageIndex = 0; baggageIndex < baggageList.length; baggageIndex++) {
                        if (wordIsPresent(collapsedPrefix + baggageList[baggageIndex], inputLetters)) {
                            newPrefixList.push(prefixList[prefixIndex] + ' ' + baggageList[baggageIndex]);
                        }
                    }
                }
                pause -= 1;
                if (pause === 0)
                {
                    await sleep(pauseLength);
                    pause = pauseInterval;
                }
            } // end prefix loop
            prefixList = newPrefixList.slice();
        } // end baggage loop
        tempWords = tempWords.slice(tempWords.indexOf(rootList[rootIndex]));
        newPercent = parseInt(totalRoots * 100 / rootList.length);
        if (newPercent != progress) {
            progress = newPercent;
            setProgress();
            await sleep(pauseLength);
        }
    } // end root list loop
    return wordList;
}

process.onclick = async function (event) {
    var letters = input.value;
    progress = 0;
    total = 0;
    setProgress();
    results.textContent = 'Requested combinations...';
    progressText.style.visibility = "visible";

    while (combinations.firstChild) {
        combinations.removeChild(combinations.firstChild);
    }

    var words = parseInt(count.value);

    // 1. Clean up input
    letters = cleanInput(letters);
    console.log('Processing ' + letters + ':');

    // 2. Find root words in dictionary
    var rootWords = getRootWords(letters);
    console.log("Collected " + rootWords.length + " root words.");

    // display root words
    for (var index = 0; index < rootWords.length; index++) {
        var rootWord = document.createElement('div');
        rootWord.className = 'rootWord'
        rootWord.textContent = rootWords[index];
        combinations.appendChild(rootWord);
    }

    // 3. Find word combinations
    var wordList = [];
    if (words === 1) { // one word?
        oneWordList = getWordsEqualTo(rootWords, letters.length);

        for (var index = 0; index < oneWordList.length; index++) {
            total += 1;
            // console.log(oneWordList[index]);
            displayNewMatch(oneWordList[index]);
        }
        progress = 100;
        setProgress();
        displayResults(letters, oneWordList.length);
    }
    else { // 2+ words
        wordList = await findWordCombinations(rootWords, letters, words);
        displayResults(letters, wordList.length);
    }
};

rangeValue();
input.focus();

// load dictionary
var oReq = new XMLHttpRequest();
oReq.addEventListener("load", reqListener);
oReq.open("GET", "./voldemot_dict.txt");
oReq.send();

// dictionary request event listener
function reqListener(evt) {
    console.log("The transfer is complete.");

    if (oReq.readyState === 4) {  // document is ready to parse.
        if (oReq.status === 200) {  // file is found
            dictionary = oReq.responseText.split("\n");
            console.log("Dictionary loaded.");// First 10 words:");
            for (var index = 0; index < dictionary.length; index++) {
                dictionary[index] = dictionary[index].replace(/\r/, '');
            }
        } else alert("voldemot_dict.txt not found");
    } else alert("voldemot_dict.txt not ready to parse");

}

// test readDictionary