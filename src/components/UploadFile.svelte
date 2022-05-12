<script lang="ts">
import type firebase from "firebase/app";
import { browserLocalPersistence,getAuth,GoogleAuthProvider,onAuthStateChanged,setPersistence,signInWithPopup } from "firebase/auth";
import { onMount } from 'svelte';
import FirebaseSingleton from '../firebase.js';
import authStore from "../stores/auth";

let thisUser : firebase.UserInfo = null;

onMount(async () => {
    const app = await FirebaseSingleton.getInstance()
    const auth = getAuth(app);

    onAuthStateChanged(auth, (user) => {
        if (user) {
            // User is signed in, see docs for a list of available properties
            // https://firebase.google.com/docs/reference/js/firebase.User
            authStore.set(user);
        } else {
            // User is signed out
            authStore.set(null)
        }
    });

})

authStore.subscribe(async (user) => {
    thisUser = user;
});

async function loginWithGoogle() {
    const app = await FirebaseSingleton.getInstance()
    const auth = getAuth(app);
    const provider = new GoogleAuthProvider();

    setPersistence(auth, browserLocalPersistence)
        .then(() => {
            return signInWithPopup(auth, provider)
                    .then((result) => {
                        // The signed-in user info.
                        const user = result.user;

                        authStore.set(user);

                        // This gives you a Google Access Token. You can use it to access the Google API.
                        // const credential = GoogleAuthProvider.credentialFromResult(result);
                        // const token = credential.accessToken;
                    }).catch((error) => {
                        console.error(error)
                        // Handle Errors here.
                        const errorCode = error.code;
                        const errorMessage = error.message;
                        // The email of the user's account used.
                        const email = error.email;
                        // The AuthCredential type that was used.
                        const credential = GoogleAuthProvider.credentialFromError(error);
                    });
        })
        .catch((err) => {
            // Handle Errors here.
            const errorCode = err.code;
            const errorMessage = err.message;
            errors = err;
        });
}

let fileinput = null;
let errors = {};
let processing: boolean = false;
let split = null;

function onSubmit() {
    const file = fileinput.files[0];

    let reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = e => {
        const b64File = e.target.result.split(',')[1];

        processSong(b64File)
            .then(data => {
                alert("1")
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

async function processSong(base64File) {
    // const endpoint = "http://3.142.221.238:8080/predict"
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

function isEmpty(obj) {
    return Object.keys(obj).length === 0;
}

</script>

<div class="my-4 flex flex-col text-gray-100">
    <div class="bg-gray-700 p-8 text-center">
        {#if !isEmpty(errors) }
            <div class="flex flex-col justify-center items-center">
                {#each Object.entries(errors) as [key, value]}
                    <p>{key} error:</p>
                    <p>{value}</p>
                {/each}
            </div>
        {:else if split != null}
            <table>
                <tbody>
                    <tr>
                        <th>Instrument</th>
                        <th>Track</th>
                    </tr>
                </tbody>
                {#each Object.entries(split) as [key, value]}
                    <tr>
                        <td>{key}</td>
                        <td class="track">
                            <audio class="w-full" controls>
                                <source src={`data:audio/mp3;base64,${value}`} type="audio/mp3" />
                            </audio>
                        </td>
                    </tr>
                {/each}
            </table>
        {:else if processing == true}
            <div class="flex flex-col justify-center items-center">
                Processing...
                <div class="mx-auto lds-ring"><div></div><div></div><div></div><div></div></div>
            </div>
        {:else}
            {#if thisUser}
                <div class="my-6 mt-0">
                    <p class="text-center">
                        Select a song to be processed:
                    </p>
                </div>
            {:else}
                <div class="mb-10">
                    <p>Sign in with Google to upload files.</p>
                    <button class="my-2" on:click="{loginWithGoogle}">
                        <img class="w-60" src="/images/btn_google_signin_dark_pressed_web@2x.png" alt="sign-in" />
                    </button>
                </div>
            {/if}

            <label>
                <input
                    type="file"
                    class="file-picker"
                    accept="audio/*"
                    disabled={thisUser == null}
                    bind:this={fileinput}
                />
            </label>
            <button
                type="submit"
                class="bg-gray-300 hover:bg-gray-100 text-gray-800 py-1 px-4 border border-gray-400 rounded"
                disabled={thisUser == null}
                on:click="{onSubmit}"
            >
                Submit
            </button>
        {/if}

    </div>
</div>

<slot />
