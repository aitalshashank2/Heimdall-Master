# Heimdall - Master

This repository contains code for the Master Server of Project Heimdall.

---

## Heimdall

Heimdall is a GitHub based server login manager. It uses GitHub to track the SSH Keys and manage the access of the servers.

### Functionalities:

- Accessing the servers is just one PR away
- Real time monitoring of the server login logs
- Stores all the logs for future reference in a database
- Notifications on slack for all login related activities activity
- Easy integration of a new server
- Everything covered in a single Docker Network!

---

## Master - Setup

- Clone the repository
    ```
    git clone https://github.com/aitalshashank2/Heimdall-Master.git
    ```

- Make a repository to store the SSH-Keys
    ```
    git clone https://github.com/aitalshashank2/Heimdall-SSH-Keys-Stencil.git
    ```

- Change the visibility of this repository to **Private**. You can find visibility controls in the settings tab.

- Make a GitHub OAuth Token. This token will be later used by the app to watch the repository with SSH Keys.
    - For generating a token, head to the *Settings* option available in the drop down menu seen after clicking the down arrow at the top right.
    - In the *Developer Settings* section, choose *Personal Access Tokens*
    - Click on *Generate new token*. After naming the token, give the token access to read private repositories by checking the **repo** scope.
    - Click on *Generate Token*

- We need to make a GitHub Webhook in order to track the changes in the SSH-Keys repository. For making a webhook, follow these steps:
    - Head to Project *Settings*
    - In *Webhooks* section, click *Add webhook*
    - Fill the Payload URL as `<URL that is going to be assigned to master>/bipolar/gh`
    - Content Type: `application/x-www-form-urlencoded`
    - Secret: A Random Secret which will be used for authentication later
    - Select `Just the push event` for the events that trigger the webhook
    - Uncheck `Active` status
    - Click on *Add Webhook*

- Now, go to the cloned **Heimdall - Master** for server setup
    ```bash
    cd .../Heimdall-Master
    ```

- We need to set up certain environment variables first. Go to the `configuration` folder
    ```bash
    cd Heimdall/configuration
    ```

- Copy `config-stencil.yml` to `config.yml`
    ```bash
    cp config-stencil.yml config.yml
    ```

- Fill `config.yml` with appropriate values
    ```yml
    DEBUG: (TRUE / FALSE)
    USE_TZ: FALSE # DO NOT CHANGE
    SECRET_KEY: # A fifty character key used by Django for hashing

    DATABASE:
        HOST: db # DO NOT CHANGE
        NAME: # The name of the database which stores the logs
        USER: # The user having rights to the database
        PASSWORD: # Password for the user
        PORT: # Port on which the database container is listening
    
    ALLOWED_HOSTS:
        - "web" # DO NOT CHANGE
    
    GITHUB:
        REPOSITORY: /Heimdall-ssh-keys/
        SECRET: # The secret that was used while making the webhook
        OAUTHTOKEN: # OAuth Token generated in the Fourth step
    
    SERVERSIDE:
        SECRET: # A secret that will be used by Heimdall to verify requests from different Servers internally
    
    SLACK: # URL to the Slack API listening to Heimdall's Webhook.
    ```

- Build the docker network and containers using `docker-compose.yml`
    ```bash
    cd ../..
    docker-compose build --build-arg GITHUB_URL=https://<your-oauth-token-here>:x-oauth-basic@github.com/<your-username-here>/Heimdall-SSH-Keys.git
    ```

- Once the network and containers are made, you can start **Heimdall - Master**
    ```bash
    docker-compose up -d
    ```

- If you want to stop the server, use,
    ```bash
    docker-compose down
    ```

- Now all you need to do is run [Heimdall-Serverside](https://github.com/aitalshashank2/Heimdall-serverside.git) on your servers!


