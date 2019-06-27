$(document).ready(function() {
    $("#btn").click(function(){
    	var query= $("#search").val();
    	console.log(query);
    	var page = 1;
        var url="searchResults.html?query="+query+"&page=" + page;
        window.location.replace(url);
    }); 
});