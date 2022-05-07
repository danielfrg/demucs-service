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
        .catch((error) => {
            // Handle Errors here.
            const errorCode = error.code;
            const errorMessage = error.message;
        });
}

</script>

{#if thisUser}
    {thisUser.uid}
{:else}
    <button on:click="{loginWithGoogle}">
        Sign in with Google
    </button>
{/if}

<slot />
