# zigator

Zigator: Security analysis tool for Zigbee networks


## Disclaimer

Zigator is a software tool that analyzes the security of Zigbee networks, which is made available for benign research purposes only.
The users of this tool are responsible for making sure that they are compliant with their local laws and that they have proper permission from the affected network owners.


## Installation

You can install Zigator using pip for Python 3 as follows:
```
$ git clone https://github.com/akestoridis/zigator.git
$ cd zigator/
$ pip3 install .
```

The following command should display the version of Zigator that you installed:
```
$ zigator -v
```

If you get an error message that the `zigator` command was not found, make sure that your system's PATH environment variable includes the directory of the installed executable. For example, if it was installed in `~/.local/bin`, add the following line at the end of your `~/.bashrc` file:
```
export PATH=$PATH:~/.local/bin
```

After reloading your `~/.bashrc` file, you should be able to find the `zigator` command.


## Getting Started

If you cannot capture your own Zigbee packets, you may use the PCAP files of the [CRAWDAD dataset cmu/zigbee‑smarthome](https://doi.org/10.15783/c7-nvc6-4q28) for your analysis.
After submitting the [CRAWDAD registration form](https://crawdad.org/registration-form.html), you will receive a username that will allow you to download the following ZIP files:

* https://crawdad.org/download/cmu/zigbee-smarthome/sth3-room.zip
* https://crawdad.org/download/cmu/zigbee-smarthome/sth2-room.zip
* https://crawdad.org/download/cmu/zigbee-smarthome/sth3-duos.zip
* https://crawdad.org/download/cmu/zigbee-smarthome/sth2-duos.zip
* https://crawdad.org/download/cmu/zigbee-smarthome/sth3-house.zip
* https://crawdad.org/download/cmu/zigbee-smarthome/sth2-house.zip
* https://crawdad.org/download/cmu/zigbee-smarthome/sth3-trios.zip
* https://crawdad.org/download/cmu/zigbee-smarthome/sth2-trios.zip

Each of these ZIP files contains a PCAP file of captured Zigbee packets and a TXT file that provides a description of the experimental setup and the encryption keys that were used. You can then view a synopsis of all the commands that Zigator supports in order to analyze them:
```
$ zigator -h
```


## Publication

Zigator was used in the following publication:

* D.-G. Akestoridis, M. Harishankar, M. Weber, and P. Tague, "Zigator: Analyzing the security of Zigbee-enabled smart homes," 2020, to appear in the Proceedings of the 13th ACM Conference on Security and Privacy in Wireless and Mobile Networks (WiSec).


## License

Copyright (C) 2020 Dimitrios-Georgios Akestoridis

This project is licensed under the terms of the GNU General Public License version 2 only (GPL-2.0-only).
