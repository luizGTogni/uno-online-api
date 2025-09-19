import js from "@eslint/js";
import globals from "globals";
import tseslint from "typescript-eslint";
import eslintPluginTs from "@typescript-eslint/eslint-plugin";
import eslintPluginPrettier from "eslint-plugin-prettier";
import { defineConfig } from "eslint/config";

export default defineConfig([
  {
    files: ["**/*.{js,mjs,cjs,ts,mts,cts}"],
    plugins: { js, prettier: eslintPluginPrettier },
    extends: ["js/recommended"],
    languageOptions: { globals: globals.node },
    rules: {
      ...eslintPluginTs.configs.recommended.rules,
      "prettier/prettier": "error",
    },
  },

  {
    ignores: ["dist", "node_modules"],
  },
  tseslint.configs.recommended,
]);
