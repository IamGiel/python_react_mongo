# BACKLOG : 

FRONT:

1. Restrict screens without authentication
2. Display data in Home page (all posts) if user is authenticated

BACK:

1. Allow only owners of post to update and delete their OWN post - done ✅
  
    ```test: check if JJ can change title on fakes post```
2. Allow only admin ability to DELETE ALL post - done ✅

    ```test: check if admin can delete any users post``` 

3. Show only users post "My posts"

    ```Test: login, verify I can check list of my posts only```

### To run (backend):

1. cd into python-server
2. create env file inside python-server

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

3. Save the dependencies in a requirement.txt (install the installer libraries pip-chill or pipreqs then...)

    `pip-chill > requirements.txt`    
    or    
    `pipreqs --encoding=iso-8859-1` 

    then (to unpack)

    `pip install -r requirements.txt`
4. (should install all dependencies)

### To run (FRONTEND):

1. cd client
2. `npm install` 
3. `npm start`
4. react runs it


