# Evalbot
Evalbot is a simple discord bot that evaluates Lisp expressions and returns the output of the Lisp expressions.

## Usage
To use evalbot, you can clone the repository using `git clone https://github.com/lattiahirvio/evalbot.git`. After which, you need to create a file called ".env", 
and add your discord token in there in the format of `TOKEN=<your-token>`. After that, run the bot using `python main.py`. Your bot should now be running. To evaluate lisp expressions, use 
`;eval (expr)`.

## Security
Currently the bot has next to no protections against Denial of Service attacks. These will be added at a later date. 

Although the bot does run somewhat arbitrary Lisp code, it should have no effect on the host operating system. The interpreter has no I/O outside of discord, 
and no primitive types are given to the interpreter. In case the bot is not secure, create an issue in the issues tab.

## Contributing
Pull requests are welcome and appreciated. Any sufficiently good code will be merged, as long as the code is commented, and the code follows Pythonic conventions.

## Acknowledgements
The Lisp interpreter in this bot was made according to Peter Norvig's [Lis.py](https://norvig.com/lispy.html).
