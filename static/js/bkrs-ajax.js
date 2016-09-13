jQuery('#myform').submit(function() {
  ajax('{{=URL('otvet')}}',
       ['slovo'], 'shkatulka-slov');
  return false;
});
