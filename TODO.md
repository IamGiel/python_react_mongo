TODOS: 

1. Restrict screens without authentication
2. Display data in Home page (all posts) if user is authenticated
3. Ability to create post in dashboard
4. Keep the user token, so that a refresh wont logout user
5. error route /error -> show error state

To run:

1. create env file inside python-server

    ``` #------FOR LINUX/MAC---------#
        #installing venv 
        sudo apt-get install python3.6-venv
        #creating virtual env
        python3 -m venv env
        #activating virtual env
        source env/bin/activate


        #-------FOR WINDOWS----------#
        #installing venv
        py -m pip install --user virtualenv
        #creating virtual env
        py -m venv env
        #activating virtual env
        .\env\Scripts\activate
        
    ```

2. `pip install -r requirements.txt` 
3. (should install all dependencies)
