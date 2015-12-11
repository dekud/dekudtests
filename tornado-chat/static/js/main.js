var lastId = -1;
function update_messages()
{
	$.ajax({
    url: '/messages?last='+lastId,       
    dataType : "json",                   
    success: function (data, textStatus) { 
        $.each(data, function(i, d)
		{    
			$("#table_event tr:first").after("<tr><td>"+d['user']+"</td><td>"+d['text']+"</td><td>"+d['datetime']+"</td></tr>");
			lastId = d['id']
        });
		//$("#div_body")[0].scrollTop = $("#div_body")[0].scrollHeight;
    } 
	});
	setTimeout(function(){ update_messages()},10000);
}

function sendCmd(cmd, dev)
{
    alert(cmd);
    $.ajax({
    url: '/cmd?cmd='+cmd + '&dev='+dev,
    success: function (data, textStatus) {
    }
	});
}
