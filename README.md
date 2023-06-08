# Casual Progress Discord Bot

## Features

- `/logs [start|stop]`: Starts or stops the logging coroutine. Only for users with administrator permissions.
  - **start**: Begins the logging coroutine.
  - **stop**: Stops the logging coroutine.

- `/logs-from [date]`: Returns the logs from a given date. Only for users with the role "Raidbewerber" or higher.

- `/guild-profile [once|start|stop]`: Shows the guild's raider.io profile.
  - **once**: Sends the guild's raider.io profile as a message. Only for users with the role "Raidbewerber" or higher.
  - **start**: Begins a coroutine to periodically update the guild's embed with the new raider.io profile information. Only for users with administrator permissions.
  - **stop**: Stops the raider.io profile update coroutine. Only for users with administrator permissions.

- `/move [source] [destination]`: Moves all users from one channel to another. Only for users with administrator permissions.

- `/raidbots`: Shows the login credentials of the raidbots account. Only for users with the role "Raidmember" or higher.

- `/bug`: Report a bug.
    - After sending this command, the bot will direct message you asking for details about the bug.

- `/request-feature`: Request a feature.
    - After sending this command, the bot will direct message you asking for details about the feature request.


# Setup

## Critical prerequisites to install

* Setup a virtual environment ```python -m venv venv/```
* Run ```pip3 install -r requirements.txt```

* **Rename the file `.env.example` to `.env`**

* Recommended python version `3.10`
## Step 1: Create a Discord bot

1. Go to https://discord.com/developers/applications create an application
2. Build a Discord bot under the application
3. Get the token from bot setting

   ![image](https://user-images.githubusercontent.com/89479282/205949161-4b508c6d-19a7-49b6-b8ed-7525ddbef430.png)
4. Store the token to `.env` under the `DISCORD_BOT_TOKEN`

   <img height="190" width="390" alt="image" src="https://user-images.githubusercontent.com/89479282/222661803-a7537ca7-88ae-4e66-9bec-384f3e83e6bd.png">

5. Turn MESSAGE CONTENT INTENT `ON`

   ![image](https://user-images.githubusercontent.com/89479282/205949323-4354bd7d-9bb9-4f4b-a87e-deb9933a89b5.png)

6. Invite your bot to your server via OAuth2 URL Generator

   ![image](https://user-images.githubusercontent.com/89479282/205949600-0c7ddb40-7e82-47a0-b59a-b089f929d177.png)
## Step 2: Official API authentication

   ### Generate an Warcraft Logs API key
   1. Go to https://www.warcraftlogs.com/profile

   2. Scroll down and click Generate new v1 API key

   3. Store the SECRET KEY to `.env` under the `WARCRAFT_LOGS_API_KEY`

   ### Generate a GitHub personal access token
   1. Go to https://github.com/settings/tokens

   2. Click on "Generate new token"

   3. Select the repo scope for the token

   4. Store the generated token in `.env` under `GITHUB_PERSONAL_ACCESS_TOKEN`

## Step 3: Run the bot on the desktop

1. Open a terminal or command prompt

2. Navigate to the directory where you installed this Discord bot

3. Run `python3 main.py` or `python main.py` to start the bot

## Step 3: Run the bot with Docker

1. Build the Docker image & Run the Docker container `docker compose up -d`

2. Inspect whether the bot works well `docker logs -t casual-progress-bot`

   ### Stop the bot:

   * `docker ps` to see the list of running services
   * `docker stop <BOT CONTAINER ID>` to stop the running bot

## Optional: Disable logging

* Set the value of `LOGGING` in the `.env` to False

