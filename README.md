# Logsend

Logsend is the dumb and simple logs aggregator.

Specify what logs to look for and where to send them with straightforward to
understand config files.

## Motivation

I have been running dedicated servers for my personal use for a while now, and
always overlooked the monitoring part. One of my recent workplaces has a very
sophisticated and complete monitoring infrastructure that analyzes logs of
hundred of services across several machines and report critical errors.

When I started looking at existing solutions, or reading the documentation of
the ones used at my workplace, I was left unconvinced. Most of them, even the
open-source ones, are part of bigger proprietary and paid ecosystems.
Furthermore, setting them up always looked like an overly complex task.

I then started to see if it was possible to easily read systemd logs from Python
and trigger an action everytime a new log comes in. Once I had a prototype
running, I decided to turn in into a complete solution for defining "bridges"
that will look at certain logs, and send them to certain places. This is
_logsend_.

## Requirements

- python 3+
- **(systemd logs):** systemd development library
  - For Debian family systems, install the package `libsystemd-dev`
  - For RHEL family systems, install the package `systemd-devel`

## Example configurations

- Send every authentication logs to a Discord webhook

  ```yaml
  inputs:
    - type: AuthLog
  outputs:
    - type: DiscordWebhook
      url: https://discordapp.com/api/webhooks/1234567890/abcdefghijklmnopqrstuvwxyz
  ```

- Logs every systemd logs to logsend's process stderr

  ```yaml
  inputs:
    - Systemd
  outputs:
    - Stderr
  ```

- Watches several files and output them to logsend's stdout

  ```yaml
  inputs:
    - AuthLog
    - type: File
      path: /var/log/nginx/access.log
    - type: File
      path: /var/log/secure
    - type: File
      path: /var/log/maillog
    - type: File
      path: /var/log/dnf.log
  outputs:
    - Stdout
  ```

- Logs systemd logs generated by the sshd.service unit, and send them to Discord
  only after 3 seconds without no new logs except if more than 10 logs are
  already waiting

  ```yaml
  # file 1
  inputs:
    - Systemd
  filters:
    - type: Field
      path: meta/unit
      value: sshd.service
  outputs:
    - type: Stream
      name: ssh-discord
  ```

  ```yaml
  # file 2
  inputs:
    - type: Stream
      name: ssh-discord
  outputs:
    - type: DiscordWebhook
      url: https://discordapp.com/api/webhooks/1234567890/abcdefghijklmnopqrstuvwxyz
  ```

More examples can be found in the `examples` folder.

## Todo for v1.0.0

- [ ] Add formatters injection
- [ ] Add more built-in modules
- [ ] Add a way to write custom modules
- [ ] Properly package and release
- [ ] Write setup instructions
