async function add_to_cart(id, count){
    rpc_call({'item_id':id,'count':count},'add_to_cart')
}

async function remove_from_cart(item_id) {
  await rpc_call({'item_id':item_id},'remove_from_cart')
  location.reload()
}

async function rpc_call(params, method_name){
  let resp = await fetch('/api/health')
  if (resp.ok){   
    payload = {
            "method": method_name,
            "params": params,
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