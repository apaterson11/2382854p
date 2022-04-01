# 2382854p L4 Project - Builds

Note: our builds are split into two categories here. 
* We have those inside `non-mininet-alternate-builds/`: these are the builds that have been altered to work outside of our testing environemnt i.e. using localhost variables and, in the case of our WebTransport builds, continuing after sending 1000 packets. Our `scripts/` folder utilises these builds.
* And we have those in the root folder here that are either used by our testing environment (and will not work outside of it) or work in and out of the testing environment. The code in our `testing/` folder utilises these builds. 

Please do not alter this structure as it may affect testing.