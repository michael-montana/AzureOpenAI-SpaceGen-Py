# Set the necessary variables
$resourceGroupName = "your-resource-group"
$openAiServiceName = "myAzureOpenAIService"
$subscriptionId = "your-subscription-id"
$apiKey = "your-api-key-from-bicep-output"

# Define the endpoint URL for Azure OpenAI Service
#$endpoint = "https://$($openAiServiceName).openai.azure.com/v1/completions"
$endpoint = "https://$openAiServiceName.openai.azure.com/openai/deployments/$deploymentName/completions?api-version=$apiVersion"


# Define the request body for the OpenAI prompt
$prompt = @"
Create a Python script that uses Blender to generate a 3D model of a cube and save it as an STL file.
"@

# Define the request JSON body for the Azure OpenAI API
$body = @{
    prompt = $prompt
    max_tokens = 150
    model = "text-davinci-003"  # You can change this to any other model available in Azure OpenAI
} | ConvertTo-Json

# Make the API request
$response = Invoke-RestMethod -Uri $endpoint -Method Post -Headers @{
    "api-key" = $apiKey
    "Content-Type" = "application/json"
} -Body $body

# Parse and display the Python script generated
$pythonScript = $response.choices[0].text
Write-Output "Generated Python script for Blender:"
Write-Output $pythonScript

# Optionally save the generated Python script to a file
$scriptPath = "C:\Path\To\Save\GeneratedScript.py"
$pythonScript | Out-File -FilePath $scriptPath

Write-Output "Python script saved to: $scriptPath"
