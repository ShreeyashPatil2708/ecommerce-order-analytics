#!/bin/bash

echo "📦 Packaging Lambda functions..."

# Create lambda-packages directory
mkdir -p lambda-packages

# Package Data Processor using PowerShell
echo "Packaging data-processor..."
cd src/lambda/data-processor
powershell.exe -Command "Compress-Archive -Path lambda_function.py -DestinationPath ../../../lambda-packages/data-processor.zip -Force"
cd ../../..

# Package Report Generator using PowerShell
echo "Packaging report-generator..."
cd src/lambda/report-generator
powershell.exe -Command "Compress-Archive -Path lambda_function.py -DestinationPath ../../../lambda-packages/report-generator.zip -Force"
cd ../../..

echo "✅ Lambda packages created in lambda-packages/"
ls -lh lambda-packages/
