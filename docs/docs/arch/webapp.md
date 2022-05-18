# Web Application

The application uses [Astro](https://astro.build/) as a static site generator and
[Svelte](https://svelte.dev/) to provide interactivity in the components that are needed.

## Astro

[Astro](https://astro.build/) produces static HTML content and has the ability to interact with different JS
frameworks for specific parts of the page ([island architecture](https://jasonformat.com/islands-architecture/)).

```html hl_lines="2"
<main class="container max-w-4xl mx-auto mb-auto">
    <UploadFile client:idle />
</main>
```

Astro takes care of loading the needed javascript when the page is loaded.

## Firebase

The Firebase initialization and singleton code can be [found here](https://github.com/danielfrg/demucs-service/blob/main/src/firebase.js).

An important piece is the `firebaseConfig`, this are not needed to be kept secret
and can be just added to the source code of the client (JS on this case).

```javascript
const firebaseConfig = {
    apiKey: import.meta.env.PUBLIC_FIREBASE_API_KEY,
    authDomain: "demucs-service.firebaseapp.com",
    projectId: "demucs-service",
    storageBucket: "demucs-service.appspot.com",
    appId: "1:259910459855:web:35a784beb610343b5732ba"
}
```

## Svelte

We use [Svelte](https://svelte.dev/) to handle the different interactive components:

- Login
- Enable/disable buttons
- File Upload
- Query the model [API endpoint](/docs/api)

We have a single component that handles the different states of the app:

Authentication is required before uploading any files:

```javascript
let thisUser : firebase.UserInfo = null;

onMount(async () => {
    const app = await FirebaseSingleton.getInstance()
    const auth = getAuth(app);

    onAuthStateChanged(auth, (user) => {
        if (user) {
            authStore.set(user);
        } else {
            // User is signed out
            authStore.set(null)
        }
    });
})
```

Enable and disable the buttons when the user is not logged in.

```html
<button
    type="submit"
    class="bg-gray-300 hover:bg-gray-100 text-gray-800 py-1 px-4 border border-gray-400 rounded"
    disabled={thisUser == null}
    on:click="{onSubmit}"
>
    Submit
</button>
```

Read the selected file and send it to the [API endpoint](/docs/api).

```javascript title="Read file in Base 64"
function onSubmit() {
    const file = fileinput.files[0];

    let reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = e => {
        const b64File = e.target.result.split(',')[1];

        processSong(b64File)
            .then(response => response.json())
            .then(data => {
                console.log(data)
                split = data;
            })
            .catch(err => {
                errors["fetch"] = err.message
            });
    };
    reader.onerror = err => {
        console.error(err);
        errors["query"] = err;
    }
}
```

```javascript title="Query model API"
async function processSong(base64File) {
    const endpoint = "https://demucs-api-hwbhnojdya-uc.a.run.app/predict"
    const data = { instances: [{"b64": base64File}] }

    processing = true;
    const promise = fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })

    return promise
}
```
