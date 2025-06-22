// /src/lib/services/firebase.svelte.ts
import { browser } from "$app/environment";
import { initializeApp, type FirebaseApp } from "firebase/app";
import {
  getAuth,
  onAuthStateChanged,
  GoogleAuthProvider,
  signInWithPopup,
  signOut as firebaseSignOut,
  type User,
} from "firebase/auth";
import {
  getFirestore,
  collection,
  doc,
  setDoc,
  getDocs,
  deleteDoc,
  serverTimestamp,
  type Firestore,
} from "firebase/firestore";

import { firebaseConfig, APP_ID } from "$lib/config/firebase";
import type { DashboardLayout } from "$lib/types/dashboard";
import type { WidgetConfig } from "$lib/types/widgets";
import type { Preset } from "$lib/types/presets";

// Check if Firebase is properly configured
const isFirebaseConfigured = firebaseConfig.apiKey !== "YOUR_API_KEY_HERE";
const DEMO_MODE = !isFirebaseConfigured;

type FirebaseService = {
  app: FirebaseApp | null;
  auth: ReturnType<typeof getAuth> | null;
  db: Firestore | null;
  user: User | null;
  isAuthenticated: boolean;
  signInWithGoogle: () => Promise<void>;
  signOut: () => Promise<void>;
  savePreset: (
    name: string,
    layout: DashboardLayout,
    widgets: Record<string, WidgetConfig>,
  ) => Promise<string | null>;
  loadPresets: () => Promise<Preset[]>;
  deletePreset: (presetId: string) => Promise<void>;
};

function createFirebaseService(): FirebaseService {
  let app: FirebaseApp | null = null;
  let auth: ReturnType<typeof getAuth> | null = null;
  let db: Firestore | null = null;

  if (browser && !DEMO_MODE) {
    try {
      app = initializeApp(firebaseConfig);
      auth = getAuth(app);
      db = getFirestore(app);
    } catch (error) {
      console.warn("Firebase initialization failed - running in demo mode", error);
    }
  }

  let user = $state<User | null>(null);

  if (auth) {
    onAuthStateChanged(auth, (currentUser) => {
      user = currentUser;
    });
  }

  async function signInWithGoogle() {
    if (DEMO_MODE) {
      console.log("[Demo Mode] Sign-in simulation");
      return;
    }
    if (!auth) return;
    const provider = new GoogleAuthProvider();
    try {
      await signInWithPopup(auth, provider);
    } catch (error) {
      console.error("Error signing in with Google:", error);
    }
  }

  async function signOut() {
    if (DEMO_MODE) {
      console.log("[Demo Mode] Sign-out simulation");
      return;
    }
    if (!auth) return;
    try {
      await firebaseSignOut(auth);
    } catch (error) {
      console.error("Error signing out:", error);
    }
  }

  async function savePreset(
    name: string,
    layout: DashboardLayout,
    widgets: Record<string, WidgetConfig>,
  ): Promise<string | null> {
    if (DEMO_MODE) {
      console.log("[Demo Mode] Saving preset to localStorage:", name);
      const presets = JSON.parse(localStorage.getItem("demo-presets") || "[]");
      const preset = {
        id: `demo-${Date.now()}`,
        name,
        layout,
        widgets,
        createdAt: new Date().toISOString(),
        author: "Demo User"
      };
      presets.push(preset);
      localStorage.setItem("demo-presets", JSON.stringify(presets));
      return preset.id;
    }
    
    if (!db || !user) {
      console.error("User not authenticated or Firestore not initialized.");
      return null;
    }

    const presetId = `${name.replace(/\s+/g, "-")}-${Date.now()}`;
    const presetRef = doc(
      db,
      `artifacts/${APP_ID}/users/${user.uid}/presets/${presetId}`,
    );

    try {
      await setDoc(presetRef, {
        name,
        layout,
        widgets,
        createdAt: serverTimestamp(),
        author: user.displayName || user.email,
      });
      console.log("Preset saved successfully:", presetId);
      return presetId;
    } catch (error) {
      console.error("Error saving preset:", error);
      return null;
    }
  }

  async function loadPresets(): Promise<Preset[]> {
    if (DEMO_MODE) {
      console.log("[Demo Mode] Loading presets from localStorage");
      return JSON.parse(localStorage.getItem("demo-presets") || "[]");
    }
    
    if (!db || !user) {
      console.error("User not authenticated or Firestore not initialized.");
      return [];
    }
    const presetsCol = collection(
      db,
      `artifacts/${APP_ID}/users/${user.uid}/presets`,
    );
    try {
      const snapshot = await getDocs(presetsCol);
      return snapshot.docs.map((d) => ({ id: d.id, ...d.data() }) as Preset);
    } catch (error) {
      console.error("Error loading presets:", error);
      return [];
    }
  }

  async function deletePreset(presetId: string) {
    if (DEMO_MODE) {
      console.log("[Demo Mode] Deleting preset:", presetId);
      const presets = JSON.parse(localStorage.getItem("demo-presets") || "[]");
      const filtered = presets.filter((p: any) => p.id !== presetId);
      localStorage.setItem("demo-presets", JSON.stringify(filtered));
      return;
    }
    
    if (!db || !user) {
      console.error("User not authenticated or Firestore not initialized.");
      return;
    }
    const presetRef = doc(
      db,
      `artifacts/${APP_ID}/users/${user.uid}/presets/${presetId}`,
    );
    try {
      await deleteDoc(presetRef);
      console.log("Preset deleted successfully:", presetId);
    } catch (error) {
      console.error("Error deleting preset:", error);
    }
  }

  return {
    get app() {
      return app;
    },
    get auth() {
      return auth;
    },
    get db() {
      return db;
    },
    get user() {
      return user;
    },
    get isAuthenticated() {
      return !!user;
    },
    signInWithGoogle,
    signOut,
    savePreset,
    loadPresets,
    deletePreset,
  };
}

export const firebase = createFirebaseService();
