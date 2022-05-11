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
    console.log("loginWithGoogle")
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
        .catch((error) => {
            // Handle Errors here.
            const errorCode = error.code;
            const errorMessage = error.message;
        });
}

</script>

<div class="my-4 flex flex-col text-gray-100">
    <div class="bg-gray-700 p-8 text-center">

        {#if thisUser}
            <p class="text-center my-3">
                Select a song to be processed: {thisUser.uid}
            </p>
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
                disabled={!thisUser != null}
            />
        </label>
        <button
            type="submit"
            class="bg-gray-300 hover:bg-gray-100 text-gray-800 py-1 px-4 border border-gray-400 rounded"
            disabled={!thisUser != null}
        >
            Submit
        </button>

    </div>
</div>

<slot />
