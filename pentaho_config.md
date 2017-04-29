# Goal
To create a wiki outling any special setup/config needed to replicate the environment

# Plugins: 
• Google Spreadsheet Input/Output
    ```
        Branch: Stable
        Version: 1.0.1
        Developer: Brian Zoetewey
    ```
    
    
# External API's
* Google APIs - https://console.developers.google.com/apis/credentials?project=cuse-analytics
    - Service Account
        - Download both .p12 & json
        - setup w/ client email & p12 file, test connection
        - share the spreadsheet w/ the app email id: read-only@cuse-analytics.iam.gserviceaccount.com
      
* Docker port binding: 
    - https://docs.docker.com/engine/userguide/networking/default_network/binding/