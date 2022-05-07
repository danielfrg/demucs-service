import { writable } from "svelte/store";
import type firebase from "firebase/app";

const authStore = writable<firebase.UserInfo>(null);

export default {
  subscribe: authStore.subscribe,
  set: authStore.set,
};
