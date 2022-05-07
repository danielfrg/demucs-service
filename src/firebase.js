import { initializeApp } from "firebase/app";
let resolve, firebaseInstance, firestoreInstance;

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: import.meta.env.PUBLIC_FIREBASE_API_KEY,
  authDomain: import.meta.env.PUBLIC_AUTH_DOMAIN,
  projectId: import.meta.env.PUBLIC_PROJECT_ID,
  storageBucket: import.meta.env.PUBLIC_STORAGE_BUCKET,
  appId: import.meta.env.PUBLIC_APP_ID,
};

const promise = new Promise((res) => (resolve = res));

export async function initialize() {
  if (import.meta.env.SSR) return undefined;
  if (firebaseInstance) return firebaseInstance;

  firebaseInstance = initializeApp(firebaseConfig);
  resolve(firebaseInstance);
  return firebaseInstance;
}

export async function getInstance() {
  // if (import.meta.env.SSR) return undefined;
  // if (firebaseInstance) return firebaseInstance;
  // return promise;
  if (import.meta.env.SSR) return undefined;
  if (firebaseInstance) return firebaseInstance;

  firebaseInstance = initializeApp(firebaseConfig);
  resolve(firebaseInstance);
  return firebaseInstance;
}

export async function getFirestore() {
  if (firestoreInstance) return firestoreInstance;

  const { getFirestore } = import("firebase/firestore");
  await getInstance();
  firestoreInstance = getFirestore();
  return firestoreInstance;
}

export default {
  initialize,
  getInstance,
  getFirestore,
};
