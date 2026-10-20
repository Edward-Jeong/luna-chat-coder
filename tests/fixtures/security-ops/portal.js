// Synthetic customer-portal fixture; contains no customer data.
const endpoint = '/api/scan/results';
export async function fetchScanResults(client, assetId) {
  return client.get(endpoint, { params: { assetId } });
}
