# BACKLOG : 

FRONT:

1. Restrict screens without authentication
2. Display data in Home page (all posts) if user is authenticated

BACK:
1. Allow only owners of post to update their OWN post - done ✅
2. Allow only admin ability to update ANY post <--
3. Allow only owner of post to delete their OWN post
4. Allow only admin can delete ANY posts <--

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

3. `pip install -r requirements.txt` or `pip-chill > requirements.txt`
4. (should install all dependencies)

### To run (FRONTEND):

1. cd client
2. `npm install` 
3. `npm start`
4. react runs it


