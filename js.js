function openNewBackgroundTab(path){
//Code Not in Use
//This Allows multiple buttons with different requirements for the same html form to exist.
window.open(path);
};
$("#FileInfo").click(function() {
  console.log('Click');
  $('[name=TC]').removeAttr('required');
  $('[name=SETS]').removeAttr('required');
  $('[nameCP]').removeAttr('required');
  $('form').submit();
});
