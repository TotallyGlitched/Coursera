(function (window){

  var speakWord = "Good Bye";
  var byespeaker = {}
  byespeaker.speak = function (name) {
    console.log(speakWord + " " + name);
  }
  window.byespeaker = byespeaker;

})(window);
