(function (){

  var names = ["Yaakov", "John", "Jen", "Jason", "Paul", "Frank", "Larry", "Paula", "Laura", "Jim"];
  var name;
  for (name in names){
    var firstLetter = names[name].charAt(0);
    firstLetter = firstLetter.toLowerCase();
      if (firstLetter=='j') {
        byespeaker.speak(names[name]);
      }
      else {
        hellospeaker.speak(names[name]);
      }
  }

})();
