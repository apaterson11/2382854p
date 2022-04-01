# 2382854p L4 Project - Testing

To run our tests, these scripts must be placed in a Linux machine with Mininet, Selenium and Google Chrome installed. Additionally, please install the required python packages by running `pip install -r` in the same directory as our `requirements.txt` provided in the `setup_instructions/` folder. Additionally, `npm install` may need to be run in each build directory on your machine.

Chrome settings must be configured.
* Navigate to `chrome://flags/#allow-insecure-localhost`. Enable "Allow invalid certificates for resources loaded from localhost." and "Insecure origins treated as secure". In the box below the latter, please enter `http://10.0.0.2:4001/`. Finally, disable "Block insecure private network requests."
* Certificates must also be set up. In Chrome, located "Manage Certificates" in your settings. Navigate to the "Trusted Root Certification Authorities" tab and click Import. Follow the instructions to import `cacert.pem`. If this does not work, follow the instructions in `setup_instructions/certs/README.md`. The certificate this document references is the `cacert.pem` file in the same folder.

To set up our WebTransport over HTTP/3 server, please follow the first three instructions in `setup_instructions/Running WPT WebTransport test server.pdf`.

To actually run a specific test, navigate a terminal window to your desired test folder and run `sudo python <TEST FILE NAME>`. Each test folder contains three scripts: `test-threading1.py`, `test-threading2.py` and whichever is left is the test you must put into `<TEST FILE NAME>`. Once this is executing, you should not touch anything until the script finishes executing.

To alter the independent variables, you can edit the lists that contain them. These will be located directly under the line `def start():`. For bandwidth tests, the list will be called `bw_list`. For loss tests, the list will called `loss_list` and so on.

You must ensure that your webcam is on and available. 

If you quit a script early and Mininet does not shut down properly, you must execute `sudo mn -c` before running any more tests. Otherwise, you will get errors.

If Chrome launches but appears "invisible", you should run the `chrome-fixer.py` file with `sudo python chrome-fixer.py`. As the script is setting up, you should enter `xterm cli1` twice. 
If you do not do this in time, you should ensure all open Chrome windows are terminated, and open two xterminals by typing `xterm cli1` twice. In one terminal, input `chromedriver`. In the other, input `google-chrome --no-sandbox`. This should fix the issue. Type `exit` to leave the Mininet CLI. Remember to execute `sudo mn -c` after this is done.