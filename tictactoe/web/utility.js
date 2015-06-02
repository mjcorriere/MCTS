// Utility functions
function clamp(value, minimum, maximum) {
  return Math.max(minimum, Math.min(value, maximum));
}

function zip(array1, array2) {

  var length = Math.min(array1.length, array2.length);
  var zipped = [];

  for (var i = 0; i < length; i++) {
      zipped.push([array1[i], array2[i]]);
  }

  return zipped;

}

// The Fisher-Yates (or Knuth) Shuffle
function shuffle(array) {
  var i = array.length;
  var e, temp;

  while (i !== 0) {
    i--;

    // Pick a random element that hasn't been shuffled.
    e = Math.floor(Math.random() * i);

    // Swap it
    temp = array[e];
    array[e] = array[i];
    array[i] = temp;

  }

  return array;

}
