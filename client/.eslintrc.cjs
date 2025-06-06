module.exports = {
  root: true,
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:svelte/recommended',
    'prettier'
  ],
  parser: '@typescript-eslint/parser',
  plugins: ['@typescript-eslint', 'svelte'],
  parserOptions: {
    sourceType: 'module',
    ecmaVersion: 2020,
    extraFileExtensions: ['.svelte']
  },
  env: {
    browser: true,
    es2017: true,
    node: true
  },
  overrides: [
    {
      files: ['*.svelte'],
      parser: 'svelte-eslint-parser',
      parserOptions: {
        parser: '@typescript-eslint/parser'
      }
    }
  ],
  rules: {
    // Disable rules that conflict with Svelte 5's state management
    '@typescript-eslint/no-explicit-any': 'off',
    'no-undef': 'off',
    // Add custom rules for Svelte 5
    'svelte/valid-compile': 'error',
    'svelte/no-at-html-tags': 'error',
    'svelte/no-dom-manipulating': 'error',
    'svelte/no-dupe-else-if-blocks': 'error',
    'svelte/no-dupe-style-properties': 'error',
    'svelte/no-dynamic-slot-name': 'error',
    'svelte/no-inner-declarations': 'error',
    'svelte/no-not-function-handler': 'error',
    'svelte/no-object-in-text-mustaches': 'error',
    'svelte/no-shorthand-style-property-overrides': 'error',
    'svelte/no-unknown-style-directive-property': 'error',
    'svelte/no-unused-svelte-ignore': 'error',
    'svelte/no-useless-mustaches': 'error',
    'svelte/require-store-callbacks-use-set-param': 'off', // Disabled for Svelte 5
    'svelte/require-store-reactive-access': 'off', // Disabled for Svelte 5
    'svelte/require-stores-init': 'off', // Disabled for Svelte 5
    'svelte/valid-compile': 'error',
    'svelte/valid-compile-svelte': 'error',
    // Add rules for Svelte 5 state management
    '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    '@typescript-eslint/explicit-module-boundary-types': 'off',
    '@typescript-eslint/no-non-null-assertion': 'off',
    '@typescript-eslint/no-empty-interface': 'off',
    '@typescript-eslint/no-empty-function': 'off',
    '@typescript-eslint/no-var-requires': 'off',
    '@typescript-eslint/ban-ts-comment': 'off',
    '@typescript-eslint/ban-types': 'off',
    '@typescript-eslint/no-this-alias': 'off',
    '@typescript-eslint/no-extra-semi': 'off',
    '@typescript-eslint/no-extra-parens': 'off',
    '@typescript-eslint/no-extra-boolean-cast': 'off',
    '@typescript-eslint/no-extra-non-null-assertion': 'off',
    '@typescript-eslint/no-extra-semi': 'off',
    '@typescript-eslint/no-extra-parens': 'off',
    '@typescript-eslint/no-extra-boolean-cast': 'off',
    '@typescript-eslint/no-extra-non-null-assertion': 'off'
  },
  settings: {
    'svelte3/typescript': () => require('typescript'),
    'svelte3/ignore-styles': () => true,
    'svelte3/ignore-warnings': warning => {
      // Ignore warnings about Svelte 5's state management
      if (warning.code === 'svelte-valid-compile') return true;
      if (warning.code === 'svelte-require-store-callbacks-use-set-param') return true;
      if (warning.code === 'svelte-require-store-reactive-access') return true;
      if (warning.code === 'svelte-require-stores-init') return true;
      if (warning.code === 'typescript-eslint/no-explicit-any') return true;
      if (warning.code === 'typescript-eslint/no-non-null-assertion') return true;
      if (warning.code === 'typescript-eslint/no-empty-interface') return true;
      if (warning.code === 'typescript-eslint/no-empty-function') return true;
      if (warning.code === 'typescript-eslint/no-var-requires') return true;
      if (warning.code === 'typescript-eslint/ban-ts-comment') return true;
      if (warning.code === 'typescript-eslint/ban-types') return true;
      if (warning.code === 'typescript-eslint/no-this-alias') return true;
      if (warning.code === 'typescript-eslint/no-extra-semi') return true;
      if (warning.code === 'typescript-eslint/no-extra-parens') return true;
      if (warning.code === 'typescript-eslint/no-extra-boolean-cast') return true;
      if (warning.code === 'typescript-eslint/no-extra-non-null-assertion') return true;
      return false;
    }
  }
} 