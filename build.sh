#!/bin/bash

# Source resty
source resty

# Initialize resty
resty http://ionic-builder.tweakbox.net/updates

# Make the Project directory
mkdir Project

# Clone the repository
# NB: Use the HTTPS url to avoid needing to accept the RSA fingerprint
echo "$(date): Cloning from GitHub..."
POST /builder '{"build_id": $1, "status_name": "Cloning Repository", "status_message": "Cloning Repository from GitHub"}'
cd Project && git clone https://github.com/$2/$3

# Export the path for the Android sdk
export PATH=${PATH}:/Development/adt-bundle-linux/sdk/platform-tools:/Development/adt-bundle-linux/sdk/tools

# Add the Android platform to the project
echo "$(date): Adding the Android platform..."
POST /builder '{"build_id": $1, "status_name": "Add Build Target", "status_message": "Adding the Android build target"}'
cd $3 && ionic platform add android

# Build the project
echo "$(date): Building the project..."
POST /builder '{"build_id": $1, "status_name": "Building Project", "status_message": "Building the project"}'
ionic build android

# Tar up the build files
echo "$(date): Compressing build artifacts..."
POST /builder '{"build_id": $1, "status_name": "Compressing Build Artifacts", "status_message": "Compressing build artifacts"}'
cd platforms/android/ant-build
tar -czf /root/$2-$3.tar.gz *.apk
