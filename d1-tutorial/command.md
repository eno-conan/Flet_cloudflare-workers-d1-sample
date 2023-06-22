# Get Started
https://developers.cloudflare.com/d1/get-started/

### Cache POST requests
https://developers.cloudflare.com/workers/examples/cache-post-request/

### execute sql
npx wrangler d1 execute sample-d1 --local --file=./schema.sql
npx wrangler d1 execute sample-d1 --file=./schema.sql
npx wrangler d1 execute sample-d1 --local --command='SELECT * FROM Customers'

### local dev
npx wrangler dev --local --persist

### Workder deploy
wrangler publish

### Honoをもちいた処理実装
https://developers.cloudflare.com/d1/tutorials/build-a-comments-api/
