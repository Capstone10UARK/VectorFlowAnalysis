This file contains details on how to send messages to the command server in src/CommandServer.java.

The command server accepts three types of commands and gives three types of responses as of this version all using JSON.

Commands-

    go
        parameters  - "filePath"    : <string with the path to the location user wants the final CSV>
        explanation - sending the command go and its required file path will start the imageProcessor running on all files in the designated folder and create a .csv with all of the vector data from said files.
        usage       - {"command":"go","filePath":"this/is/a/dummy/path.csv"}
        returns     - commandExecuted response if run successfully
                    - error response if run unsuccesfully or lacking a filePath
        
    progressReport
        parameters  - none
        explanation - sending this command will query the imageProcessor for information on its progress on the current job
        usage       - {"command":"progressReport"}
        returns     - progressReport response
        
    end
        parameters  - none
        explanation - this command will gracefully shutdown the server and close all sockets and streams
        usage       - {"command":"end"}
        returns     - commandExecuted response if run successfully
                    - error response if run unsuccesfully
    
Responses-

    commandExecuted
        parameters  - none
        explanation - receiving this response means that the previous command was executed successfully
        usage       - {"response":"commandExecuted"}
        
    progressReport
        parameters  - "status"      : <either "running" or "done">
                    - "progress"    : <integer that is the percentage of execution of current job>
        explanation - this response is sent after receiveing a progressReport command and gathering the information from the imageProcessor
        usage       - {"response":"progressReport","status":"running","progress":25}
        
    error
        parameters  - "message"     : <message detailing the error that occured>
        explanation - this response will be given if parameters of the previous command were unfulfilled or if the execution of said command failed
        usage       - {"response":"error","message":"Expecting a filePath parameter with go command"}
