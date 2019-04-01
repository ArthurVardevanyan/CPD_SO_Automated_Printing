function openNewBackgroundTab(path){
window.open(path);
};

$("#FileInfo").click(function() {
  console.log('Click');
  $('[name=TC]').removeAttr('required');
  $('[name=SETS]').removeAttr('required');
  $('[nameCP]').removeAttr('required');
  $('form').submit();
});
