/**
 * @fileoverview
 * This file contains the Firebase configuration for the application.
 *
 * IMPORTANT:
 * The configuration values provided here are placeholders.
 * For a production environment, you MUST replace these with your actual
 * Firebase project's configuration. It is strongly recommended to use
 * environment variables to store sensitive information and to avoid
 * committing secrets directly to the repository.
 *
 * For example, using SvelteKit's environment variable handling:
 * import { env } from '$env/dynamic/public';
 *
 * export const firebaseConfig = {
 *   apiKey: env.PUBLIC_FIREBASE_API_KEY,
 *   authDomain: env.PUBLIC_FIREBASE_AUTH_DOMAIN,
 *   projectId: env.PUBLIC_FIREBASE_PROJECT_ID,
 *   storageBucket: env.PUBLIC_FIREBASE_STORAGE_BUCKET,
 *   messagingSenderId: env.PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
 *   appId: env.PUBLIC_FIREBASE_APP_ID,
 * };
 *
 */

export const firebaseConfig = {
  apiKey: "YOUR_API_KEY_HERE",
  authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT_ID.appspot.com",
  messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
  appId: "YOUR_APP_ID",
};

export const APP_ID = "ultimate-sensor-monitor";
