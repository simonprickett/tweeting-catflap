# Start on Boot Instructions

The best approach on Raspberry Pi OS is a **systemd service**. It handles "wait for network" cleanly via `After=network-online.target` and `Wants=network-online.target`.

## 1. Create the service file

From the terminal, enter the following command to create and edit a new file:

```bash
sudo vi /etc/systemd/system/tweeting-catflap.service
```

In the Vi editor press "i" to enter edit mode.

Paste the following into the editor (this assumes you installed the code using a user named `daphne`, if your user is named something else, update `/home/daphne` in two locations below to represent your user name):

```ini
[Unit]
Description=Tweeting Catflap
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/daphne/Desktop/tweeting-catflap
ExecStart=/home/daphne/Desktop/tweeting-catflap/venv/bin/python main.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Now press `Esc` to exit edit mode.  

Press `:wq` to save and exit the Vi editor.

## 2. Enable and start the service

Enter the following commands in the terminal:

```bash
sudo systemctl daemon-reload
sudo systemctl enable tweeting-catflap.service
sudo systemctl start tweeting-catflap.service
```

## 3. Ensure network-online.target is active

This target is not always enabled by default. Enable the appropriate service depending on your network manager.

If using **NetworkManager** (desktop Pi OS), enter the following command in the terminal:

```bash
sudo systemctl enable NetworkManager-wait-online.service
```

If using **systemd-networkd** (headless/lite Pi OS), enter the following command in the terminal:

```bash
sudo systemctl enable systemd-networkd-wait-online.service
```

## Reboot to test it...

From the terminal:

```bash
sudo reboot
```

The Pi will reboot.  When it's started up again, trigger the cat flap and ensure that a new post appears.

## Checking logs

At any time, you can check the service logs by entering this command in the terminal:

```bash
sudo journalctl -u tweeting-catflap -f
```

Press `Ctrl-C` to stop viewing the latest log entries.

## Stopping / Disabling the Service

If you want to stop the service:

```bash
sudo systemctl stop tweeting-catflap.service
```

If you want to disable the service so that it no longer runs on boot:

```bash
sudo systemctl disable tweeting-catflap.service
```