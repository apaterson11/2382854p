# 2382854p L4 Project - Builds

Note: our builds are split into two categories here. 
* We have those inside `non-mininet-alternate-builds/`: these are the builds that have been altered to work outside of our testing environemnt i.e. using localhost variables and, in the case of our WebTransport builds, continuing after sending 1000 packets. Our `scripts/` folder utilises these builds.
* And we have those in the root folder here that are either used by our testing environment (and will not work outside of it) or work in and out of the testing environment. The code in our `testing/` folder utilises these builds. 

To get each of these to run, you must run `npm install` within each folder. 

Additionally, the contents of wpt (the platform that runs our server) could not be included in this submission as it was too big. However, I have provided you with this project's python server file in  `wpt-server`. Please clone `https://github.com/web-platform-tests/wpt/` into the `wpt/` folder, and replace the `webtransport_h3_server.py` at `wpt/tools/webtransport/h3` with our `webtransport_h3_server.py` in `wpt-server`. 

Please do not alter this structure as it may affect testing.