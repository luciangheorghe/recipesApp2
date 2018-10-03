// This code snippet was taken from StackOverflow from Themes.guide
// Here is the link to related snippet: https://stackoverflow.com/questions/17390179/using-bootstrap-to-paginate-a-set-number-of-p-elements-on-a-webpage/17552091#17552091

var listElement = $('#pageRecipes');
var perPage = 9;
var numItems = listElement.children().length;
var numPages = Math.ceil(numItems/perPage);

$('.pager').data("curr",0);

var curr = 0;
while(numPages > curr){
  $('<li><a href="#" class="page_link">'+(curr+1)+'</a></li>').appendTo('.pager');
  curr++;
}

$('.pager .page_link:first').addClass('active');

listElement.children().css('display', 'none');
listElement.children().slice(0, perPage).css('display', 'block');

$('.pager li a').click(function(){
  var clickedPage = $(this).html().valueOf() - 1;
  goTo(clickedPage,perPage);
});

function previous(){
  var goToPage = parseInt($('.pager').data("curr")) - 1;
  if($('.active').prev('.page_link').length==true){
    goTo(goToPage);
  }
}

function next(){
  goToPage = parseInt($('.pager').data("curr")) + 1;
  if($('.active_page').next('.page_link').length==true){
    goTo(goToPage);
  }
}

function goTo(page){
  var startAt = page * perPage,
    endOn = startAt + perPage;

  listElement.children().css('display','none').slice(startAt, endOn).css('display','block');
  $('.pager').attr("curr",page);
}
