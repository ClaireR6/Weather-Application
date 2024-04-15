function refreshTable( x ) 
{
	x = JSON.parse(x)
	$("#table").html("<tr><th>name</th><th>cost</th></tr>");
	for (i of x) 
	{   
		row = "<tr><td>"+i.code+"</td><td>"+i.temp+"</td></tr>";
		$("#table").html($("#table").html()+row);
		//table.html += row
	}
}

var tableData = $.ajax(
	{
		url: "/",
		method: "GET"
	}
);
tableData.done(refreshTable);
tableData.fail(function( jqXHR, textStatus ) {
	alert( "Request failed: " + textStatus + JSON.stringify(jqXHR) );
});

function userChanged() {
		print('changed')
		var user = $("#user").val();
		var zip = $("#zip").val(); 
		out = {user:user,zip:zip};
		$.post(
			"/user/",
			out,
			refreshTable
		)
}

setInterval(
	function(x) //repeated function
	{
		var tableData = $.ajax(
			{
				url: "/",
				method: "GET"
			}
		);
		tableData.done(refreshTable);
		tableData.fail(function( jqXHR, textStatus ) {
			alert( "Request failed: " + textStatus + JSON.stringify(jqXHR) );
		});
	}, 
	10000 //interval in ms
)
