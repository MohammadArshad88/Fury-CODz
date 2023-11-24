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
  