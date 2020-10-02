# DoodleUp Backend

## TODO

Progress saving of drawn photo

- Accept file from React Js -> store in flask working dir
- Upload file to Storage -> return Storage link
- Write Storage link & Username to Realtime Database 

## API Endpoint

`https://tanshengrong.pythonanywhere.com/`

## Available APIs

`https://tanshengrong.pythonanywhere.com/asseturl?file_location=assets/<string:filename>`

`https://tanshengrong.pythonanywhere.com/asseturl?file_location=assets/soundFX/<string:filename>`

- **GET**: Get the url of the asset on Firebase Storage

`https://tanshengrong.pythonanywhere.com/signup`

- **POST**: Add User in firebase authentication and add an entry in realtime database
- Requires form(username, email, password)

`https://tanshengrong.pythonanywhere.com/signin`

- **POST**: Check if user exists
- Requires form(username, email, password)

`https://tanshengrong.pythonanywhere.com/resetpassword?email=<string:email>`

- **GET**: Get the result on whether password reset email is successfully sent

`https://tanshengrong.pythonanywhere.com/accountinfo/<string:idToken>`

- **GET**: Get user info - token, email

`https://tanshengrong.pythonanywhere.com/user/<username>`

- **GET**: Get result on whether user exists using Realtime database

`https://tanshengrong.pythonanywhere.com/autosave`

- **POST**: 

`https://tanshengrong.pythonanywhere.com/save`

- **POST**: 

`https://tanshengrong.pythonanywhere.com/progress?username=<string:username>&story=<string:index>`

- **GET**: Get user's progress for the selected story, else initialize

## Tools used

- [Firebase Authentication, Realtime Database, Firebase Storage](https://firebase.google.com)
- [Python Anywhere](https://www.pythonanywhere.com)