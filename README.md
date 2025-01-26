# User Notification System

![Python CI](https://github.com/breynisson/user_notification_system/actions/workflows/python-ci.yml/badge.svg)


## Description

## Usage

### Generate protobuf files
```bash
poetry run generate-grpc
``` 


### Activate Poetry virtual environment
```bash
eval $(poetry env activate)
```

### Start the server
```bash
poetry run python start-server
```

### Send messages to the server
```bash
poetry run send-message {{client_id}} {{message}}
```

### Fetch client status
```bash
poetry run fetch-status {{client_id}}
```

### Fetch all clients status (NOTE: This command is not working currently)
```bash
poetry run fetch-all-status
```


### TODO: Add commands for testing with Allure reports and geneerating the reports


## Notes:
The collections.Mapping attribute has been deprecated and removed in Python 3.10. You should use collections.abc.Mapping instead.  
To fix this issue, you need to update the namedlist.py file to use collections.abc.Mapping. However, since this file is part of a third-party package,
you should consider updating the package to a version that supports Python 3.12 or applying a temporary fix.  Here is a temporary fix you can apply:  
Locate the namedlist.py file in your virtual environment.
Open the file and replace `_collections.Mapping` with `_collections.abc.Mapping`. While this fix will work, it is not
recommended to modify the files in the virtual environment. However, I did this instead of downgrading python.