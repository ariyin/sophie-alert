# Restock Alerts for Sophie (Costco Next)

A Python script that notifies you if out-of-stock items on Sophie (Costco Next) return. 

## Installation

Download the script onto your computer.

```bash
git clone https://github.com/ariyin/sophie-alert
cd sophie-alert
```

Then, install the needed packages for the script.

```bash
pip install -r requirements.txt
```

## Using the Script

### Setup

Create a `.env` file with the following fields filled out:

```
FROM_EMAIL_ADDRESS=email@provider.com
FROM_EMAIL_PASSWORD=password
TO_EMAIL_ADDRESS=email@provider.com
SMTP_SERVER=smtp.server.com
SMTP_PORT=number
```

If you want to use an email with 2FA, create an [app password](https://myaccount.google.com/apppasswords) and use that as the `FROM_EMAIL_PASSWORD`.

To find your SMTP server and port, search [here](https://domar.com/pages/smtp_pop3_server). For example, for Gmail, the `SMTP_SERVER` would be `smtp.gmail.com` and the `SMTP_PORT` would be `587`.

**Note**: I've only tested this for Gmail since I only use Gmail

Replace the `urls` field in `main.py` with the links of the products you wish to track. The links should start with `https://costco.bysophieofficial.com/products/` and everything after a `?` would be extraneous.

### Scheduling

**Mac**

The plist file will run as a LaunchAgent at 8 AM every day. If your computer isn't running at 8 AM, it'll run the next time your computer wakes up.

Change the paths in `sophie.plist` to the appropriate paths and then move the file to `~/Library/LaunchAgents`. If you use a venv environment for Python, create a venv environment in the sophie-alert directory and link the Python path in the plist to the Python path in the `.venv` folder. For example, the path might be `/Users/username/sophie-alert/.venv/bin/python3`.

There are two ways to launch the agent. One is by using terminal commands, and the other is by installing a third-party application. I failed with the terminal commands but they may work for you.

**Terminal Command Method**

Try at your own risk, but this should theoretically work according to this [source](https://davidhamann.de/2018/03/13/setting-up-a-launchagent-macos-cron/).

Find your user id with `id -u` or `id -u <username>`.

In `~/Library/LaunchAgents`, load the agent:

```bash
launchctl bootstrap gui/<user-id> sophie.plist
```

And then kickstart it (or wait):

```bash
launchctl kickstart -k gui/<user-id>/sophie
```

In the future, if you ever wish to unload the agent:

```bash
launchctl bootout gui/<user-id> sophie.plist
```

**Easy GUI Method**

Aka what I did because I failed at the above.

Download [LaunchControl](https://www.soma-zone.com/LaunchControl/). You do not need to purchase anything; the free trial works for our purposes.

Find sophie on the side bar and click the "Load" button on the top. That's all.

**Windows**

Use Task Scheduler to create a new task that runs the script daily.

**Note**: I have not tested anything on Windows
