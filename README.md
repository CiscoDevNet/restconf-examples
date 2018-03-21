## Cisco DevNet Learning Labs: Sample code for RESTCONF

These scripts use RESTCONF to demonstrate various configurations you can run as examples in the [DevNet Sandbox](https://developer.cisco.com/sandbox/).

Contributions are welcome, and we are glad to review changes through pull requests. See [contributing.md](contributing.md) for details.

The goal of DevNet sample code and learning labs is to ensure a 'hands-on' learning approach rather than just theory or instructions.

## About these Learning Labs

These samples can be run against Cisco hardware available in the [DevNet Sandbox](https://developer.cisco.com/sandbox/). The VLAN example code provisions (or deletes) a VLAN interface on an existing (physical) interface that is connected to an upstream switch via a 802.1Q trunk.

## Contributing

These learning modules are for public consumption, so you must ensure that you have the rights to any content that you contribute.

Write your content in Markdown. DevNet staff reviews content according to the [Cisco Style Guide](http://www-author.cisco.com/c/en/us/td/docs/general/style/guide/Latest/stylegd.html). (Link available on Cisco VPN only.)

#### Publishing Requirements

To create and publish a new lab, take the following steps:
- Add a new folder under `labs`.
- Create a JSON file with the same name as the `labs/`_folder_ name.
- Create markdown files named 1.md, 2.md, and so on; refer to those files in the `labs/`_folder_ JSON file.
- Ensure that the JSON file contains appropriate page titles and file references.
- Send a pull request to get the files committed and merged to `master` by a DevNet reviewer.

A DevNet reviewer then creates a release on the repository with the latest `master` and publishes through the admin interface.

#### Editors

You can write Markdown in a plain text editor, but there are many desktop and Web-based options that allow you to write and preview your work at the same time. We recommend Visual Studio Code [Download](https://code.visualstudio.com/) for several reasons:
- Lightweight environment for coding (or writing Markdown)
- Available on Mac OS, Linux or Windows
- Github Client integration
- Great Markdown preview features native in the editor
- Intuitive operation and structure

You can validate a JSON file by using the [online formatter and validator](https://jsonformatter.curiousconcept.com).

## Getting Involved

* If you'd like to contribute to an existing lab, refer to [contributing.md](contributing.md).
* If you're interested in creating a new Cisco DevNet Learning Lab, please contact a DevNet administrator for guidance.
