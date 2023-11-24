var selectedValue = "win"


  
  var toggleSuccess = function() {
    var progressButton = document.querySelector('.progress-button');
    progressButton.classList.add('success');
    draw('.checkmark path');
    
    setTimeout(function() {
      progressButton.classList.remove('success');
      progressButton.classList.remove('loading');
      resetDashes();
    }, 3000);
  };

  var toggleError = function() {
    var progressButton = document.querySelector('.progress-button');
    progressButton.classList.add('error');
    draw('.cross path');
    
    setTimeout(function() {
      progressButton.classList.remove('error');
      progressButton.classList.remove('loading');
      resetDashes();
    }, 3000);
  };
  
  function draw(loc) {
    var paths = document.querySelectorAll(loc);
    for (var i = 0; i < paths.length; i++) {
      paths[i].style.strokeDashoffset = '0';
    }
  }
  
  function resetDashes() {
    var paths = document.querySelectorAll('path');
    for (var i = 0; i < paths.length; i++) {
      var path = paths[i];
      var length = path.getTotalLength();
      path.style.strokeDasharray = length + ' ' + length;
      path.style.strokeDashoffset = length;
    }
  }

