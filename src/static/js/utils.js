var last_AdjClose = 0;
var last_Close = 0;
var last_Open = 0;
var last_High = 0;
var last_Low = 0;
var last_Date = "";
$(function(){
	$('#btnRefresh').click(function(){

		$.ajax({
			url: '/refresh',
			data: $('fieldset').serialize(),
			type: 'POST',
			success: function(response){
			     if (IsJsonString(response)){
                    text = JSON.parse(response);
                    if ("error" in text) {
                        alert(text['error']);
                    }else if ("message" in text) {
                        csv_to_table('../static/data/aapl.csv');
                        setPriceHTML();
                        draw_chart('../static/data/aapl.csv');
                        draw_chart_macd('../static/data/aapl.csv');
                    }
                } else {
                    alert(response);
                }
			},
			error: function(error){
				console.log(error);
			}
		});
	});
	$('#btnScrape').click(function(){

    		$.ajax({
    			url: '/scrape',
                data: $('fieldset').serialize(),
    			type: 'POST',
    			success: function(response){
    				console.log(response);
    				if (IsJsonString((response))) {
    				    text = JSON.parse(response);
    				    if ("error" in text) {
                            alert(text['error']);
                        }else {
    				        aaplData(response);
    				        setPriceHTML();
                            draw_chart('../static/data/aapl.csv');
                            draw_chart_macd('../static/data/aapl.csv');
                        }
    				} else{
    				    alert(response);
    				}
    			},
    			error: function(error){
    				console.log(error);
    			}
    		});
    	});
    $('#btnLoadAAPL').click(function(){
                $.ajax({
                    url: '/load',
        			data: $('fieldset').serialize(),
                    type: 'POST',
                    success: function(response){
                        if (IsJsonString(response)){
                            text = JSON.parse(response);
                            if ("error" in text) {
                                alert(text['error']);
                            }else {
                                alert(text[Object.keys(text)[0]]);
                            }
                        } else {
                            alert(response);
                        }
                    },
                    error: function(error){
                        console.log(error);
                    }
                });
            });
});

function setPriceHTML(){
    $('#last_Date').text(last_Date);
    $('#last_Open').text(last_Open);
    $('#last_High').text(last_High);
    $('#last_Low').text(last_Low);
    $('#last_Close').text(last_Close);
    $('#last_AdjClose').text(last_AdjClose);
    delta = last_AdjClose-$('#cost').text()
    $('#delta').text(last_AdjClose-$('#cost').text());
}

function IsJsonString(str) {
    try {
        JSON.parse(str);
    }
    catch (e) {
        return false;
    }
    return true;
}

function csv_to_table(file_name){
    var tbody = d3.select("#aapl-table-body");
    tbody.selectAll("tr").remove();
    var url ='../static/data/aapl.csv';
//    url + '?' + Math.floor(Math.random() * 1000)
    d3.csv(file_name + '?' + Math.floor(Math.random() * 1000), function(data) {
      console.log(data.Open);
      tabulate(data);
    });
}
var tabulate = function (value) {
    var tbody = d3.select("#aapl-table-body");
    // Use d3 to update each cell's text with
    // a data from row
    row = tbody.append("tr");
    cell = row.append("td");
//    date = new Date(value.Date).toISOString().substring(0, 10);
    date = value.Date;
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
    cell.text(value["Adj. Close"]);
    cell = row.append("td");
    cell.text(value.Volume);
    last_Close=value.Close;
    last_Open=value.Open;
    last_High=value.High;
    last_Date = date;
    last_Low=value.Low;
    last_AdjClose=value["Adj. Close"];
}

function aaplData(tableData) {
    if (tableData != "Error") {
        var tbody = d3.select("#aapl-table-body");
            tbody.selectAll("tr").remove();
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
            last_Close=value.Close;
            last_Open=value.Open;
            last_High=value.High;
            last_Low=value.Low;
            last_Date = date;
            last_AdjClose=value["Adj Close"];
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