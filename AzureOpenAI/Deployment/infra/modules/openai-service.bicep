param location string
param openAiServiceName string

resource openAiService 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: openAiServiceName
  location: location
  kind: 'OpenAI'
  sku: {
    name: 'S0'
  }
  properties: {
    apiProperties: {
      apiVersion: 'v3'
    }
  }
}

output openAiServiceName string = openAiService.name
output openAiServiceKey string = listKeys(openAiService.id, '2023-05-01').key1
output openAiServiceEndpoint string = 'https://${openAiService.name}.openai.azure.com/'
