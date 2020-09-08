What is this:

A docker image which can be used in conjunction with the openfire-docker-compose repo to create automated testing.
It's based of aioxmpp, and is an extremely basic set of test currently which exercise sending and recieving messages 
across federated Openfire servers. 

What's left to do on this?

* Extend the current tests to make them parameterised and push something like the big list of naughty strings through it.
* Add a control mechanism for other docker containers, so the tests can disconnect the XMPP servers to simulate networking
errors. 
* Use the current test methods as helper methods instead, to simplify test generation. 
* Address TODOs already in code. 