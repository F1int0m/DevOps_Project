async function add_to_cart(id){
	let resp = await fetch('/api/health')
	if (resp.ok){		
		item_id = document.getElementById('row_id_'+id).getElementsByTagName('th')[0].textContent;
		count = document.getElementById('count_id_'+id).value;
		payload = {
            "method": "add_to_cart",
            "params": {
            	'item_id':item_id,
            	'count':count
            },
            "jsonrpc": "2.0",
            "id": document.cookie
        };
        let response = await fetch('/api/v1/jsonrpc', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json;charset=utf-8'
              },
              body: JSON.stringify(payload)
            });
        console.log(response.json)
	}
}