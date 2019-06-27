function getParameterByName(target) {
   
    let url = window.location.href;
 
    target = target.replace(/[\[\]]/g, "\\$&");

  
    let regex = new RegExp("[?&]" + target + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';

    
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}


function handleResult(resultData) {

    console.log("handleResult: populating result table from resultData");
    let queryTable = jQuery("#results_table");
    console.log(resultData[0]);
    var count = 0;
    var len = resultData.length;
    console.log("results:"+len);
//    var start = page * 10;
//    var pagination_array = resultData.splice(start-1,start-1+10);
    for (let i = start; i < start + 10; i++) {
        if(count == 10){
            break;
        }
        if(i > len-1 || i <0){
        	break;
        }
         let rowHTML = "";
         rowHTML += "<tr>";
         rowHTML += "<th>" +

         '<a href = http://' + resultData[i]+ '>' + resultData[i] +
         '</a>' +
         "</th>";
         rowHTML += "</tr>";
              
         // Append the row created to the table body, which will refresh the page
         queryTable.append(rowHTML);
         count = count + 1;
         
    } 
    let pageHTML  = "";
    let preOffset=Number(page)-1;
    let postOffset=Number(page)+1;
    console.log(postOffset);
    var  url_temp_prev = "http://localhost:8080/Search-Engine/searchResults.html?query="+query+"&page="+ preOffset;
    var  url_temp_next = "searchResults.html?query="+query+"&page="+ postOffset;
   pageHTML += "<div>";
   pageHTML += '<button>'+'<a href = '+url_temp_prev+'>';
   pageHTML += "prev" + '</a>';
   pageHTML += "</button>";
   pageHTML += '<button>'+'<a href = '+url_temp_next+'>';
   pageHTML += "next" + '</a>';
   pageHTML += "</button>"; 
   pageHTML += "</div>";
   queryTable.append(pageHTML);
   }

$("#search").keyup(function(event) {
    if (event.keyCode === 13) {
        $("#btn").click();
    }
});

let query= getParameterByName('query');
let page = getParameterByName('page');
let start = Number(page)*10 - 1;
  $(document).ready(function(){
//  let query= getParameterByName('query');
//  let page = getParameterByName('page');
  console.log("karan:"+query);
  console.log(page);

  jQuery.ajax({
     
    cache: false,
      method: "GET",
      url: "http://127.0.0.1:4996/search/" + query, 
      success: function(resultData){
      	handleResult(resultData) ;    
      },
      error:function(response){
    	  alert("error");
      }
      
  });  
   
  });
   