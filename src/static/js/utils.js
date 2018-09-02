$(function(){
	$('#btnRefresh').click(function(){

		$.ajax({
			url: '/refresh',
//			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
			    var json = $.parseJSON(response);
				console.log(response);
				putData(json);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
	$('#btnScrape').click(function(){

    		$.ajax({
    			url: '/scrape',
    //			data: $('form').serialize(),
    			type: 'POST',
    			success: function(response){
    			    var json = $.parseJSON(response);
    				console.log(response);
    				if (IsJsonString) {
    				    aaplData(response);
    				} else{
    				    alert("Something Wrong Happened!!!");
    				}

    			},
    			error: function(error){
    				console.log(error);
    			}
    		});
    	});
});

function IsJsonString(str) {
    try {
        JSON.parse(str);
    } catch (e) {
        return false;
    }
    return true;
}

function aaplData(tableData) {
    if (tableData != "Error") {
        var tbody = d3.select("#aapl-table-body");
     // Use d3 to update each cell's text with
     // a data from tableDate
       obj = JSON.parse(tableData)
       Object.entries(obj).forEach(function([key, value]) {
            row = tbody.append("tr");
            cell = row.append("td");
            date = new Date(key/1).toISOString().substring(0, 10);
            cell.text(date);
            cell = row.append("td");
            cell.text(value.Open);
            cell = row.append("td");
            cell.text(value.High);
            cell = row.append("td");
            cell.text(value.Low);
            cell = row.append("td");
            cell.text(value.Close);
            cell = row.append("td");
            cell.text(value["Adj Close"]);
            cell = row.append("td");
            cell.text(value.Volume);
            console.log(key+" :   "+value["Adj Close"]);
        });
    } else {
        alert("Error Happened!!");
    }
}

function putData(tableData) {
// convert array to JSON
//    jsonData = JSON.stringify(tableData);
// Get a reference to the table body
	var tbody = d3.select("#stock-table-body");
 // Use d3 to update each cell's text with
 // a data from tableDate
 // Going through all data
	tableData.forEach(function(stockData) {
// ufoData - it's a one object in tableData which will put in the row
// add new row into the table
	  var row = tbody.append("tr");
// go through all elements in the object: ID, name, CountuCode,...
	  Object.entries(stockData).forEach(function([key, value]) {
//   ID: "1" -> key:ID, value:"1"

	 // Append a cell to the row for each value
	 // in the stock data report
		var cell = row.append("td");
		cell.text(value);
	  });
	});
}