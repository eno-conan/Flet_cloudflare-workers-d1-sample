export interface Env {
	// Example binding to KV. Learn more at https://developers.cloudflare.com/workers/runtime-apis/kv/
	// MY_KV_NAMESPACE: KVNamespace;
	//
	// Example binding to Durable Object. Learn more at https://developers.cloudflare.com/workers/runtime-apis/durable-objects/
	// MY_DURABLE_OBJECT: DurableObjectNamespace;
	//
	// Example binding to R2. Learn more at https://developers.cloudflare.com/workers/runtime-apis/r2/
	// MY_BUCKET: R2Bucket;
	//
	// Example binding to a Service. Learn more at https://developers.cloudflare.com/workers/runtime-apis/service-bindings/
	// MY_SERVICE: Fetcher;
	MY_SAMPLE_DB: D1Database;
}

export default {
	async fetch(
		request: Request,
		env: Env,
		ctx: ExecutionContext
	): Promise<Response> {
		const { pathname } = new URL(request.url);
		if (pathname === "/api/") {
			if (request.method.toUpperCase() === 'POST') {
				// POST request
				const body = await request.text();
				const req = JSON.parse(body);
				const company_name = req.CompanyName
				const contract_name = req.ContactName
				const { results } = await env.MY_SAMPLE_DB.prepare(
					`insert into Customers(CompanyName, ContactName) values(?,?)
					`).bind(company_name, contract_name).run()
				return Response.json(results);
			}
			// GET request get all
			const { results } = await env.MY_SAMPLE_DB.prepare(
				"SELECT * FROM Customers"
			).all();
			// GET request add filtering
			// const { results } = await env.MY_SAMPLE_DB.prepare(
			// 	"SELECT * FROM Customers WHERE CompanyName = ?"
			// )
			// 	.bind("Bs Beverages")
			// 	.all();
			return Response.json(results);
		}
		return new Response("Other '/api/' route");
	},
};