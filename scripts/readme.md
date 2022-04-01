# 2382854p L4 Project - Scripts

NOTE: These scripts will not work until the README instructions in `/builds` have been completed.

To run each of these builds, simply run the "start" batch file within the respective folder.

Please ensure that `npm install` has been run in each build folder before doing this.

Please note that for our WebTransport builds (`datagrams/` and `streams/`) to run, you will need to do the following things.

* You will need to ensure that your PC launches Chrome when you type `chrome` into a terminal.
* You will need to have Anaconda3 installed, specifically the Anaconda Prompt. Additionally, you will need to edit the `client` and `client2` scripts to change the hardcoded destination of Anaconda's active.bat file. You should change the first line to the following: `call C:\Users\<USER>\Anaconda3\Scripts\activate.bat C:\Users\<USER>\Anaconda3` where you replace `<USER>` with your own computer's profile name.
* Chrome settings must be configured. Navigate to `chrome://flags/#allow-insecure-localhost`. Enable "Allow invalid certificates for resources loaded from localhost." and "Insecure origins treated as secure". Finally, disable "Block insecure private network requests."
* Chrome certificates must also be set up. In Chrome, located "Manage Certificates" in your settings. Navigate to the "Trusted Root Certification Authorities" tab and click Import. Follow the instructions to import `setup_instructions/certs/cacert.pem`. If this does not work, follow the instructions in `setup_instructions/certs/README.md`. The certificate this document references is the `cacert.pem` file in the same folder.

To set up our WebTransport over HTTP/3 server, please follow the first three instructions in `setup_instructions/Running WPT WebTransport test server.pdf`.