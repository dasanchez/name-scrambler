var process = document.querySelector('button'),
    input = document.querySelector('input'),
    count = document.getElementById('count'),
    results = document.querySelector('.results'),
    combinations = document.querySelector('.combinations');

var names = ['isaacasimov', 'iainmbanks', 'arthurclarke',
 'corydoctorow', 'williamgibson', 'frankherbert', 'ursulaleguin', 'stephenking']

// progress bar:
var progress=0;
var total = 0;
var totalRoots = 0;

var currentRequest = '';
var progressContainer = document.getElementById("progCon");
var progressBar = document.getElementById("progBar");
var progressText = document.querySelector(".prog-text");
var body = document.getElementsByTagName("BODY")[0];

async function setProgress(newProgress) {
    contW = progressContainer.clientWidth;
    var pixelValue = (contW*newProgress/100);
    progressBar.style.width = pixelValue+"px";
    progressText.textContent = newProgress;
  }

body.onresize = function() {
    setProgress(progress)    
};

  var x = 0;
  function myFunction() {
      var txt = x += 1;
      document.getElementById("demo").innerHTML = txt;
  }

input.addEventListener("keyup", function(event) {
    event.preventDefault();
    if(event.keyCode === 13) {
        process.click();
    }
});

process.onclick = function (event) {
    var letters = input.value;
    setProgress(0)
    total = 0;
    results.textContent = 'Requested combinations...';
    progressText.style.visibility = "visible";

    while (combinations.firstChild) {
        combinations.removeChild(combinations.firstChild);
    }

    console.log('Processing ' + letters + ':');
    var words = parseInt(count.value);

    var myJSON = {
        "type": "voldemot-request",
        "input": letters,
        "word-count": words
    };
    console.log(myJSON);

    // try {
        websocket = new WebSocket("ws://" + document.domain + ":9000/");
        websocket.onmessage = function (event) {
 
            data = JSON.parse(event.data);
            if (data['total-matches']) {
                if (data['value'] == 0){
                results.textContent = currentRequest + ": " + 'No combinations found';
                } else if (data['value'] == 1) {
                    results.textContent = currentRequest + ": " + '1 combination found';
                } else {
                    results.textContent = currentRequest + ": " + data['value'] + ' combinations found';
                }
                console.log("Total matches received: " + total);
            } else if (data['match']) {
                 var combo = document.createElement('div');
                combo.className = 'match';
                combo.textContent = data['value'];
                combinations.appendChild(combo);
                total += 1;
                results.textContent = currentRequest + ':' + total + ' combinations found';
            } else if (data['rootWord']) {
                var rootWord = document.createElement('div');
                rootWord.className = 'rootWord'
                rootWord.textContent = data['value'];
                combinations.appendChild(rootWord);
                totalRoots += 1;                
            } else if (data['percent']) {
                console.log('percent done: ' + data['value']);
                progress=data['value']
                setProgress(progress)
            } else if (data['reject']) {
                if (data['reason']==='max-users') {
                    results.textContent = 'Max connections reached, try again later';
                }
                console.log('Connection rejected: ' + data['reason']);
            } else if (data['input']) {
                currentRequest = data['value'];
                results.textContent = 'Processing ' + currentRequest + '...';
                console.log('Processing ' + data['value']);
            }
        };
        
        websocket.onopen = function(evt) {
        websocket.send(JSON.stringify(myJSON));
        }
};

input.focus();

input.value = names[Math.floor(Math.random() * names.length)];

input.onchange = function (event) {
    console.log("New value: " + input.value)
}
