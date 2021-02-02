# House API

## Building and Running
First, you will need to create a virtual environment for running this program. 'cd' into the **`api`** directory and run:

### 'python3 -m venv env' activate with 'venv/scripts/Activate.ps1' leave venv with 'deactivate'

Next, you will need to install the dependencies from **`requirements.txt`** run:

### 'pip install -r requirements.txt'

You're now ready to run; from the 'api' directory, enter:

### 'python -m flask run'

And the server should be up and running. Make your requests on Postman as you see fit.

## Testing

The testing file is **`tests`/`house_test.py`** to run this make sure you are in the parent **`House-API`** directory and then enter

### 'python -m tests.house_test'

## Implementation Improvements

I had some trouble with setting the 'Accepts' header on requests to 'Accepts: application/json'. I tried some scripts in Postman as well as trying to set a before_request script in Flask but those were both unsuccessful. If I had more time this is an issue I feel like I could resolve.
I also wish I could've covered more http error code handlers or handlers that were more comprehensive. Creating scenarios to get some of the errors would take a lot more time I believe and as my implementation went on I realized I did not have as much time to dedicate to these situations.
Lastly, I would've liked to trim down the number of dependencies for the project.

## API Design

I found my implementation to be pretty straight forward. I have a single GET for the request for all houses and another method that serves the other GET and PUT request. If I were to refractor this second method I would probably make the logic for the two requests more consequential. They are somewhat interleaving the logic which could hurt readability. Lastly, I believe dividing up my models, init, view, and tests all into different files was very efficient and helpful when trying to track down bugs or make additions to the code.

## Security Implications

There are some security implications at play here. One I thought of was how I parse the **`houses.csv`** file to make my database. This could potentially be a security risk if a non .csv file was used or just a .csv file that does not follow the same formatting as **`houses.csv`**. Also, a lack of complete handling of HTTP error codes could cause some troubles if new issues arise as more clients use the program.