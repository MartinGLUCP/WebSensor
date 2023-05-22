function getDataForGraphics(requestGraphicType){ //modif

	var list = null;
	var data_action;
	
	switch(requestGraphicType){
	
		case "lineChart" :
			data_action = "action=getDataLine";
			break;
			
		case "bubbleChart":
			data_action = "action=getDataBubble";
			break;
			
		default :
			alert("Le type de graphique n'est pas renseigné dans le function getDataForGraphics");
			data_action = "action=getDataLine";
	}
	
	$.ajax({
		method : "GET",
		url : 'pdo/sql_request.php',
		async : false,
		data : data_action,
		dataType : "json",
		accepts : "application/json; charset=utf-8",
	}).done(function(data) {
		list = data;
		console.log(data);

	}).fail(function(data) {
		
		var respObj = null;
		var msg;

		try {
			respObj = JSON.parse(data.responseText);
			msg = respObj.msg;
		} catch (err) {
			msg = data.responseText;
		}
		alert(msg);
	});
	return list;
}