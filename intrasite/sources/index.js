// SCSS or SASS here
require('./main.scss');

// Images
require('./img/logo.png');
require('./img/academic_logo.svg');

// Fonts

// Javascripts

var $ = require('jquery');
window.$ = $;

require('popper.js');
require('bootstrap');

$(document).ready(
  function() {
    $('[data-toggle="tooltip"]').tooltip()
  }
);