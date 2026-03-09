# Start on Boot Instructions

The best approach on Raspberry Pi OS is a **systemd service**. It handles "wait for network" cleanly via `After=network-online.target` and `Wants=network-online.target`.

## 1. Create the service file

Create `/etc/systemd/system/tweeting-catflap.service` with the following content:

```ini
[Unit]
Description=Tweeting Catflap
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/Desktop/tweeting-catflap
ExecStart=/home/pi/Desktop/tweeting-catflap/venv/bin/python main.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## 2. Enable and start the service

```bash
sudo systemctl daemon-reload
sudo systemctl enable tweeting-catflap.service
sudo systemctl start tweeting-catflap.service
```

## 3. Ensure network-online.target is active

This target is not always enabled by default. Enable the appropriate service depending on your network manager.

If using **systemd-networkd** (headless/lite Pi OS):

```bash
sudo systemctl enable systemd-networkd-wait-online.service
```

If using **NetworkManager** (desktop Pi OS):

```bash
sudo systemctl enable NetworkManager-wait-online.service
```

## Notes

- `WorkingDirectory` is set to the project directory because `main.py` uses relative paths (`capture.jpg`, `history/`, `grammar.txt`, `capture-image.sh`).
- `ExecStart` calls the venv's Python directly — no need to activate the venv, this is the correct way to use a venv in a service.
- `Restart=on-failure` with a 10 second delay means if the script crashes (e.g. network blip, API error), systemd will restart it automatically.

## Checking logs

```bash
sudo journalctl -u tweeting-catflap -f
```
