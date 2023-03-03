# Web-Based ChatGPT Chatbot with Django

- Web-Based ChatGPT Chatbot
  - Remember the conversation in a session
  - Uses NanumSquareNeo font (Neat looking for Korean)

Chatbot with the background tasks processing and communications via WebSockets.
For more details please check my article - [Heroku Chatbot with Celery, WebSockets, and Redis](https://itnext.io/heroku-chatbot-with-celery-websockets-and-redis-340fcd160f06).

Supported by <a href="https://woensug-choi.github.io/" style="text-decoration: none; color: rgb(42, 144, 42); font-weight: bold;">Choi Woen-Sug (Ocean Eng., KMOU)</a>🧑‍🏫

## Installation

- Requirements
  - Supported system : Debian Linux (e.g. Ubuntu)
  - Tested system : Ubuntu 22.04

### Install Redis

```bash
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
sudo apt update && sudo apt install -y redis
```

Check redis by running with following command,

```bash
redis-cli
```
You may see redis url and port. To exit, type `exit`.

## Environment Variables

- REDIS URL
  - default redis url and port is 127.0.0.1:6379
- DJANGO SECRET KEY
  - Obtain at https://djecrety.ir/
  - Replafe `YOUR_DJGANGO_SECRET_KEY` with your key
- OPENAI MODEL
  - Name of the model you want to use.
  - ChatGPT version 3 is `text-davinci-003`
- OPENAI API KEY
  - Obtain at https://platform.openai.com/account/api-keys
  - Replace `YOUR_API_KEY` with your key
- PROMPT OPTION
  - It's an option you want to give to add exaplanation to the prompt.
  - It will be added to the prompt to help better responses.
  - Example would be `Response in 40 words maximum`. You may add as much as you want.

### Set variables

  ```bash
  export PROMPT_OPTION="Response in 40 words maximum."
  export REDIS_URL="redis://127.0.0.1:6379"
  export DJANGO_SECRET_KEY="YOUR_DJGANGO_SECRET_KEY"
  export OPENAI_MODEL='text-davinci-003'
  export OPENAI_API_KEY="YOUR_API_KEY"
  ```

- If you want to fix it and don't type every time
  
  ```bash
  # Export Redis URL (default redis url and port is 127.0.0.1:6379)
  echo "export REDIS_URL='redis://127.0.0.1:6379'" >> ~/.bashrc

  # Export Django Secret Key
  echo 'export DJANGO_SECRET_KEY="YOUR_DJGANGO_SECRET_KEY"' >> ~/.bashrc

  # Export the name of the OpenAI Model
  echo 'export OPENAI_MODEL="text-davinci-003"' >> ~/.bashrc

  # Export OpenAI ChatGPT API Key
  echo 'export OPENAI_API_KEY=YOUR_API_KEY' >> ~/.bashrc
  ```

### Load bashrc for environment variables

```bash
source ~/.bashrc
```

## Get source code

```bash
git clone git@github.com:woensug-choi/SimpleWebChatGPT.git
```

## Install Dependencies

```bash
sudo apt install python3-pip
pip install -r requirements.txt
pip install openai
```

## Run server

### set-up database (ONLY ONCE)

```bash
python manage.py migration
```

### Finally, run the server

```bash
python manage.py runserver 0:8080
```

## Open Browser to access

When running the `python manage.py runserver 0:8080`, you will be given a url to access.
Typical access is http://127.0.0.1:8080. Open with any browser you will have access.



## Example of system service to make it run at background

### Write a service configuration file

- wirte a service configuration file at `/etc/systemd/system/webchatgpt.service` 
- `sudo nano /etc/systmd/system/webchatgpt.service`
- You may change the name `webchatgpt` with anything you want
- CHANGE THE PATH OF `manage.py` in the following example
    
  ```
  # Example of /etc/systemd/system/webchatgpt.service
  [Unit]
  Description=WebChatGPT

  [Service]
  User=ubuntu
  Type=simple
  Restart=always
  ExecStart=/usr/bin/python3 /home/ubuntu/WebChatGPT/manage.py runserver 0:8888

  [Install]
  WantedBy=multi-user.target
  ```

### Run the service,

  ```
  sudo systemctl daemon-reload # Reload the config file
  sudo systemctl enable webchatgpt.service # Enable (make it auto start)
  sudo systemctl start webchatgpt.service # Star the service now
  ```














# Obsolete





## Deployment
You can host it on [Heroku](https://www.heroku.com) for free ([account verification required](https://devcenter.heroku.com/articles/account-verification)).

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
