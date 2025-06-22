
// this file is generated — do not edit it


/// <reference types="@sveltejs/kit" />

/**
 * Environment variables [loaded by Vite](https://vitejs.dev/guide/env-and-mode.html#env-files) from `.env` files and `process.env`. Like [`$env/dynamic/private`](https://svelte.dev/docs/kit/$env-dynamic-private), this module cannot be imported into client-side code. This module only includes variables that _do not_ begin with [`config.kit.env.publicPrefix`](https://svelte.dev/docs/kit/configuration#env) _and do_ start with [`config.kit.env.privatePrefix`](https://svelte.dev/docs/kit/configuration#env) (if configured).
 * 
 * _Unlike_ [`$env/dynamic/private`](https://svelte.dev/docs/kit/$env-dynamic-private), the values exported from this module are statically injected into your bundle at build time, enabling optimisations like dead code elimination.
 * 
 * ```ts
 * import { API_KEY } from '$env/static/private';
 * ```
 * 
 * Note that all environment variables referenced in your code should be declared (for example in an `.env` file), even if they don't have a value until the app is deployed:
 * 
 * ```
 * MY_FEATURE_FLAG=""
 * ```
 * 
 * You can override `.env` values from the command line like so:
 * 
 * ```bash
 * MY_FEATURE_FLAG="enabled" npm run dev
 * ```
 */
declare module '$env/static/private' {
	export const VITE_API_BASE_URL: string;
	export const VITE_WEBSOCKET_URL: string;
	export const VITE_APP_TITLE: string;
	export const VITE_DEBUG: string;
	export const VITE_LOG_LEVEL: string;
	export const ALLUSERSPROFILE: string;
	export const APPDATA: string;
	export const ChocolateyInstall: string;
	export const ChocolateyLastPathUpdate: string;
	export const CommonProgramFiles: string;
	export const CommonProgramW6432: string;
	export const COMPUTERNAME: string;
	export const ComSpec: string;
	export const CONDA_PROMPT_MODIFIER: string;
	export const DriverData: string;
	export const EFC_13112_1262719628: string;
	export const EFC_13112_1592913036: string;
	export const EFC_13112_2283032206: string;
	export const EFC_13112_2775293581: string;
	export const EFC_13112_3789132940: string;
	export const FPS_BROWSER_APP_PROFILE_STRING: string;
	export const FPS_BROWSER_USER_PROFILE_STRING: string;
	export const GOPATH: string;
	export const HOME: string;
	export const HOMEDRIVE: string;
	export const HOMEPATH: string;
	export const INIT_CWD: string;
	export const LOCALAPPDATA: string;
	export const LOGONSERVER: string;
	export const NODE: string;
	export const NODE_ENV: string;
	export const NODE_OPTIONS: string;
	export const NODE_PATH: string;
	export const npm_command: string;
	export const npm_config_audit_level: string;
	export const npm_config_auto_install_peers: string;
	export const npm_config_child_concurrency: string;
	export const npm_config_dedupe_peer_dependents: string;
	export const npm_config_enable_pre_post_scripts: string;
	export const npm_config_frozen_lockfile: string;
	export const npm_config_fund: string;
	export const npm_config_loglevel: string;
	export const npm_config_network_concurrency: string;
	export const npm_config_node_gyp: string;
	export const npm_config_node_options: string;
	export const npm_config_prefer_frozen_lockfile: string;
	export const npm_config_registry: string;
	export const npm_config_user_agent: string;
	export const npm_config_verify_deps_before_run: string;
	export const npm_config__jsr_registry: string;
	export const npm_execpath: string;
	export const npm_lifecycle_event: string;
	export const npm_lifecycle_script: string;
	export const npm_node_execpath: string;
	export const npm_package_json: string;
	export const npm_package_name: string;
	export const npm_package_version: string;
	export const NUMBER_OF_PROCESSORS: string;
	export const NVM_HOME: string;
	export const NVM_SYMLINK: string;
	export const OMP_NUM_THREADS: string;
	export const OS: string;
	export const Path: string;
	export const PATHEXT: string;
	export const PM_PACKAGES_ROOT: string;
	export const pnpm_config_verify_deps_before_run: string;
	export const PNPM_SCRIPT_SRC_DIR: string;
	export const POSH_CURSOR_COLUMN: string;
	export const POSH_CURSOR_LINE: string;
	export const POSH_INSTALLER: string;
	export const POSH_SESSION_ID: string;
	export const POSH_SHELL: string;
	export const POSH_SHELL_VERSION: string;
	export const POSH_THEME: string;
	export const POSH_THEMES_PATH: string;
	export const POWERLINE_COMMAND: string;
	export const POWERSHELL_DISTRIBUTION_CHANNEL: string;
	export const POWERSHELL_TELEMETRY_OPTOUT: string;
	export const PROCESSOR_ARCHITECTURE: string;
	export const PROCESSOR_IDENTIFIER: string;
	export const PROCESSOR_LEVEL: string;
	export const PROCESSOR_REVISION: string;
	export const ProgramData: string;
	export const ProgramFiles: string;
	export const ProgramW6432: string;
	export const PROMPT: string;
	export const PSModulePath: string;
	export const PUBLIC: string;
	export const PYENV: string;
	export const PYENV_VIRTUALENV_DISABLE_PROMPT: string;
	export const SESSIONNAME: string;
	export const SSH_SOCKET_DIR: string;
	export const SystemDrive: string;
	export const SystemRoot: string;
	export const TEMP: string;
	export const TERM_PROGRAM: string;
	export const TMP: string;
	export const UAPATH: string;
	export const USERDOMAIN: string;
	export const USERDOMAIN_ROAMINGPROFILE: string;
	export const USERNAME: string;
	export const USERPROFILE: string;
	export const VIRTUAL_ENV_DISABLE_PROMPT: string;
	export const WARP_HONOR_PS1: string;
	export const WARP_IS_LOCAL_SHELL_SESSION: string;
	export const WARP_SHELL_DEBUG_MODE: string;
	export const WARP_USE_SSH_WRAPPER: string;
	export const windir: string;
	export const ZES_ENABLE_SYSMAN: string;
	export const __COMPAT_LAYER: string;
}

/**
 * Similar to [`$env/static/private`](https://svelte.dev/docs/kit/$env-static-private), except that it only includes environment variables that begin with [`config.kit.env.publicPrefix`](https://svelte.dev/docs/kit/configuration#env) (which defaults to `PUBLIC_`), and can therefore safely be exposed to client-side code.
 * 
 * Values are replaced statically at build time.
 * 
 * ```ts
 * import { PUBLIC_BASE_URL } from '$env/static/public';
 * ```
 */
declare module '$env/static/public' {
	export const PUBLIC_WS_URL: string;
}

/**
 * This module provides access to runtime environment variables, as defined by the platform you're running on. For example if you're using [`adapter-node`](https://github.com/sveltejs/kit/tree/main/packages/adapter-node) (or running [`vite preview`](https://svelte.dev/docs/kit/cli)), this is equivalent to `process.env`. This module only includes variables that _do not_ begin with [`config.kit.env.publicPrefix`](https://svelte.dev/docs/kit/configuration#env) _and do_ start with [`config.kit.env.privatePrefix`](https://svelte.dev/docs/kit/configuration#env) (if configured).
 * 
 * This module cannot be imported into client-side code.
 * 
 * Dynamic environment variables cannot be used during prerendering.
 * 
 * ```ts
 * import { env } from '$env/dynamic/private';
 * console.log(env.DEPLOYMENT_SPECIFIC_VARIABLE);
 * ```
 * 
 * > In `dev`, `$env/dynamic` always includes environment variables from `.env`. In `prod`, this behavior will depend on your adapter.
 */
declare module '$env/dynamic/private' {
	export const env: {
		VITE_API_BASE_URL: string;
		VITE_WEBSOCKET_URL: string;
		VITE_APP_TITLE: string;
		VITE_DEBUG: string;
		VITE_LOG_LEVEL: string;
		ALLUSERSPROFILE: string;
		APPDATA: string;
		ChocolateyInstall: string;
		ChocolateyLastPathUpdate: string;
		CommonProgramFiles: string;
		CommonProgramW6432: string;
		COMPUTERNAME: string;
		ComSpec: string;
		CONDA_PROMPT_MODIFIER: string;
		DriverData: string;
		EFC_13112_1262719628: string;
		EFC_13112_1592913036: string;
		EFC_13112_2283032206: string;
		EFC_13112_2775293581: string;
		EFC_13112_3789132940: string;
		FPS_BROWSER_APP_PROFILE_STRING: string;
		FPS_BROWSER_USER_PROFILE_STRING: string;
		GOPATH: string;
		HOME: string;
		HOMEDRIVE: string;
		HOMEPATH: string;
		INIT_CWD: string;
		LOCALAPPDATA: string;
		LOGONSERVER: string;
		NODE: string;
		NODE_ENV: string;
		NODE_OPTIONS: string;
		NODE_PATH: string;
		npm_command: string;
		npm_config_audit_level: string;
		npm_config_auto_install_peers: string;
		npm_config_child_concurrency: string;
		npm_config_dedupe_peer_dependents: string;
		npm_config_enable_pre_post_scripts: string;
		npm_config_frozen_lockfile: string;
		npm_config_fund: string;
		npm_config_loglevel: string;
		npm_config_network_concurrency: string;
		npm_config_node_gyp: string;
		npm_config_node_options: string;
		npm_config_prefer_frozen_lockfile: string;
		npm_config_registry: string;
		npm_config_user_agent: string;
		npm_config_verify_deps_before_run: string;
		npm_config__jsr_registry: string;
		npm_execpath: string;
		npm_lifecycle_event: string;
		npm_lifecycle_script: string;
		npm_node_execpath: string;
		npm_package_json: string;
		npm_package_name: string;
		npm_package_version: string;
		NUMBER_OF_PROCESSORS: string;
		NVM_HOME: string;
		NVM_SYMLINK: string;
		OMP_NUM_THREADS: string;
		OS: string;
		Path: string;
		PATHEXT: string;
		PM_PACKAGES_ROOT: string;
		pnpm_config_verify_deps_before_run: string;
		PNPM_SCRIPT_SRC_DIR: string;
		POSH_CURSOR_COLUMN: string;
		POSH_CURSOR_LINE: string;
		POSH_INSTALLER: string;
		POSH_SESSION_ID: string;
		POSH_SHELL: string;
		POSH_SHELL_VERSION: string;
		POSH_THEME: string;
		POSH_THEMES_PATH: string;
		POWERLINE_COMMAND: string;
		POWERSHELL_DISTRIBUTION_CHANNEL: string;
		POWERSHELL_TELEMETRY_OPTOUT: string;
		PROCESSOR_ARCHITECTURE: string;
		PROCESSOR_IDENTIFIER: string;
		PROCESSOR_LEVEL: string;
		PROCESSOR_REVISION: string;
		ProgramData: string;
		ProgramFiles: string;
		ProgramW6432: string;
		PROMPT: string;
		PSModulePath: string;
		PUBLIC: string;
		PYENV: string;
		PYENV_VIRTUALENV_DISABLE_PROMPT: string;
		SESSIONNAME: string;
		SSH_SOCKET_DIR: string;
		SystemDrive: string;
		SystemRoot: string;
		TEMP: string;
		TERM_PROGRAM: string;
		TMP: string;
		UAPATH: string;
		USERDOMAIN: string;
		USERDOMAIN_ROAMINGPROFILE: string;
		USERNAME: string;
		USERPROFILE: string;
		VIRTUAL_ENV_DISABLE_PROMPT: string;
		WARP_HONOR_PS1: string;
		WARP_IS_LOCAL_SHELL_SESSION: string;
		WARP_SHELL_DEBUG_MODE: string;
		WARP_USE_SSH_WRAPPER: string;
		windir: string;
		ZES_ENABLE_SYSMAN: string;
		__COMPAT_LAYER: string;
		[key: `PUBLIC_${string}`]: undefined;
		[key: `${string}`]: string | undefined;
	}
}

/**
 * Similar to [`$env/dynamic/private`](https://svelte.dev/docs/kit/$env-dynamic-private), but only includes variables that begin with [`config.kit.env.publicPrefix`](https://svelte.dev/docs/kit/configuration#env) (which defaults to `PUBLIC_`), and can therefore safely be exposed to client-side code.
 * 
 * Note that public dynamic environment variables must all be sent from the server to the client, causing larger network requests — when possible, use `$env/static/public` instead.
 * 
 * Dynamic environment variables cannot be used during prerendering.
 * 
 * ```ts
 * import { env } from '$env/dynamic/public';
 * console.log(env.PUBLIC_DEPLOYMENT_SPECIFIC_VARIABLE);
 * ```
 */
declare module '$env/dynamic/public' {
	export const env: {
		PUBLIC_WS_URL: string;
		[key: `PUBLIC_${string}`]: string | undefined;
	}
}
