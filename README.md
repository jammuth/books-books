# Firebase Setup Instructions

> To use Firebase in your project, you need to add a `firebaseconfig.json` file to the root directory. This file contains your Firebase service account credentials.

## How to get a new `firebaseconfig.json`

1. **Log in to the [Firebase Console](https://console.firebase.google.com/).**
2. **Select your project.**
3. **Go to Project Settings** (the gear icon).
4. **Click the Service Accounts tab.**
5. **Click _Generate new private key_.** This will download a JSON file.
6. **Rename the downloaded file to `firebaseconfig.json`.**
7. **Move `firebaseconfig.json` to the root folder of your project.**

> This file is required for your code to authenticate and interact with Firebase services. **Make sure to keep it secure and never commit it to public repositories.**