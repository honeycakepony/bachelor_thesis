<h1>Purpose of this Repository</h1>
This repository is used for my code base which I use for my bachelor thesis on improving the interoperability of some components, namely Policy Enforcement Point and Policy Decision Point, within a Zero Trust Architecture.<br />
For this, I'm building upon the [Special Publication from the National Institute of Standards and Technology](https://www.nist.gov/publications/zero-trust-architecture) and the ongoing effort of the [Authorization API](https://openid.github.io/authzen/authorization-api-1_1_01), which is currently developed by the AuthZen Working Group as part of the OpenID Foundation.<br /> 
<b>Note</b>: The code in this repository is experimental and represents the submission state of my bachelor thesis.

<h2>Run the Code on your System</h2>

Navigate into the 'demonstration' folder and run `python3 pdp_main_functions.py` in one terminal. 
The server, i.e. the PDP, responds '* Running on http://127.0.0.1:2111'. 
Please make sure that all modules which are imported in the practical implementation have to be installed on your system.

Open another terminal and navigate to the 'demonstration' folder.
To run an attack scenario, run `python3 -m unittest testing/test_as_ra.py` in your terminal.

In the terminal which was used for the PDP, the following output is displayed:<br>
Non-parametrised Access Request:
```
check_params -> _check_params_subject:  False
	_is_valid_stype: 'user' is valid? 'True'
	_is_valid_sid: 'account3@mission−thesis.org' is valid? 'True'
```

Parametrised Access Request:
```
check_params -> _check_params_subject:  True
	_is_valid_stype: 'user' is valid? 'True'
	_is_valid_sid: 'account3@mission−thesis.org' is valid? 'True'
	check_params_subject -> pdp_os.is_required_param_valid: fingerprint for account3@mission−thesis.org
    ...
```