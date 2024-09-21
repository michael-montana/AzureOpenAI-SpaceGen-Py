targetScope = 'subscription'

// Ensure the allowed locations match your requirements
@allowed([
  'westeurope'
  'switzerlandnorth'
])
param AZURE_LOCATION string = 'westeurope'

// Ensure the service name matches your environment variable
param OPEN_AI_SERVICE_NAME string = 'AzureOpenAi-SpaceGen-Py'

// Define the resource group
resource resourceGroup 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: 'rg-${OPEN_AI_SERVICE_NAME}'
  location: AZURE_LOCATION
}

// Deploy the OpenAI service module
module openAiServiceModule 'modules/openai-service.bicep' = {
  name: 'deployOpenAiService'
  scope: resourceGroup
  params: {
    location: AZURE_LOCATION
    openAiServiceName: OPEN_AI_SERVICE_NAME
  }
}
