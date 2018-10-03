// This code snippet was taken from StackOverflow from how to use pagination
// Here is the link to related snippet: https://stackoverflow.com/questions/19605078/how-to-use-pagination-on-html-tables

$(document).ready(function(){
    $('#pagDashboard').after('<div id="nav"></div>');
    var rowsShown = 8;
    var rowsTotal = $('#pagDashboard tbody tr').length;
    var numPages = rowsTotal/rowsShown;
    for(i = 0;i < numPages;i++) {
        var pageNum = i + 1;
        $('#nav').append('<a href="#" rel="'+i+'">'+pageNum+'</a> ');
    }
    $('#pagDashboard tbody tr').hide();
    $('#pagDashboard tbody tr').slice(0, rowsShown).show();
    $('#nav a:first').addClass('active');
    $('#nav a').bind('click', function(){

        $('#nav a').removeClass('active');
        $(this).addClass('active');
        var currPage = $(this).attr('rel');
        var startItem = currPage * rowsShown;
        var endItem = startItem + rowsShown;
        $('#pagDashboard tbody tr').css('opacity','0.0').hide().slice(startItem, endItem).
        css('display','table-row').animate({opacity:1}, 300);
    });
});
